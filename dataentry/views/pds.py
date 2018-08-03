import json
import logging
import inspect

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.cache import cache
from api.ehb_service_client import ServiceClient
from api.utilities import SubjectUtils

from ehb_client.requests.exceptions import PageNotFound
from ehb_datasources.drivers.exceptions import RecordDoesNotExist,\
    RecordCreationError, IgnoreEhbExceptions

from .base import DataEntryView

log = logging.getLogger(__name__)


class StartView(DataEntryView):
    '''
    Renders a page with the list of current records in a Protocol Data Source
    with id = pds_id for the Subject with ehb-service id = subject_id. The
    exact form of this page is protocol_data_source dependent as determined by
    the driver
    '''

    template_name = 'pds_dataentry_start.html'

    def generateSubRecordSelectionForm(
            self, driver, record_id, form_url, attempt_count,
            max_attempts, redcap_form_complete_codes={}):

        if redcap_form_complete_codes:
            try:
                form = driver.subRecordSelectionForm(
                    form_url=form_url,
                    record_id=record_id,
                    redcap_form_complete_codes=redcap_form_complete_codes
                )
                try:
                    self.request.META['action'] = 'Sub record selection form generated.'
                except:
                    pass
                return form
            except RecordDoesNotExist:
                return None
        # Nautilus will not have redcap_form_complete_code field
        else:
            try:
                form = driver.subRecordSelectionForm(
                    form_url=form_url,
                    record_id=record_id
                )
                self.request.META['action'] = 'Sub record selection form generated.'
                return form
            except RecordDoesNotExist:
                return None

    # Method to create and load color codes for redcap form tables
    # cache key is by protocoldatasource: 'protocoldatasource#_redcap_completion_codes'
    # cache value is {subjectid: {recordid: {form_spec: completion_code, form_spec: completion_code}}}
    def redcap_form_complete_caching(self, driver, cache_key, subject_id, record_id, record_name):

        def construct_field_names(list_of_forms):
            form_completion_fields=[]
            for form in list_of_forms:
                form_completion_fields.append(form + "_complete")
            return form_completion_fields

        def assign_form_statuses(driver, record, completion_fields, event_index=-1):
            form_statuses = {}
            for field in completion_fields:
                form_complete_value = record[field]
                form_name = field[:-9]
                # key is the form spec according to driver config
                if event_index == -1: # nonlong study
                    key = str(driver.form_names.index(form_name))
                else:
                    key = str(driver.form_data_ordered.index(form_name)) + "_" + str(event_index)
                    # key = str(list(driver.form_data.keys()).index(form_name)) + "_" + str(event_index)
                if (form_complete_value == '1'):
                    form_statuses[key] = 1
                elif (form_complete_value == '2'):
                    form_statuses[key] = 2
            return form_statuses

        def get_and_cache_completion_codes (self, cache_data={}, subject_records={}):
            completion_codes = {}
            if driver.form_names: # nonlongitudinal studies
                completion_fields = construct_field_names(driver.form_names)
                record_set = driver.get(_format=driver.FORMAT_JSON,
                                  records=[record_name],
                                  rawResponse=True,
                                  fields=completion_fields).read().strip()
                record_set = driver.raw_to_json(record_set)
                # iterate through the record set to find the completion field
                for r in record_set:
                    completion_codes = assign_form_statuses(driver,r, completion_fields)

            else: # longitudinal studies
                # must specify field study_id for redcap api to return study_id and event name
                field_names = [driver.record_id_field_name]
                completion_fields = construct_field_names(list(driver.form_data.keys()))
                field_names += completion_fields
                temp = driver.get(_format=driver.FORMAT_JSON, rawResponse=True,
                            records=[record_name], fields=field_names).read().strip()
                record_set = driver.raw_to_json(temp)
                record_set = json.loads(json.dumps(record_set)) # have to reload json in order for the field redcap_event_name to be read

                first_event = True
                for r in record_set: # iterate through the record set to find the completion field
                    redcap_eventname = r['redcap_event_name']
                    if redcap_eventname in driver.unique_event_names:
                        event_index = driver.unique_event_names.index(redcap_eventname)
                        if first_event:
                            completion_codes = assign_form_statuses(driver,r, completion_fields, event_index)
                            first_event = False
                        else:
                            # merge the 2 dictionaries
                            completion_codes = {**completion_codes, **assign_form_statuses(driver,r, completion_fields, event_index)}

            subject_records[record_id] = completion_codes # {recordid: {form_spec: completion_code, form_spec: completion_code}}
            cache_data[subject_id] = subject_records # {subjectid: {recordid: {form_spec: completion_code, form_spec: completion_code}}}
            cache.set(cache_key, cache_data, timeout=172800) # cache key expires after 2 days
            cache.persist(cache_key)
            return completion_codes

        cache_data = cache.get(cache_key)
        if cache_data: # cache key exists
            if subject_id in cache_data:
                subject_records = cache_data[subject_id]   # get all records of the subject
                if record_id in subject_records:
                    redcap_completion_codes = subject_records[record_id] # load the completion codes
                else: # record table hasn't been generated for that record
                    redcap_completion_codes = get_and_cache_completion_codes(self, cache_data, subject_records)
            else: # subject hasn't been added to cache
                redcap_completion_codes = get_and_cache_completion_codes(self, cache_data)
        else: # cache key doesn't exist
            redcap_completion_codes = get_and_cache_completion_codes(self)
        return redcap_completion_codes

    def get_context_data(self, **kwargs):
        context = super(StartView, self).get_context_data(**kwargs)
        form_url = '{root}/dataentry/protocoldatasource/{pds_id}/subject/{subject_id}/record/{record_id}/form_spec/'.format(
            root=self.service_client.self_root_path,
            **kwargs)
        # Get name of driver class to differentiate between Redcap and Nautilus
        driverClass = inspect.getfile(self.driver.__class__)
        if "redcap" in str(driverClass):
            cache_key = 'protocoldatasource{pds_id}_redcap_completion_codes'.format(root=self.service_client.self_root_path, **kwargs)
            subject_id = context['subject'].id
            record_id = context['record'].id
            record_name = context['record'].record_id
            redcap_form_complete_codes = self.redcap_form_complete_caching(self.driver, cache_key, subject_id, record_id, record_name)
            context['redcap_complete_legend'] = '<div class="pull-right"><div class="col-md-6"><table class = "table table-borderless"><tbody><tr><td style="border:none" align="center"> <button class="btn btn-primary"><i class="fa fa-circle-o"></i> </button></td><td style="border:none" align="center"> <button class="btn btn-warning"><i class="fa fa-adjust"></i> </button></td><td style="border:none" align="center"> <button class="btn btn-success"><i class="fa fa-circle"></i> </button></td> </tr> <tr><td style="border:none">Incomplete</td> <td style="border:none">Unverified</td><td style="border:none">Complete</td></tr> </tbody> </table></div></div> '
            context['subRecordSelectionForm'] = self.generateSubRecordSelectionForm(
                self.driver, context['record'].record_id, form_url,0,1, redcap_form_complete_codes)
        else: # this is a nonredcap project
            context['subRecordSelectionForm'] = self.generateSubRecordSelectionForm(
                self.driver, context['record'].record_id, form_url,0,1)
        return context


