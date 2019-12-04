import logging

from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView

from api.ehb_service_client import ServiceClient
from api.utilities import DriverUtils
from api.models.protocols import ProtocolDataSource

log = logging.getLogger(__name__)


class DataEntryView(TemplateView):

    service_client = ServiceClient
    org = None
    pds = None
    record = None
    record_id = None
    subject = None
    start_path = ''
    create_path = ''

    def get_external_record(self, **kwargs):
        record_id = kwargs.get('record_id', None)
        if record_id:
            try:
                rh = self.service_client.get_rh_for(
                    record_type=ServiceClient.EXTERNAL_RECORD)
                return rh.get(id=record_id)
            except:
                log.error('Unable to retrieve record from eHB')
                return
        return

    def get_label(self, context):

        if context['record']:
            label_id = context['record'].label_id
        else:
            label_id = context['label_id']
        try:
            label = self.service_client.get_rh_for(
                record_type=ServiceClient.EXTERNAL_RECORD_LABEL).get(id=label_id)
            return label
        except:
            return

    def get_context_data(self, **kwargs):
        subject_api_url = "/api/subject/id/" + kwargs['subject_id'] + "/"
        context = super(DataEntryView, self).get_context_data(**kwargs)
        
        self.pds = get_object_or_404(ProtocolDataSource, pk=kwargs['pds_id'])
        self.subject = ServiceClient.ehb_api(subject_api_url, "GET").json()
        self.record = self.get_external_record(**kwargs)
        self.org = self.service_client.get_rh_for(
            record_type=ServiceClient.ORGANIZATION).get(id=self.subject['organization'])
        self.driver = DriverUtils.getDriverFor(
            protocol_data_source=self.pds, user=self.request.user)
        if self.record:
            self.start_path = '{0}/dataentry/protocoldatasource/{1}/subject/{2}/record/{3}/start/'.format(
                self.service_client.self_root_path,
                self.pds.id,
                kwargs['subject_id'],
                self.record.id)
        self.create_path = '{0}/dataentry/protocoldatasource/{1}/subject/{2}/create/'.format(
            self.service_client.self_root_path,
            self.pds.id,
            kwargs['subject_id'])
        context = {
            'protocol': self.pds.protocol,
            'organization': self.org,
            'subject': self.subject,
            'root_path': self.service_client.self_root_path,
            'pds': self.pds,
            'request': self.request,
            'record': self.record,
            'errors': []
        }
        if not context['record']:
            context['label_id'] = self.request.GET.get('label_id', 1)
        context['label'] = self.get_label(context)
        return context
