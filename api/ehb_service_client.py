from django.conf import settings

from ehb_client.requests.external_record_request_handler import ExternalRecordRequestHandler  # noqa
from ehb_client.requests.external_record_request_handler import ExternalRecordLabelRequestHandler  # noqa
from ehb_client.requests.external_record_request_handler import ExternalRecordRelationRequestHandler  # noqa
from ehb_client.requests.external_system_request_handler import ExternalSystemRequestHandler  # noqa
from ehb_client.requests.subject_request_handler import SubjectRequestHandler
from ehb_client.requests.organization_request_handler import OrganizationRequestHandler  # noqa
from ehb_client.requests.group_request_handler import GroupRequestHandler


class ServiceClient(object):
    """This class provides access to the ehb-client api.

    The various request handlers are initialized using auth settings. They
    can be accessed using the `get_rh_for` method with either the record_type
    constant or a record instance itself. The `create` method tries to create
    a passed record in the EHB, using the passed functions on success, error,
    and exception.
    """

    SERVICE_CLIENT_SETTINGS = settings.SERVICE_CLIENT_SETTINGS
    host = SERVICE_CLIENT_SETTINGS['HOST']
    # This is for calls to the eHB
    root_path = SERVICE_CLIENT_SETTINGS['ROOT_PATH']
    # This is needed for react UI to connect to the BRP dataentry Backend
    self_root_path = SERVICE_CLIENT_SETTINGS['SELF_ROOT_PATH']
    isSecure = SERVICE_CLIENT_SETTINGS['ISSECURE']
    APP_URL = SERVICE_CLIENT_SETTINGS['APP_URL']
    api_key = SERVICE_CLIENT_SETTINGS['API_KEY']

    ext_rec_client = ExternalRecordRequestHandler(
        host, root_path, isSecure, api_key)

    ext_rec_rel_client = ExternalRecordRelationRequestHandler(
        host, root_path, isSecure, api_key)

    ext_rec_label_client = ExternalRecordLabelRequestHandler(
        host, root_path, isSecure, api_key)

    ext_sys_client = ExternalSystemRequestHandler(
        host, root_path, isSecure, api_key)

    subj_client = SubjectRequestHandler(host, root_path, isSecure, api_key)
    org_client = OrganizationRequestHandler(host, root_path, isSecure, api_key)
    group_client = GroupRequestHandler(host, root_path, isSecure, api_key)

    SUBJECT = 0
    EXTERNAL_SYSTEM = 1
    EXTERNAL_RECORD = 2
    ORGANIZATION = 3
    GROUP = 4
    EXTERNAL_RECORD_LABEL = 5
    EXTERNAL_RECORD_RELATION = 6

    req_handlers = {
        EXTERNAL_SYSTEM: ext_sys_client,
        EXTERNAL_RECORD: ext_rec_client,
        EXTERNAL_RECORD_LABEL: ext_rec_label_client,
        EXTERNAL_RECORD_RELATION: ext_rec_rel_client,
        SUBJECT: subj_client,
        ORGANIZATION: org_client,
        GROUP: group_client
    }

    @staticmethod
    def get_rh_for(**kwargs):
        """Get the request handler for the given record instance or constant.

        Args:
            record: value of an appropriate ehb_client IdentityBase instance
            record_type: value from one of ServiceClient predefined int values

        Returns:
            An auth-configured instance of the appropriate EHB client request
            handler or None if the appropriate client can't be found.
        """

        rec_type = kwargs.pop('record_type', -1)
        record = kwargs.pop('record', None)

        if rec_type in ServiceClient.req_handlers:
            return ServiceClient.req_handlers.get(rec_type)

        elif record:

            # TODO: Could the `isinstance()` builtin function work here?
            for c in type(record).__bases__:

                if c.__name__ == 'Subject':
                    return ServiceClient.subj_client
                elif c.__name__ == 'ExternalSystem':
                    return ServiceClient.ext_sys_client
                elif c.__name__ == 'ExternalRecord':
                    return ServiceClient.ext_rec_client
                elif c.__name__ == 'ExternalRecordLabel':
                    return ServiceClient.ext_rec_label_client
                elif c.__name__ == 'ExternalRecordRelation':
                    return ServiceClient.ext_rec_rel_client
                elif c.__name__ == 'Organization':
                    return ServiceClient.org_client
                elif c.__name__ == 'Group':
                    return ServiceClient.group_client

        else:
            return None

    @staticmethod
    def create(record, f_success, f_errors, f_except=None):
        """Create a record in the EHB using the provided callbacks."""

        rh = ServiceClient.get_rh_for(record)

        if rh:
            try:

                r = rh.create(record)[0]
                s = r.get('success')

                if s:
                    f_success(r.get(record.identityLabel))

                else:
                    f_errors(r.get('errors'))

            except Exception as e:

                if f_except is None:
                    raise e

                else:
                    f_except(e)

        else:

            msg = ('No request handler found for record of type:'
                   ' {0}').format(str(type(record)))

            raise Exception(msg)