class FormView(DataEntryView):

    template_name = 'pds_dataentry_srf.html'

    def generateSubRecordForm(self, driver, external_record, form_spec, attempt_count, max_attempts):
        try:
            form = driver.subRecordForm(external_record=external_record,
                                        form_spec=form_spec,
                                        session=self.request.session)
            self.request.META['action'] = 'Sub record form generated.'
            return form
        except RecordDoesNotExist:
            return None

    def get_context_data(self, **kwargs):
        context = super(FormView, self).get_context_data(**kwargs)
        form_submission_url = '{root}/dataentry/protocoldatasource/{pds_id}/subject/{subject_id}/record/{record_id}/form_spec/{form_spec}/'.format(
            root=self.service_client.self_root_path,
            **kwargs)
        try:
            forms = json.loads(context['pds'].driver_configuration)['form_order']
            current_index = forms.index(kwargs['form_spec'])
            next_form = forms[current_index + 1]
            next_form_url = '{root}/dataentry/protocoldatasource/{pds_id}/subject/{subject_id}/record/{record_id}/form_spec/{next_form}/'.format(
                root=self.service_client.self_root_path,
                next_form=next_form,
                **kwargs)
        except:
            next_form_url = ''
        context['form_submission_url'] = form_submission_url
        context['next_form_url'] = next_form_url
        context['subRecordForm'] = self.generateSubRecordForm(
            self.driver,
            context['record'],
            kwargs['form_spec'],
            0,
            1)
        return context

    # update cache for subrecordselectionform, class StartView
    def update_cache(self, cache_key, subject_id, record_id):
        cache_data = cache.get(cache_key)
        try:
            if cache_data:
                if subject_id in cache_data:
                    subject_data = cache_data[subject_id]
                    if record_id in subject_data:
                        del subject_data[record_id]
                    cache_data[subject_id] = subject_data
                cache.set(cache_key, cache_data, timeout=172800) # cache key expires after 2 days
                cache.persist(cache_key)
        except:
            raise Exception('Record form was not updated')


    # this method is called when users submits forms
    # if there exists any errors, we display elements from
    # pds_dataentry_srf.html and this is called with
    # formBuilderJson.py from ehb_datasources
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # have the driver process this request
        errors = self.driver.processForm(
            request=request, external_record=context['record'], form_spec=kwargs['form_spec'], session=request.session)

        # this grabs the filepath of the driver instance to
        # differentiate from nautilus and redcap driver
        driverClass = inspect.getfile(self.driver.__class__)

        if errors:
            self.request.META['action'] = 'Errors processing form.'
            self.request.META['user_error_msg'] = errors
            self.request.META['error'] = True
            error_msgs = [e for e in errors]
            context['errors'] = error_msgs
            # if this is a redcap error message, need to clean and parse
            if "redcap" in str(driverClass):
                # this is to clean the redcap error message
                errors = errors.replace("Exception('", "")
                errors = errors.replace ("',)","")
                json_errors = errors
                errors = errors.split ('"')
                # overwrite the previous META for user_error_msg
                # errors[3] = field Name
                # errors [5] = redcap message
                self.request.META['user_error_msg'] = "Error in this field: " + errors[3] + ". " + errors [5]
                return  JsonResponse({'status': 'error', 'errors': json_errors})
            return JsonResponse({'status': 'error', 'errors': errors})
        else:
            self.request.META['action'] = 'Form processed.'
            self.request.META['subject_id'] = context['subject'].id  #The ehb PK for this subject
            # For all processed forms, clear cache for record selection table
            cache_key = 'protocoldatasource{pds_id}_redcap_completion_codes'.format(
                root=self.service_client.self_root_path, **kwargs)
            subject_id = context['subject'].id
            record_id = context ['record'].id
            try:
                self.update_cache(cache_key, subject_id, record_id)
            except:
                request.META['error'] = True
                context['errors'].append((
                    'Error in updating redcap completion code.'))
            return JsonResponse({'status': 'ok'})


