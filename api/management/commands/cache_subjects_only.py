# encoding: utf-8
import json
import time
import datetime

from api.ehb_service_client import ServiceClient
from api.models.protocols import Protocol
from api.serializers import eHBSubjectSerializer
from api.utilities import SubjectUtils

from ehb_client.requests.exceptions import PageNotFound

from django.core.management.base import BaseCommand
from django.core.cache import cache


class Command(BaseCommand):
    """Cache subjects from given protocols locally."""

    help = 'Cache subjects from given protocols locally.'

    def add_arguments(self, parser):
        """Set up the protocol_id argument."""
        parser.add_argument('protocol_id', nargs='+', type=str)

    def cache_records(self, protocol_id):
        """Cache subject records from a given protocol locally."""

        protocol_id = protocol_id[0]

        if protocol_id == 'all':
            protocols = Protocol.objects.all()
        else:
            protocols = Protocol.objects.filter(id=int(protocol_id)).all()

        # Tell user how many protocols are being cached.
        print('Caching {0} protocol(s)...'.format(len(protocols)))

        for protocol in protocols:

            all_subs = []
            # Tell user which protocol is being cached.
            print('Caching {}'.format(protocol))
            all_subs = SubjectUtils.get_protocol_subjects(protocol)

            # Cache the array of subjects.
            cache_key = 'protocol{0}_sub_only_data'.format(protocol.id)
            cache.set(cache_key, json.dumps(all_subs))
            cache.persist(cache_key)

    def handle(self, *args, **options):
        """Handle command invocation."""
        self.cache_records(options['protocol_id'])
        print("caching complete")
