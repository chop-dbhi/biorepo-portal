# encoding: utf-8
import json
import time

from api.ehb_service_client import ServiceClient
from api.models.protocols import Protocol
from api.serializers import eHBSubjectSerializer
from api.utilities import DriverUtils

from ehb_client.requests.exceptions import PageNotFound

from django.core.management.base import BaseCommand
from django.core.cache import cache

from dataentry.views.pds import StartView
from dataentry.views.base import DataEntryView


from rest_framework.response import Response


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('protocol_id', nargs='+', type=str)

    def getExternalRecords(self, pds, subject, lbls):
        er_rh = ServiceClient.get_rh_for(record_type=ServiceClient.EXTERNAL_RECORD)
        try:
            pds_records = er_rh.get(
                external_system_url=pds.data_source.url, path=pds.path, subject_id=subject)
            time.sleep(0.05)
        except PageNotFound:
            pds_records = []

        r = []
        for ex_rec in pds_records:
            # Convert ehb-client object to JSON and then parse as py dict
            e = json.loads(ex_rec.json_from_identity(ex_rec))
            # Map label descriptions from the eHB to External Records
            for label in lbls:
                if e['label'] == label['id']:
                    if label['label'] == '':
                        e['label_desc'] = 'Record'
                    else:
                        e['label_desc'] = label['label']
            e['pds'] = pds.id
            r.append(e)
        return r

    def get_protocols(self, protocol_id):
        protocol_id = protocol_id[0]
        if protocol_id == 'all':
            protocols = Protocol.objects.all()
        else:
            protocols = Protocol.objects.filter(id=int(protocol_id)).all()
        return protocols

    def get_protocol_subjects (self, protocol, lbls):
        subjects = protocol.getSubjects()
        subject_ids = []
        if subjects:
            subs = [eHBSubjectSerializer(sub).data for sub in subjects]
            for s in subs:
                subject_ids.append(s['id'])
                # self.cache_records(protocol, s['id'], lbls)
        return subject_ids


    def get_protocol_user(self, protocol):
        users = protocol.users.all()
        # find someone on the eig team
        eig_emails = ["felmeistera@email.chop.edu", "gonzalezak@email.chop.edu", "geraces@email.chop.edu", "williamsrm@email.chop.edu", "huangs4@email.chop.edu"]
        for e in eig_emails:
            print (e)
            eig_user = users.values().filter(email=e)
            if eig_user:
                for e_u in eig_user:
                    username = e_u['username']
                    break
                break
        user = users.get(username=username)
        return user

    def get_protocoldatasource (self, protocol):
        protocoldatasources = protocol.getProtocolDataSources()
        # assuming redcap data source is always numbered as 1
        try:
            redcap_pds = protocoldatasources.filter(data_source_id=1)
            for pds in redcap_pds:
                return pds
        except:
            raise

    def get_subject_records (self, pds, s_id, lbls):
        all_records = self.getExternalRecords(pds, s_id, lbls)
        return all_records

    def cache_redcap_form_complete (self, pds, user, cache_key, s_id, r_id, r_name):
        form_url = '/dataentry/protocoldatasource/' + str(pds.id) + '/subject/' + str(s_id) + '/record/' + str(r_id)+ '/form_spec/'
        driver = DriverUtils.getDriverFor(protocol_data_source=pds, user=user)
        sv = StartView()
        form = sv.redcap_form_complete_caching(driver, cache_key, s_id, r_id, form_url, r_name)
        # form = sv.generateSubRecordSelectionForm(driver, record['record_id'], form_url, 0, 1)
        return form

    def handle(self, *args, **options):
        er_label_rh = ServiceClient.get_rh_for(record_type=ServiceClient.EXTERNAL_RECORD_LABEL)
        lbls = er_label_rh.query()
        protocols = self.get_protocols(options['protocol_id'])
        for protocol in protocols:
            # get redcap protocol datasource
            pds = self.get_protocoldatasource(protocol)
            # get eig user in protocol
            user = self.get_protocol_user(protocol)
            # get all subjects in protocol
            subject_id_list = self.get_protocol_subjects(protocol, lbls)

            cache_key = 'protocoldatasource{0}'.format(pds.id) + '_record_table_test5'

            subject_data = {}
            for s_id in subject_id_list:
                # for each subject in protocol, get records
                records = self.get_subject_records(pds,s_id, lbls)
                record_data = {}
                for record in records:
                    r_id = record['id']
                    r_name = record['record_id']
                    self.cache_redcap_form_complete(pds, user, cache_key, s_id, r_id, r_name)


        print("caching records table complete")