class CreateView(DataEntryView):

    template_name = 'pds_dataentry_rec_create.html'

    def create_external_system_record(self, request, driver, pds, subject, record_id=None, label=None):

        def rec_id_validator(new_record_id):
            return SubjectUtils.validate_new_record_id(
                pds, subject, new_record_id)

        grp = SubjectUtils.get_protocol_subject_record_group(pds.protocol, subject)
        if grp:
            rec_id_prefix = grp.ehb_key
        else:
            request.META['action'] = 'No subject record group found'
            request.META['error'] = True
            raise Exception('No subject record group found')
        rec_id = None

        if record_id:
            if record_id.startswith(rec_id_prefix):
                rec_id = driver.create(
                    record_id_prefix=None, record_id=record_id, record_id_validator=rec_id_validator)
            else:
                rec_id = driver.create(
                    record_id_prefix=rec_id_prefix, record_id=record_id)
        else:
            rec_id = driver.create(
                record_id_prefix=rec_id_prefix, record_id_validator=rec_id_validator)

        er = SubjectUtils.create_new_ehb_external_record(
            pds, request.user, subject, rec_id, label)
        return er.id

    def check_cache(self):
        cache_key = 'protocol{0}_sub_data'.format(self.pds.protocol.id)
        self.cached_data = cache.get(cache_key)
        if self.cached_data:
            return True

    def update_cache(self):
        subs = json.loads(self.cached_data)
        for sub in subs:
            if sub['id'] == int(self.subject.id):
                er = self.get_external_record(record_id=self.record_id)
                context = {"record": er}
                label = self.get_label(context)
                exRec = json.loads(er.json_from_identity(er))
                exRec['pds'] = self.pds.id
                exRec['label_id'] = label['id']
                if label['label'] == '':
                    label['label'] = 'Record'
                exRec['label_desc'] = label['label']
                if exRec['external_system'] == 3:
                    sub['external_ids'].append(exRec)
                sub['external_records'].append(exRec)
        cache_key = 'protocol{0}_sub_data'.format(self.pds.protocol.id)
        cache.set(cache_key, json.dumps(subs))
        cache.persist(cache_key)
        self.check_cache()

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        if self.driver.new_record_form_required():
            # Generate the form and pass it to the template (Nautilus)
            form = self.driver.create_new_record_form(self.request)
            context['recordCreateForm'] = form
            context['form_submission_url'] = self.create_path
        return context

    def dispatch(self, request, *args, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        allow_more_records = False
        try:
            records = self.service_client.get_rh_for(
                record_type=ServiceClient.EXTERNAL_RECORD).get(
                    external_system_url=self.pds.data_source.url,
                    subject_id=self.subject.id,
                    path=self.pds.path)
            allow_more_records = self.pds.max_records_per_subject == (
                -1) or len(records) < self.pds.max_records_per_subject
        except PageNotFound:
            allow_more_records = self.pds.max_records_per_subject != 0
        if not allow_more_records:
            request.META['action'] = 'Maximum number of records created for subject {0}'.format(self.subject.id)
            request.META['error'] = True
            return HttpResponse('Error: The maximum number of records has been created.')
        if request.method == 'GET' and not self.driver.new_record_form_required():
            # Just create the record and redirect (REDCap)
            try:
                label_id = self.request.GET.get('label_id', 1)
                self.record_id = self.create_external_system_record(
                    self.request, self.driver, context['pds'], context['subject'],
                    label=label_id)
                if self.check_cache():
                    self.update_cache()
                self.start_path = '{0}/dataentry/protocoldatasource/{1}/subject/{2}/record/{3}/start/'.format(
                    self.service_client.self_root_path,
                    self.pds.id,
                    self.subject.id,
                    self.record_id)
                return HttpResponseRedirect(self.start_path)
            except RecordCreationError as rce:  # exception from the eHB
                request.META['action'] = rce.errmsg
                request.META['error'] = True
                context['errors'].append((
                    'The record could not be created. Please contact a system'
                    ' administrator. There could be a connection problem.'))
        return super(CreateView, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        context = self.get_context_data(**kwargs)

        def rec_id_validator(new_record_id, include_path):
            return SubjectUtils.validate_new_record_id(
                context['pds'], context['subject'], new_record_id, include_path)

        try:
            grp = SubjectUtils.get_protocol_subject_record_group(
                self.pds.protocol, self.subject)
            grp.client_key = self.pds.protocol._settings_prop(
                'CLIENT_KEY', 'key', '')
            rec_id_prefix = ''

            label_id = request.POST.get('label_id', 1)
            if grp:
                rec_id_prefix = grp.ehb_key
            else:
                request.META['action'] = 'Subject record group not found for {0}'.format(context['subject'].id)
                request.META['error'] = True
                raise Exception('No subject record group found')
            # Try to process the new record form
            try:
                rec_id = self.driver.process_new_record_form(
                    request=request,
                    record_id_prefix=rec_id_prefix,
                    record_id_validator=rec_id_validator
                )
                # If we have successfully created the record. Make sure it is in the eHB.
                try:
                    self.record_id = SubjectUtils.create_new_ehb_external_record(
                        self.pds, request.user, self.subject, rec_id, label_id).id
                    if self.check_cache():
                        self.update_cache()
                    return HttpResponseRedirect(self.start_path)
                except RecordCreationError as rce:  # exception from the eHB
                    request.META['action'] = rce.errmsg
                    request.META['error'] = True
                    context['errors'].append((
                        'The record could not be created on the '
                        'electronic Honest Broker. Please contact a '
                        'system administrator. There could be a '
                        'connection problem.'))
            except IgnoreEhbExceptions as iee:
                # TODO this is a hack until BRP can create Nautilus records
                rec_id = iee.record_id
                ehb_rec_id = ''
                try:
                    # this will create the ehb external_record entry
                    # and add that record to the subject's record group
                    self.record_id = SubjectUtils.create_new_ehb_external_record(
                        self.pds, request.user, self.subject, rec_id, label_id).id

                    if self.check_cache():
                        self.update_cache()
                    self.start_path = '{0}/dataentry/protocoldatasource/{1}/subject/{2}/record/{3}/start/'.format(
                        self.service_client.self_root_path,
                        self.pds.id,
                        self.subject.id,
                        self.record_id)
                    return HttpResponseRedirect(self.start_path)

                except RecordCreationError as rce:  # exception from the eHB
                    request.META['action'] = rce.errmsg
                    request.META['error'] = True
                    record_already_exists = 6
                    cause = rce.raw_cause
                    if cause and len(cause) == 1 and record_already_exists == cause[0]:
                        er_rh = ServiceClient.get_rh_for(
                            record_type=ServiceClient.EXTERNAL_RECORD)
                        ehb_recs = er_rh.get(
                            external_system_url=self.pds.data_source.url, subject_id=self.subject.id, path=self.pds.path)
                        ehb_rec_id = None
                        for record in ehb_recs:
                            if record.record_id == rec_id:
                                ehb_rec_id = record.id
                        if ehb_rec_id:
                            self.start_path = '%s/dataentry/protocoldatasource/%s/subject/%s/record/%s/start' % (
                                ServiceClient.self_root_path,
                                self.pds.id,
                                self.subject.id,
                                ehb_rec_id)
                        else:
                            context['errors'].append(
                                'This ID has already been assigned to another subject.')
                            return render_to_response(
                                'pds_dataentry_rec_create.html',
                                context,
                                context_instance=RequestContext(request)
                            )
                    else:
                        request.META['action'] = 'Record could not be created'
                        request.META['error'] = True
                        context['errors'].append((
                            'The record could not be created on the '
                            'electronic Honest Broker. Please contact '
                            'a system administrator. There could be a'
                            ' connection problem.'))
                except:
                    return HttpResponse('Unknown Error')
                return HttpResponseRedirect(self.start_path)

        except RecordCreationError as rce:
            # Handle errors in the form.
            request.META['action'] = rce.errmsg
            request.META['error'] = True
            context['errors'].append(rce.cause)
            return render_to_response(
                'pds_dataentry_rec_create.html',
                context,
                context_instance=RequestContext(request)
            )
