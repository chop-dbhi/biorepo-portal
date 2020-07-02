import logging
import json
import string
import random
from datetime import datetime

from copy import deepcopy

from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist

from .base import BRPApiView
from api.models.protocols import Protocol, ProtocolUserCredentials, DataSource
from api.serializers import OrganizationSerializer, ProtocolSerializer, \
    eHBSubjectSerializer, ProtocolDataSourceSerializer, DataSourceSerializer
from api.utilities import SubjectUtils
from ehb_client.requests.exceptions import PageNotFound
from ehb_client.requests.subject_request_handler import Subject
from ehb_client.requests.subj_fam_relationships_handler import SubjFamRelationship
from ..ehb_service_client import ServiceClient
from rest_framework.response import Response

from rest_framework import viewsets

logger = logging.getLogger(__name__)


class ProtocolViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows protocols to be viewed.
    """
    queryset = Protocol.objects.all()
    serializer_class = ProtocolSerializer

    def list(self, request, *args, **kwargs):
        protocols = []
        for p in Protocol.objects.all():
            if request.user in p.users.all():
                protocols.append(ProtocolSerializer(p, context={'request': request}).data)

        return Response(protocols)


class ProtocolAllViewSet(BRPApiView):
    """
    API endpoint that allows all protocols to be viewed.
    """
    def get(self, request, *args, **kwargs):
        protocols = []
        if request.user.is_superuser:
            protocols = Protocol.objects.values('id', 'name')
        return Response(protocols)


class ProtocolDataSourceView(BRPApiView):
    def get(self, request, pk, *args, **kwargs):
        """
        Returns a list of protocol datasources associated with this protocol

        Also determines authorization for each protocol datasource based on
        the user making the request.
        """
        try:
            p = Protocol.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'error': 'Protocol requested not found'}, status=404)

        ds = []

        for pds in p.getProtocolDataSources():
            t = ProtocolDataSourceSerializer(pds, context={'request': request}).data
            # Parse ProtocolDataSource configuration
            if pds.driver_configuration != '':
                dc = json.loads(pds.driver_configuration)
            else:
                dc = {}
            # If labels are defined get label names from eHB.
            # (label_id, label_description)
            if 'labels' in list(dc.keys()):
                labels = cache.get('ehb_labels')
                if not labels:
                    labels = self.erl_rh.query()
                    cache.set('ehb_labels', labels)
                    if hasattr(cache, 'ttl'):
                        cache.ttl('ehb_labels', 60)
                nl = []
                for l in dc['labels']:
                    for label in labels:
                        if l == label['id']:
                            if label['label'] == '':
                                nl.append((label['id'], 'Record'))
                            else:
                                nl.append((label['id'], label['label']))
                dc['labels'] = nl
            else:
                dc['labels'] = [(1, 'Record')]

            t["driver_configuration"] = dc
            # Determine Authorization
            try:
                ProtocolUserCredentials.objects.get(
                    protocol=p, data_source=pds, user=request.user)
                t["authorized"] = True
            except ProtocolUserCredentials.DoesNotExist:
                t["authorized"] = False
            # Include DataSource details
            t["data_source"] = DataSourceSerializer(pds.data_source).data

            ds.append(t)

        return Response(sorted(
            ds, key=lambda ds: ds["display_label"]))


class ProtocolOrganizationView(BRPApiView):
    def get(self, request, pk, *args, **kwargs):
        """
        Provide a list of organizations associated with a protocol
        """
        try:
            p = Protocol.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'error': 'Protocol requested not found'}, status=404)

        if p.isUserAuthorized(request.user):
            q = p.organizations.all()
            orgs = [OrganizationSerializer(org.getEhbServiceInstance()).data for org in q]
        return Response(
            orgs,
            headers={'Access-Control-Allow-Origin': '*'}
        )


class ProtocolSubjectsView(BRPApiView):
    def get(self, request, pk, *args, **kwargs):
        """
        Returns a list of subjects associated with a protocol.
        """
        try:
            p = Protocol.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'error': 'Protocol requested not found'}, status=404)
        if p.isUserAuthorized(request.user):
            # Check cache
            cache_data = cache.get('protocol{0}_sub_data'.format(p.id))
            if cache_data:
                # if all subjects have a modified date in cache then sort using modified date
                try:
                    subs = sorted(json.loads(cache_data), key=lambda i: datetime.strptime(i['modified'], '%Y-%m-%dT%H:%M:%S.%f'), reverse=True)
                # if some subjects do not have modified date then sort by PK
                except:
                    logger.info('subjects sorted by primary key for protocol {protocol}'.format(protocol=p.id))
                    subs = sorted(json.loads(cache_data), key=lambda i: (i['id'], '%Y-%m-%dT%H:%M:%S.%f'), reverse=True)
                return Response(
                    subs,
                    headers={'Access-Control-Allow-Origin': '*'}
                )
            else:
                subjects = p.getSubjects()
                organizations = p.organizations.all()
                if subjects:
                    subs = [eHBSubjectSerializer(sub).data for sub in subjects]
                else:
                    return Response([])
                ehb_orgs = []
                # We can't rely on Ids being consistent across apps so we must
                # append the name here for display downstream.
                for o in organizations:
                    ehb_orgs.append(o.getEhbServiceInstance())
                # Check if the protocol has external IDs configured. If so retrieve them
                manageExternalIDs = False

                protocoldatasources = p.getProtocolDataSources()

                for pds in protocoldatasources:
                    if pds.driver == 3:
                        ExIdSource = pds
                        manageExternalIDs = True

                if manageExternalIDs:
                    try:
                        config = json.loads(ExIdSource.driver_configuration)
                        if 'sort_on' in list(config.keys()):
                            # er_label_rh = ServiceClient.get_rh_for(record_type=ServiceClient.EXTERNAL_RECORD_LABEL)
                            # lbl = er_label_rh.get(id=config['sort_on'])
                            lbl = ''
                            addl_id_column = lbl
                    except:
                        pass

                for sub in subs:
                    sub['external_records'] = []
                    sub['external_ids'] = []
                    sub['organization'] = sub['organization_id']
                    sub['organization_id_label'] = sub['organization_id_label']
                    sub.pop('organization_id')
                    for pds in protocoldatasources:
                        sub['external_records'].extend(pds.getSubjectExternalRecords(sub))
                    if manageExternalIDs:
                        # Break out external ids into a separate object for ease of use
                        for record in sub['external_records']:
                            if record['external_system'] == 3:
                                sub['external_ids'].append(record)
                    for ehb_org in ehb_orgs:
                        if sub['organization'] == ehb_org.id:
                            sub['organization_name'] = ehb_org.name
        else:
            return Response(
                {"detail": "You are not authorized to view subjects in this protocol"},
                status=403
            )

        if subjects:
            return Response(
                subs,
                headers={'Access-Control-Allow-Origin': '*'}
            )

        return Response([])


class ProtocolSubjectDetailView(BRPApiView):
    def edit_subject_user_audit(self, new_subject, old_subject, payload):
        # check what subject elements have changed: first name, last name, DOB, organization, organization ID
        final_payload = []

        if (new_subject['first_name'] != old_subject['first_name']):
            payload['change_field'] = "first_name"
            payload['old_value'] = old_subject['first_name']
            payload['new_value'] = new_subject['first_name']
            final_payload.append(payload.copy())

        if (new_subject['last_name'] != old_subject['last_name']):
            payload['change_field'] = "last_name"
            payload['old_value'] = old_subject['last_name']
            payload['new_value'] = new_subject['last_name']
            final_payload.append(payload.copy())

        if (new_subject['organization_subject_id'] != old_subject['organization_subject_id']):
            payload['change_field'] = "organization_subject_id"
            payload['old_value'] = old_subject['organization_subject_id']
            payload['new_value'] = new_subject['organization_subject_id']
            final_payload.append(payload.copy())

        if (new_subject['organization'] != old_subject['organization']):
            payload['change_field'] = "organization"
            payload['old_value'] = old_subject['organization']
            payload['new_value'] = new_subject['organization']
            final_payload.append(payload.copy())

        if (datetime.strptime(new_subject['dob'], '%Y-%m-%d') != datetime.strptime(old_subject['dob'], '%Y-%m-%d')):
            payload['change_field'] = "dob"
            payload['old_value'] = old_subject['dob']
            payload['new_value'] = new_subject['dob']
            final_payload.append(payload.copy())

        if (final_payload != []):
            ServiceClient.user_audit(final_payload)

    def post(self, request, pk, *args, **kwargs):
        '''
        Add a subject to the protocol

        Expects a request body of the form:
        {
            "last_name": "John",
            "last_name": "Doe",
            "organization_subject_id": "123123123",
            "organization": "1",
            "dob": "2000-01-01"
        }
        '''
        try:
            protocol = Protocol.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'error': 'Protocol requested not found'}, status=404)
        subject = request.data
        new_subject = Subject(
            first_name=subject['first_name'],
            last_name=subject['last_name'],
            organization_id=int(subject['organization']),
            organization_subject_id=subject['organization_subject_id'],
            dob=datetime.strptime(subject['dob'], '%Y-%m-%d')
        )
        try:
            org = self.o_rh.get(id=subject['organization'])
        except:
            return Response({'error': 'Invalid Organization Selected'}, status=400)
        errors = []
        try:
            subject = self.s_rh.get(
                organization_id=new_subject.organization_id,
                organization_subject_id=new_subject.organization_subject_id)
            success = True
            # If found this indicates the subject is already in the ehb for
            # this organization, but not necessarily for this protocol.
            # That will be checked below in the external record search
            prefix = "A subject with this " + org.subject_id_label + " exists but with "
            if subject.first_name != new_subject.first_name:
                success = False
                errors.append(prefix + "first name: " + subject.first_name)
            if subject.last_name != new_subject.last_name:
                success = False
                errors.append(prefix + "last name: " + subject.last_name)
            if subject.dob != new_subject.dob.date():
                success = False
                errors.append(prefix + "birth date: " + str(subject.dob))
        except PageNotFound:
            # Subject is not in the system so create it
            r = self.s_rh.create(new_subject)[0]
            success = r.get('success')
            errors = r.get('errors')
            subject = r.get(Subject.identityLabel)
        # Dont proceed if creation was not a success
        if not success:
            subject = json.loads(Subject.json_from_identity(subject))
            return Response([success, subject, errors], status=422)

        if not errors:
            errors = []
            # Add this subject to the protocol and create external record group
            if self.subject_utils.create_protocol_subject_record_group(protocol, new_subject):
                if protocol.addSubject(subject):
                    success = True
                    # add this action to the user audit
                    user_audit_payload = [{
                        'subject': subject.id,
                        'change_type': "SubjectGroup",
                        'change_type_ehb_pk': protocol._subject_group().id,
                        'change_action': "Add",
                        'user_name': request.user.username,
                        'protocol_id': protocol.id
                    }]
                    ServiceClient.user_audit(user_audit_payload)
                else:
                    # Could not add subject to project
                    errors.append(
                        'Failed to complete eHB transactions. Could not add subject to project. Please try again.')
                    success = False
            else:
                # For some reason we couldn't get the eHB to add the subject to the protocol group
                subjects = protocol.getSubjects()
                if subjects and subject in subjects:
                    # Subject is already in protocol
                    errors.append(
                        'This subject ' + org.subject_id_label +
                        ' has already been added to this project.'
                    )
                    logger.error("Could not add subject. They already exist on this protocol.")
                    success = False
                else:
                    errors.append(
                        'Failed to complete eHB transactions. Could not add subject to project. Please try again.')
                    success = False
        subject = json.loads(Subject.json_from_identity(subject))
        subject['organization_name'] = org.name

        if not success:
            return Response(
                [success, subject, errors],
                headers={'Access-Control-Allow-Origin': '*'},
                status=400
            )
        # Add subject to cache
        self.update_subject_cache(protocol.id, subject, True)
        return Response(
            [success, subject, errors],
            headers={'Access-Control-Allow-Origin': '*'},
            status=200
        )

    def get(self, request, pk, subject, *args, **kwargs):
        ''' get all subject data:
        external records, Organization, external ids and relationships'''
        # TODO: add getting relationships for subjects here
        try:
            p = Protocol.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'error': 'Protocol requested not found'}, status=404)

        if p.isUserAuthorized(request.user):
            protocoldatasources = p.getProtocolDataSources()
            manageExternalIDs = False
            for pds in protocoldatasources:
                if pds.driver == 3:
                    ExIdSource = pds
                    manageExternalIDs = True
            try:
                subject = self.s_rh.get(id=subject)
                organization = self.o_rh.get(id=subject.organization_id)
            except:
                return Response({'error': 'Subject not found'}, status=404)
            sub = json.loads(Subject.json_from_identity(subject))
            sub['organization_name'] = organization.name
            sub['external_records'] = []
            for pds in protocoldatasources:
                sub['external_records'].extend(pds.getSubjectExternalRecords(sub))
            if manageExternalIDs:
                # Break out external ids into a separate object for ease of use
                sub['external_ids'] = []
                for record in sub['external_records']:
                    if record['external_system'] == 3:
                        sub['external_ids'].append(record)
            return Response(sub)
        else:
            return Response(
                {"detail": "You are not authorized to view subjects in this protocol"},
                status=403
            )

    def put(self, request, pk, subject, *args, **kwargs):
        subject_update = json.loads(request.body.decode('utf-8'))
        subject_api_url = "/api/subject/id/" + subject + "/"
        # See if subject exists
        try:
            ehb_sub = ServiceClient.ehb_api(subject_api_url, "GET").json()
            protocol = Protocol.objects.get(pk=pk)
            old_group_name = SubjectUtils.protocol_subject_record_group_name(protocol, ehb_sub)
            group = self.g_rh.get(name=old_group_name)
        except:
            return Response({'error': 'subject not found'}, status=404)

        update_subject_response = self.updateEhbSubject(subject, subject_update, ehb_sub)
        try:
            success = update_subject_response['success']
        except:
            success = (update_subject_response.status_code == 200)

        if (success is False):
            return Response(json.dumps({'error': 'Unable to update subject'}), status=400)
        user_audit_payload = {
            'subject': ehb_sub['id'],
            'change_type': "Subject",
            'change_type_ehb_pk': ehb_sub['id'],
            'change_action': "Update",
            'user_name': request.user.username,
            'protocol_id': protocol.id
        }
        self.edit_subject_user_audit(subject_update, ehb_sub, user_audit_payload)
        # If the update is succesful, update the subject record group associated with this subject
        update_subj_gr_resp = self.update_subject_group(protocol, subject_update, group)
        if not update_subj_gr_resp['success']:
            return Response(json.dumps({'error': 'Unable to update group'}), status=400)

        # If the update is succesful, update the cache.
        try:
            self.update_subject_cache(pk, subject_update, False)
        except:
            return Response(json.dumps({'error': 'Unable to update cache'}), status=400)

        return Response(
            subject_update,
            headers={'Access-Control-Allow-Origin': '*'}
        )

    def delete(self, request, pk, subject, *args, **kwargs):
        if request.user.is_superuser:
            try:
                subject = self.s_rh.get(id=subject)
                protocol = Protocol.objects.get(pk=pk)
                group_id = self.get_group_id(protocol.immutable_key.key)
                # instead of deleting a subject - we want to just remove them from the subject group
                # self.s_rh.delete(id=subject.id)
                self.remove_sub_from_ehb_group(subject.id, group_id)
                SubjectUtils.delete_protocol_subject_record_group(protocol, subject)
            except:
                return Response({'error': 'Unable to delete subject'}, status=400)

            return Response({'info': 'Subject deleted'}, status=200)
        else:
            return Response(
                {"detail": "You are not authorized to view subjects in this protocol"},
                status=403
            )

    @staticmethod
    def get_group_id(key):
        get_group_url = '/api/group/?name=' +'BRP:' + key
        group = ServiceClient.ehb_api(get_group_url, "GET").json()
        return group['id']

    @staticmethod
    def remove_sub_from_ehb_group(sub_pk, group_pk):
        url = '/api/group/id/' + str(group_pk) + '/subjects/id/' + str(sub_pk) + '/'
        return ServiceClient.ehb_api(url, "DELETE")

    @staticmethod
    def updateEhbSubject(subjectID, new_subject, old_subject):
        subject_update_api_url = "/api/subject/"
        ehb_update_subj = {}

        ehb_update_subj["id"] = subjectID
        ehb_update_subj["old_subject"] = deepcopy(old_subject)
        ehb_update_subj["new_subject"] = deepcopy(new_subject)
        ehb_update_subj_body = '[' + str(json.dumps(deepcopy(ehb_update_subj))) + ']'
        return ServiceClient.ehb_api(subject_update_api_url, "PUT", json.loads(ehb_update_subj_body))

    @classmethod
    def update_subject_group(cls, protocol, subject_update, group):
        new_group_name = SubjectUtils.protocol_subject_record_group_name(protocol, subject_update)
        group.name = new_group_name
        group.client_key = protocol._settings_prop(
            'CLIENT_KEY', 'key', '')
        group.current_client_key(group.client_key)
        return cls.g_rh.update(group)[0]

    @classmethod
    def update_subject_cache(cls, protocol_pk, subject_update, new_subject):
        cache_key = 'protocol{0}_sub_data'.format(protocol_pk)
        cache_data = cls.cache.get(cache_key)
        if cache_data:
            subjects = json.loads(cache_data)
            if new_subject:
                subject_update['external_ids'] = []
                subject_update['external_records'] = []
                subjects.append(subject_update)
            else:
                for i in range(0, len(subjects)):
                    if subjects[i]['id'] == subject_update['id']:
                        subjects[i] = subject_update
            cls.cache.set(cache_key, json.dumps(subjects))
            if hasattr(cls.cache, 'persist'):
                cls.cache.persist(cache_key)


class ProtocolSubjFamDetailView(BRPApiView):

    def update_relationship_user_audit(self, new_value, old_value, field, **change):
        if (new_value != old_value):
            change['change_field'] = field
            change['old_value'] = old_value
            change['new_value'] = new_value
            self.user_audit_relationship(change)

    def user_audit_relationship(self, change):
        ''' pass in a dictionary with the following elements:
        subject_1, subject_2 (not required), change_type, change_type_ehb_pk,
        change_action, user_name, protocol_id, change_field '''

        user_audit_payload1 = []
        user_audit_payload2 = []

        subject_1 = change.pop('subject_1')
        subject_2 = change.pop('subject_2')

        change['subject'] = subject_1
        user_audit_payload1.append(change.copy())
        ServiceClient.user_audit(user_audit_payload1)
        # if there is a subject_2 send second request
        if subject_2:
            change['subject'] = subject_2
            user_audit_payload2.append(change.copy())
            ServiceClient.user_audit(user_audit_payload2)

    # will return True if subject inputs are valid
    def check_subject(self, subject_1, subject_2=None):
        try:
            subject_1_response = self.s_rh.get(id=subject_1)
            if subject_2:
                subject_2_response = self.s_rh.get(id=subject_2)
        except:
            return {'error': 'Invalid subject Selected'}

        sub1 = json.loads(Subject.json_from_identity(subject_1_response))
        if subject_2:
            sub2 = json.loads(Subject.json_from_identity(subject_2_response))
        if sub1['id'] is None:
            return {'error': 'Invalid subject Selected'}
        if subject_2 is not None and sub2['id'] is None:
            return {'error': 'Invalid subject Selected'}
        return True

    # will return true if request body is valid, otherwise will return error
    def validate_req_body(self, relationship):
        try:
            subject_1_id = relationship['subject_1']
        except:
            return {'error': 'missing subject_1 from request'}

        try:
            subject_2_id = relationship['subject_2']
        except:
            return {'error': 'missing subject_2 from request'}

        try:
            relationship['subject_1_role']
        except:
            return {'error': 'missing subject_1_role from request'}

        try:
            relationship['subject_2_role']
        except:
            return {'error': 'missing subject_2 from request'}

        valid_subjects = self.check_subject(subject_1_id, subject_2_id)
        if valid_subjects is not True:
            return (valid_subjects)

        return True

    def post(self, request, pk,):
        '''
        Add a subject relationship to the protocol

        Expects a request body of the form:
        {
            "subject_1": 1,
            "subject_2": 2,
            "subject_1_role": 3,
            "subject_2_role": 4,
            "protocol_id": 1
        }
        '''
        relationship = request.data
        req_body_valid = self.validate_req_body(relationship)
        if req_body_valid is not True:
            return Response(req_body_valid, status=400)

        try:
            new_relationship = SubjFamRelationship(
                subject_1_id=relationship['subject_1'],
                subject_2_id=relationship['subject_2'],
                subject_1_role=relationship['subject_1_role'],
                subject_2_role=relationship['subject_2_role'],
                protocol_id=relationship['protocol_id']
            )
        except:
            return Response({'error': 'Invalid subject or subject role Selected'}, status=400)

        r = self.relationship_HB_handler.create(new_relationship)[0]
        success = r.get('success')
        errors = r.get('errors')
        relationship = r.get(SubjFamRelationship.identityLabel)

        # Dont proceed if creation was not a success
        if not success:
            try:
                relationship = json.loads(SubjFamRelationship.json_from_identity(relationship))
            except:
                pass  # because either way we are replying with error info
            return Response(
                [{"success": success, "relationship": relationship, "errors": errors}],
                status=422)

        change = {
            'subject_1': r['subjFamRelationship'].subject_1_id,
            'subject_2': r['subjFamRelationship'].subject_2_id,
            'change_type': "SubjectFamRelation",
            'change_type_ehb_pk': r['subjFamRelationship'].id,
            'change_action': "Create",
            'user_name': request.user.username,
            'protocol_id': r['subjFamRelationship'].protocol_id
        }
        self.user_audit_relationship(change)

        return Response(
            [{"success": success, "relationship": json.loads(SubjFamRelationship.json_from_identity(new_relationship)), "errors": errors}],
            headers={'Access-Control-Allow-Origin': '*'},
            status=200
        )

    def get(self, request, pk, subject=None, relationship_id=None):
        ''' returns list of relationships unless relationship_id is passed in.
            in that case, a single relationship will be returned.'''
        try:
            p = Protocol.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'error': 'Protocol requested not found'}, status=404)
        # TODO: when cache added - check for cache data handleRecordClick
        if p.isUserAuthorized(request.user):
            # if subject is not None, then collect all relationships for given subject
            if subject:
                valid_subject = self.check_subject(subject)
                if valid_subject is True:
                    r = self.relationship_HB_handler.get(subject_id=subject)
                    r = SubjFamRelationship.json_from_identity(r)
                else:
                    return Response(valid_subject, status=400)
            # get relationship by relationship id
            elif relationship_id:
                try:
                    r = self.relationship_HB_handler.get(relationship_id=relationship_id)
                except ObjectDoesNotExist:
                    return Response({'error': 'relationship requested not found'}, status=404)
            # get all relationships in the protocol
            else:
                r = self.relationship_HB_handler.get(protocol_id=pk)

            r = json.loads(r)
            return Response(
                {"relationships": r},
                status=200
            )

        else:
            return Response(
                {"detail": "You are not authorized to view subjects in this protocol"},
                status=403
            )

    def delete(self, request, pk, relationship_id):
        '''
        Delete a subject relationship in the protocol

        Expects a request body of the form:
        {
            "subject_1": 1,
            "subject_2": 2,
            "subject_1_role": 3,
            "subject_2_role": 4,
            "protocol_id": 1,
            "id": 1
        }
        '''
        try:
            p = Protocol.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'error': 'Protocol requested not found'}, status=404)
        if p.isUserAuthorized(request.user):
            relationship = request.data
            req_body_valid = self.validate_req_body(relationship)
            if req_body_valid is not True:
                return Response(req_body_valid, status=400)
            try:
                self.relationship_HB_handler.delete(relationship_id=relationship_id)
            except:
                return Response({'error': 'Unable to delete relationship'}, status=400)

            # Send delete information to the user audit log
            relationship['change_type'] = "SubjectFamRelation"
            relationship['user_name'] = request.user.username
            relationship['change_type_ehb_pk'] = relationship_id
            relationship['change_action'] = "Delete"

            self.user_audit_relationship(relationship)

            return Response({'info': 'Relationship deleted'}, status=200)
        else:

            return Response(
                {"detail": "You are not authorized to view subjects in this protocol"},
                status=403
            )

    def put(self, request, pk, relationship_id):
        '''
        updates a subject relationship in the protocol

        Expects a request body of the form:
        {
            "subject_1": 1,
            "subject_2": 2,
            "subject_1_role": 3,
            "subject_2_role": 4,
            "protocol_id": 1,
            "id": 1
        }
        '''
        # todo authorize user
        try:
            updated_relationship = request.data
            old_relationship = json.loads(self.relationship_HB_handler.get(relationship_id=relationship_id))

        except ObjectDoesNotExist:
            return Response({'error': 'relationship requested not found'}, status=404)
        try:
            self.relationship_HB_handler.update(relationship_id, updated_relationship)

        except:
            return Response({'error': 'Unable to update relationship'}, status=400)

        # update User audit log if update was a success
        try:
            # check each element in updated and old relationships to identify Changes
            relationship_change = {}
            relationship_change["subject_1"] = updated_relationship['subject_1']
            relationship_change["subject_2"] = updated_relationship['subject_2']
            relationship_change["change_type"] = "SubjectFamRelation"
            relationship_change["change_type_ehb_pk"] = relationship_id
            relationship_change["change_action"] = "Update"
            relationship_change["user_name"] = request.user.username
            relationship_change["protocol_id"] = pk

            self.update_relationship_user_audit(int(updated_relationship['subject_1']), int(old_relationship['subject_1']['id']), "subject_1", **relationship_change)
            self.update_relationship_user_audit(int(updated_relationship['subject_1_role']), int(old_relationship['subject_1_role']['id']), "subject_1_role", **relationship_change)
            self.update_relationship_user_audit(int(updated_relationship['subject_2']), int(old_relationship['subject_2']['id']), "subject_2", **relationship_change)
            self.update_relationship_user_audit(int(updated_relationship['subject_2_role']), int(old_relationship['subject_2_role']['id']), "subject_2_role", **relationship_change)

        except:
            logger.info('error updating relationship id {0}'.format(relationship_id))

        return Response({'updatedRelationship': updated_relationship, 'oldRelationship': old_relationship}, status=200)


class ProtocolSubjectIdView(BRPApiView):
    """
    API endpoint that allows creation of Id to be used as de-identifiers in
    external datasets and external applications not directly connected to the BRP.
    """
    def get(self, request, protocol_pk, datasource_pk):
        try:
            datasource = DataSource.objects.get(pk=datasource_pk)
            protocol = Protocol.objects.get(pk=protocol_pk)
        except:
            return Response('datasource or protocol does not exist in the BRP', status=404)

        print("datasource: {}".format(datasource.id))
        # check to make sure that protocol name is somewhere in the datasource description
        if not (protocol.name in str(datasource.description)):
            return Response('protocol name is not in the datasource description', status=400)

        # Check to make sure user is authorized for this protocol
        if not protocol.isUserAuthorized(request.user):
            return Response('user is not authorized for this protocol', status=403)

        eHB_ex_sys_pk, msg, status = self.get_ehb_external_system(datasource.name)
        if status is not 200:
            return Response(msg, status=status)

        # get all subjects in the protocol
        subjects_protocol, msg, status = self.get_protocol_subjects(protocol)
        if status is not 200:
            return Response(msg, status=status)

        # get all subjects in DataSource
        subjects_datasource, msg, status = self.get_datasource_subjects(datasource)
        if status is not 200:
            return Response(msg, status=status)

        # get list of subjects that need to be added to the eHB datasource
        subs_to_be_added, msg, status = self.check_all_sub_in_datasource(subjects_protocol, subjects_datasource)
        if status is not 200:
            return Response(msg, status=status)


        # add subjects to the eHB DataSource
        msg, status = self.add_subs_to_datasource(subs_to_be_added, subjects_datasource, datasource)
        if status is not 200:
            return Response(msg, status=status)

        print(subs_to_be_added)
        return Response('response', status=200)

    def get_ehb_external_system(self, brp_external_sys_name):
        msg = ' '
        status_code = 200
        ehb_ex_sys_pk = None
        success = True
        api_url = '/api/externalsystem/query/'
        payload = [{"name": brp_external_sys_name}]
        # payload = json.loads(payload)
        # print(brp_external_sys_name)
        # ehb_response = ServiceClient.ehb_api(api_url, "POST", payload)
        # print(ehb_response.text)
        try:
            ehb_response = ServiceClient.ehb_api(api_url, "POST", payload)
            print(ehb_response)
            ehb_ex_sys_json = ehb_response.json()
            ehb_ex_sys_pk = ehb_ex_sys_json[0]['externalSystem']['id']
        except:
            success = False
        # print("ehb_ex_sys_pk: {}".format(ehb_ex_sys_pk[0]['externalSystem']['id']))
        if (not success) or (ehb_response.status_code is not 200):
            msg = 'cannot retreive external system from the eHB'
            status_code = 400

        return ehb_ex_sys_pk, msg, status_code

    def add_subs_to_datasource(self, subs, datasource_subs, datasource, label=1):
        msg = ' '
        status_code = 200
        print("datasource external system: {}".format(datasource.getExternalSystem().id))
        for sub in subs:
            print("we are hitting multiple subs")
            print(sub)
            # generate a new ID for this subject
            new_id = self.generate_unique_random_id(datasource_subs)
            print("new_id: {}".format(new_id))
            ehb_response = self.add_subject_to_eHB_datasource(sub, datasource, new_id, label)
            print(ehb_response)
        try:
            for sub in subs:
                print("we are hitting multiple subs")
                print(sub)
                # generate a new ID for this subject
                new_id = self.generate_unique_random_id(datasource_subs)
                print("new_id: {}".format(new_id))
                ehb_response = self.add_subject_to_eHB_datasource(sub, datasource, new_id, label)
                print(ehb_response)
        except:
            # print("we could not add subjects to ehb")
            # return Response('error adding subjects to the eHB datasource', status=300)
            msg = 'error adding subjects to the eHB datasource'
            status_code = 300
        return msg, status_code

    @staticmethod
    def get_protocol_subjects(protocol):
        msg = ' '
        status_code = 200
        subjects_protocol = None
        try:
            subjects_protocol_obj = protocol.getSubjects()
            if subjects_protocol_obj:
                subjects_protocol = [eHBSubjectSerializer(sub).data for sub in subjects_protocol_obj]
            else:
                subjects_protocol = None
        except:
            # return Response('there are no subjects aligned to this protocol', status=200)
            msg = 'there are no subjects aligned to this protocol'
            status_code = 204
        if (subjects_protocol is None):
            # return Response('there are no subjects aligned to this protocol', status=200)
            msg = 'there are no subjects aligned to this protocol'
            status_code = 204

        return subjects_protocol, msg, status_code
        # return subjects_protocol

    def check_all_sub_in_datasource(self, protocol_subs, datasource_subs):
        """
        This function will identify subjects that need to be added to the eHB
        DataSource
        """
        msg = ' '
        status_code = 200
        # print('protocol_subs: {}'.format(protocol_subs))
        print('protocol_subs count: {}'.format(len(protocol_subs)))
        subs_to_be_added = []
        print('datasource subs: {}'.format(datasource_subs))
        for subject in protocol_subs:
            subs_to_be_added.append(subject['id'])
            # print(subject['organization_subject_id'])
            # if(str(subject['organization_subject_id']) not in datasource_subs):
            #     # generate a new ID for this subject
            #     new_id = self.generate_unique_random_id(datasource_subs)

                # TODO add subject to eHB datasource
                # ehb_response = self.add_subject_to_eHB_datasource(sub['id'], ex_system_pk, sub_record_id, path, label=1)
                # get a fresh list of subjects in the datasource
                # datasource_subs = self.get_datasource_subjects()
        # if (datasource_subs is not None) and (datasource_subs.status_code == 200):
        #     print('datasource_subs count: {}'.format(len(datasource_subs)))
        return subs_to_be_added, msg, status_code

    def add_subject_to_eHB_datasource(self, sub_pk, datasource, sub_record_id, label=1):
        print("we are in add_subject_to_eHB_datasource")
        # todo make API call to add subject to eHN DataSource
        ehb_api_url = '/api/externalrecord/'
        # print("datasource external system: {}".format(datasource.getExternalSystem()))
        print("we are about to make payload")
        print("sub_pk: {}".format(sub_pk))
        print("datasource id: {}".format(str(datasource.getExternalSystem().id)))
        print("path: {}".format(datasource.url))
        print("label: {}".format(label))
        payload = [{
            'subject': str(sub_pk),
            'external_system': str(datasource.getExternalSystem().id),
            'record_id': sub_record_id,
            'path': datasource.url,
            'label': label
        }]
        print("after making payload")
        print("payload: {}".format(payload))
        ehb_response = ServiceClient.ehb_api(ehb_api_url, "POST", payload)
        print(ehb_response)
        return ehb_response

    @staticmethod
    def get_datasource_subjects(datasource):
        msg = ' '
        status_code = 200
        subjects = []
        # subjects = datasource.getSubjects()
        try:
            class_subjects = datasource.getSubjects()
            for sub in class_subjects:
                print("datasource subjects: {}".format(sub.organization_subject_id))
                subjects.append(sub.organization_subject_id)
        except:
            msg = 'there was an error getting subjects aligned to datasource'
            status_code = 400
            # subjects = None
            # return msg, status_code
            # return Response('there was an error getting subjects aligned to datasource', status=400)
        # print("subjects: {}".format(subjects))
        return subjects, msg, status_code

    @staticmethod
    def generate_random_id():
        seed = 493827561
        length = 10
        chars = string.ascii_uppercase + string.digits
        random.seed(random.randrange(0, seed))
        return ''.join(random.choice(chars) for idx in range(length))

    def generate_unique_random_id(self, exisiting_ids):
        success = False
        while not success:
            new_id = self.generate_random_id()
            print("new_id in generate unique random id: {}".format(new_id))
            if (exisiting_ids is None) or (new_id not in exisiting_ids):
                success = True
                print("success")
        return new_id
