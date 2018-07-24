# encoding: utf-8
import json
import time

from api.ehb_service_client import ServiceClient
from api.models.protocols import Protocol
from api.serializers import eHBSubjectSerializer

from ehb_client.requests.exceptions import PageNotFound

from django.core.management.base import BaseCommand
from django.core.cache import cache


class Command(BaseCommand):
    """Cache subjects from given protocols locally."""

    help = 'Cache subjects from given protocols locally.'

    def add_arguments(self, parser):
        """Set up the protocol_id argument."""
        parser.add_argument('protocol_id', nargs='+', type=str)

    def getExternalRecords(self, pds, subject, lbls):
        """Get external records for a subject/protocol combination.

        Returns external records for a given subject from a given protocol
        after labelling them with EHB labels and the protocol id.
        """

        # Get the appropriate request handler for external records.
        er_rh = ServiceClient.get_rh_for(
            record_type=ServiceClient.EXTERNAL_RECORD)

        try:

            # Retrieve the external records for the subject/protocol.
            # Path argument is needed for ehb_datasources to make request.
            pds_records = er_rh.get(
                external_system_url=pds.data_source.url, path=pds.path,
                subject_id=subject['id'])

            # TODO: why is this necessary?
            time.sleep(0.05)

        except PageNotFound:

            # Return an empty array if the subject/protocol is not found.
            pds_records = []

        # Result array.
        r = []

        for ex_rec in pds_records:

            # Convert ehb-client object to JSON and then parse as py dict.
            # TODO: the external record object should have this capability.
            # We should examine this to refactor for simplicity. It is possible
            # to remove json.loads for each json_from_identity call.
            e = json.loads(ex_rec.json_from_identity(ex_rec))

            # Map label descriptions from the eHB to External Records.
            for label in lbls:
                if e['label'] == label['id']:
                    if label['label'] == '':
                        e['label_desc'] = 'Record'
                    else:
                        e['label_desc'] = label['label']

            # Add the protocol datasource id to the external record.
            e['pds'] = pds.id
            r.append(e)

        return r

    def cache_records(self, protocol_id):
        """Cache subject records from a given protocol locally."""

        # TODO: consider passing in a list if we ever need to cache a small
        # number of protocols at one time. look at why only using first item in
        # list.
        protocol_id = protocol_id[0]

        if protocol_id == 'all':
            # Special "all" protocol gets all protocols.
            protocols = Protocol.objects.all()
        else:
            protocols = Protocol.objects.filter(id=int(protocol_id)).all()

        # Get external record label request handler.
        er_label_rh = ServiceClient.get_rh_for(
            record_type=ServiceClient.EXTERNAL_RECORD_LABEL)

        # Retrieve the actual external record labels.
        lbls = er_label_rh.query()

        # Tell user how many protocols are being cached.
        print('Caching {0} protocol(s)...'.format(len(protocols)))

        for protocol in protocols:

            # Tell user which protocol is being cached.
            print('Caching {}'.format(protocol))

            # Get list of subjects and organizations in the protocol.
            subjects = protocol.getSubjects()
            organizations = protocol.organizations.all()

            # Serialize retrieved subjects or continue if there are none.
            if subjects:
                subs = [eHBSubjectSerializer(sub).data for sub in subjects]
            else:
                continue

            ehb_orgs = []

            # We can't rely on Ids being consistent across apps so we must
            # append the name here for display downstream.
            for o in organizations:
                ehb_orgs.append(o.getEhbServiceInstance())

            # TODO: Explain this block, down to the `for sub in subs` loop.
            # Check if the protocol has external IDs configured.
            # If so, retrieve them.
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
                        # er_label_rh = ServiceClient.get_rh_for(
                        #     record_type=ServiceClient.EXTERNAL_RECORD_LABEL)
                        # lbl = er_label_rh.get(id=config['sort_on'])
                        lbl = ''
                        addl_id_column = lbl  # noqa
                except:
                    raise
                    pass

            # Transform subjects for ease of use.
            for sub in subs:

                # Initialize new fields.
                sub['external_records'] = []
                sub['external_ids'] = []
                sub['organization'] = sub['organization_id']
                sub.pop('organization_id')

                # Add external records from all data sources.
                for pds in protocoldatasources:
                    try:
                        sub['external_records'].extend(
                            self.getExternalRecords(pds, sub, lbls))
                    except:
                        print("there was an error processing external records")
                        print("subject DB id:")
                        print(sub['id'])
                        print("protocol data source:")
                        print(pds)
                        pass

                # TODO: Explain this block.
                if manageExternalIDs:
                    # Break out external ids into a separate object for ease of
                    # use.
                    for record in sub['external_records']:
                        if record['external_system'] == 3:
                            try:
                                sub['external_ids'].append(record)
                            except:
                                print("an error occured getting external records")
                                print(sub['external_ids'])

                # Add organization name to subject record for display, since
                # organization IDs can vary across apps. (?)
                for ehb_org in ehb_orgs:
                    if sub['organization'] == ehb_org.id:
                        sub['organization_name'] = ehb_org.name

            # Cache the array of subjects.
            cache_key = 'protocol{0}_sub_data'.format(protocol.id)
            cache.set(cache_key, json.dumps(subs))
            cache.persist(cache_key)

    def handle(self, *args, **options):
        """Handle command invocation."""
        self.cache_records(options['protocol_id'])
        print("caching complete")
