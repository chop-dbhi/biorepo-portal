# encoding: utf-8
import json
import time
import threading

from api.ehb_service_client import ServiceClient
from api.models.protocols import Protocol
from api.serializers import eHBSubjectSerializer
from api.utilities import DriverUtils

from ehb_client.requests.exceptions import PageNotFound

from django.core.management.base import BaseCommand
from django.core.cache import cache

from dataentry.views.pds import StartView


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('protocol_id', nargs='+', type=str)

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
        return subject_ids

    def get_protocol_user(self, protocol):
        users = protocol.users.all()
        # find someone on the eig team
        eig_emails = ["gonzalezak@email.chop.edu", "felmeistera@email.chop.edu", "krausee@email.chop.edu", "geraces@email.chop.edu", "williamsrm@email.chop.edu", "huangs4@email.chop.edu"]
        for e in eig_emails:
            eig_user = users.values().filter(email=e)
            if eig_user:
                for e_u in eig_user:
                    username = e_u['username']
                    break
                break
        user = users.get(username=username)
        return user

    def get_protocoldatasource(self, protocol):
        try:
            protocoldatasources = protocol.getProtocolDataSources()
            # the driver RedCAP Client is indexed at 0
            redcap_pds = protocoldatasources.filter(driver=0)
            return redcap_pds
        except:
            print ("Unable to find protocoldatasource")

    def get_subject_records(self, pds, subject, lbls):
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

    def cache_redcap_form_complete(self, pds, user, cache_key, s_id, r_id, r_name):
        try:
            form_url = '/dataentry/protocoldatasource/' + str(pds.id) + '/subject/' + str(s_id) + '/record/' + str(r_id)+ '/form_spec/'
            # create redcap driver
            driver = DriverUtils.getDriverFor(protocol_data_source=pds, user=user)
            # instantiate an instance of the Class StartView in pds.py
            sv = StartView()
            # call the method to cache redcap completion codes
            form = sv.redcap_form_complete_caching(driver, cache_key, s_id, r_id, r_name)
            return form
        except:
            print ("error in caching redcap tables")

    def handle(self, *args, **options):

        def subject_threading(self, pds, s_id, lbls, user, cache_key):
            # get all records associated with subject
            records = self.get_subject_records(pds,s_id, lbls)
            for record in records:
                r_id = record['id']
                r_name = record['record_id']
                self.cache_redcap_form_complete(pds, user, cache_key, s_id, r_id, r_name)
            return

        def clear_cache(cache_key):
            cache.delete(cache_key)

        start = time.time()
        er_label_rh = ServiceClient.get_rh_for(record_type=ServiceClient.EXTERNAL_RECORD_LABEL)
        lbls = er_label_rh.query()
        protocols = self.get_protocols(options['protocol_id'])
        for protocol in protocols:
            protocoldatasources = self.get_protocoldatasource(protocol) # get redcap protocol datasource
            for pds in protocoldatasources:
                print ("\n Caching protocol datasource {} \n".format(pds))
                user = self.get_protocol_user(protocol) # get eig user in protocol
                subject_id_list = self.get_protocol_subjects(protocol, lbls) # get all subjects in protocol
                try:
                    cache_key = 'protocoldatasource{0}'.format(pds.id) + '_redcap_completion_codes'
                    cache.delete(cache_key)
                except AttributeError: # protocoldatasource wasn't properly configured
                    print (str(pds) + ' was skipped')
                    continue

                threads = [] # array to hold all threads, length is # of records per subj
                for s_id in subject_id_list: # for every subject
                    # creating threads
                    curr_thread = threading.Thread(target=subject_threading, args=(self, pds, s_id, lbls, user, cache_key,))
                    threads.append(curr_thread)
                    curr_thread.start()
                # make sure every thread has finished
                for t in threads:
                    t.join()

        elapsed = time.time()-start
        print ("total caching time" + str (elapsed))
        print("caching records table complete")
