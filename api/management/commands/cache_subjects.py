# encoding: utf-8
import json
import time

from api.ehb_service_client import ServiceClient
from api.models.protocols import Protocol
from api.serializers import eHBSubjectSerializer

from ehb_client.requests.exceptions import PageNotFound

from django.core.management.base import BaseCommand
from django.core.cache import cache


from rest_framework.response import Response


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('protocol_id', nargs='+', type=str)

    def getExternalRecords(self, pds, subject, lbls):
        er_rh = ServiceClient.get_rh_for(record_type=ServiceClient.EXTERNAL_RECORD)
        try:
            pds_records = er_rh.get(
                external_system_url=pds.data_source.url, path=pds.path, subject_id=subject['id'])
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

    def cache_records(self, protocol_id):
        protocol_id = protocol_id[0]
        if protocol_id == 'all':
            protocols = Protocol.objects.all()
        else:
            protocols = Protocol.objects.filter(id=int(protocol_id)).all()
        er_label_rh = ServiceClient.get_rh_for(record_type=ServiceClient.EXTERNAL_RECORD_LABEL)
        lbls = er_label_rh.query()
        print('Caching {0} protocol(s)...'.format(len(protocols)))
        for protocol in protocols:
            print('Caching {}'.format(protocol))
            subjects = protocol.getSubjects()
            organizations = protocol.organizations.all()
            if subjects:
                subs = [eHBSubjectSerializer(sub).data for sub in subjects]
            else:
                continue
            ehb_orgs = []
            # We can't rely on Ids being consistent across apps so we must
            # append the name here for display downstream.
            for o in organizations:
                ehb_orgs.append(o.getEhbServiceInstance())
            # Check if the protocol has external IDs configured. If so retrieve them
            manageExternalIDs = False

            protocoldatasources = protocol.getProtocolDataSources()

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
                    raise
                    pass

            for sub in subs:
                sub['external_records'] = []
                sub['external_ids'] = []
                sub['organization'] = sub['organization_id']
                sub.pop('organization_id')
                for pds in protocoldatasources:
                    try:
                        sub['external_records'].extend(self.getExternalRecords(pds, sub, lbls))
                    except:
                        print("there was an error processing external records")
                        print("subject DB id:")
                        print(sub['id'])
                        print("protocol data source:")
                        print(pds)
                        pass


                if manageExternalIDs:
                    # Break out external ids into a separate object for ease of use
                    for record in sub['external_records']:
                        if record['external_system'] == 3:
                            try:
                                sub['external_ids'].append(record)
                            except:
                                print("an error occured getting external records")
                                print(sub['external_ids'])
                for ehb_org in ehb_orgs:
                    if sub['organization'] == ehb_org.id:
                        sub['organization_name'] = ehb_org.name
            cache_key = 'protocol{0}_sub_data'.format(protocol.id)
            cache.set(cache_key, json.dumps(subs))
            cache.persist(cache_key)

    def handle(self, *args, **options):
        self.cache_records(options['protocol_id'])
        print("caching complete")
