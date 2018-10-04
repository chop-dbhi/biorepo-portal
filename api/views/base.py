from django.core.cache import cache as _cache
from rest_framework.views import APIView
# from rest_framework import authentication
from api.ehb_service_client import ServiceClient
from api.utilities import SubjectUtils, RecordUtils


class BRPApiView(APIView):
    # Cache
    cache = _cache
    # Honest Broker Request Handelers
    s_rh = ServiceClient.get_rh_for(record_type=ServiceClient.SUBJECT)
    o_rh = ServiceClient.get_rh_for(record_type=ServiceClient.ORGANIZATION)
    es_rh = ServiceClient.get_rh_for(record_type=ServiceClient.EXTERNAL_SYSTEM)
    er_rh = ServiceClient.get_rh_for(record_type=ServiceClient.EXTERNAL_RECORD)
    erl_rh = ServiceClient.get_rh_for(record_type=ServiceClient.EXTERNAL_RECORD_LABEL)  # noqa
    err_rh = ServiceClient.get_rh_for(record_type=ServiceClient.EXTERNAL_RECORD_RELATION)  # noqa
    g_rh = ServiceClient.get_rh_for(record_type=ServiceClient.GROUP)
    relationship_HB_handler = ServiceClient.get_rh_for(record_type=ServiceClient.RELATIONSHIP)
    # Utility Classes
    subject_utils = SubjectUtils
    record_utils = RecordUtils
