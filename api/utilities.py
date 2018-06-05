import logging
import json

from .models.constants import ProtocolConstants
from .ehb_service_client import ServiceClient

from ehb_client.requests.group_request_handler import Group
from ehb_client.requests.exceptions import PageNotFound
from ehb_client.requests.external_record_request_handler import ExternalRecord
from ehb_datasources.drivers.exceptions import RecordCreationError

logger = logging.getLogger(__name__)


class DriverUtils(object):

    @staticmethod
    def getDriverFor(protocol_data_source, user):
        '''
        Attempts to get the driver for the specified protocol_data_source and
        user and configures the driver.  If the user does not have
        credentials for this data source a DoesNotExist exception is raised
        '''
        from .models.protocols import ProtocolUserCredentials

        creds = ProtocolUserCredentials.objects.get(
            protocol=protocol_data_source.protocol,
            data_source=protocol_data_source,
            user=user
        )

        driver = protocol_data_source.getDriver(creds)

        driver.configure(
            driver_configuration=protocol_data_source.driver_configuration)

        return driver


class RecordUtils(object):

    @staticmethod
    def serialize_external_records(pds, records, labels):
        '''
        Returns serialized form of eHB external records from the eHB to API
        friendly form. API friendly meaning it contains ProtocolDatasource ID,
        and label description.
        '''

        serialized_records = []

        for ex_rec in records:

            # Convert ehb-client object to JSON and then parse as py dict
            e = json.loads(ex_rec.json_from_identity(ex_rec))

            # Map label descriptions from the eHB to External Records
            for label in labels:
                if e['label'] == label['id']:

                    if label['label'] == '':
                        e['label_desc'] = 'Record'

                    else:
                        e['label_desc'] = label['label']

            e['pds'] = pds.id
            serialized_records.append(e)

        return serialized_records


class SubjectUtils(object):
    @staticmethod
    def protocol_subject_record_group_name(protocol, subject):
        from .models.protocols import Organization

        orh = ServiceClient.get_rh_for(record_type=ServiceClient.ORGANIZATION)
        ehb_org = orh.get(id=subject.organization_id)
        brp_org = Organization.objects.get(name=ehb_org.name)

        return ':'.join(['BRP',
                         protocol.immutable_key.key,
                         brp_org.immutable_key.key,
                         subject.organization_subject_id])

    @staticmethod
    def get_protocol_subject_record_group(protocol, subject):
        gh = ServiceClient.get_rh_for(record_type=ServiceClient.GROUP)

        return gh.get(
            name=SubjectUtils.protocol_subject_record_group_name(
                protocol, subject))

    @staticmethod
    def create_protocol_subject_record_group(protocol, subject):
        try:

            n = SubjectUtils.protocol_subject_record_group_name(
                protocol, subject)

            gh = ServiceClient.get_rh_for(record_type=ServiceClient.GROUP)
            ck = protocol._settings_prop('CLIENT_KEY', 'key', '')

            grp = Group(
                name=n,
                description='A BRP Protocol Subject Record Group',
                is_locking=True,
                client_key=ck
            )

            r = gh.create(grp)

            return r[0].get('success')
        except:
            raise
            logger.error("Failure creating a subject record group for"
                         " {0}".format(subject.id))

            return False

    @staticmethod
    def delete_protocol_subject_record_group(protocol, subject):
        try:

            n = SubjectUtils.protocol_subject_record_group_name(
                protocol, subject)

            gh = ServiceClient.get_rh_for(record_type=ServiceClient.GROUP)
            ck = protocol._settings_prop('CLIENT_KEY', 'key', '')

            gh.delete(name=n, client_key=ck)
            return True

        except:
            return False

    @staticmethod
    def standard_record_prefix(subject):
        return ''.join([ProtocolConstants.ex_rec_org_pre,
                        str(subject.organization_id),
                        ProtocolConstants.ex_rec_sep,
                        ProtocolConstants.ex_rec_sub_id_pre,
                        str(subject.organization_subject_id)])

    @staticmethod
    def add_record_to_subject_record_group(protocol, subject, record):
        grp = SubjectUtils.get_protocol_subject_record_group(
            protocol, subject)

        grp.client_key = protocol._settings_prop('CLIENT_KEY', 'key', '')
        gh = ServiceClient.get_rh_for(record_type=ServiceClient.GROUP)

        gh.add_records(grp, [record])

    @staticmethod
    def validate_new_record_id(protocol_data_source, subject, record_id,
                               include_path):

        er_rh = ServiceClient.get_rh_for(
            record_type=ServiceClient.EXTERNAL_RECORD)

        try:

            ehb_recs = None

            if include_path:

                ehb_recs = er_rh.get(
                    external_system_url=protocol_data_source.data_source.url,
                    path=protocol_data_source.path
                )

            else:

                ehb_recs = er_rh.get(
                    external_system_url=protocol_data_source.data_source.url
                )

            for record in ehb_recs:
                if record.record_id == record_id:
                    if record.subject_id == subject.id:

                        logger.error(
                            'Record id {0} already exists for subject {1} on'
                            ' datasource {2}'.format(
                                record.record_id,
                                subject.id,
                                protocol_data_source))

                        return 1

                    else:
                        logger.error(
                            'Record id {0} already exists for a different'
                            ' Subject').format(record.record_id)

                        return 2

            return 0

        except PageNotFound:
            return 0

    @staticmethod
    def create_new_ehb_external_record(protocol_data_source, user, subject,
                                       record_id, label=None):

        es = protocol_data_source.data_source.getExternalSystem()

        # Want to make sure we're not going to overwrite a record already in the system
        try:

            if not label:
                label = 1

            er = ExternalRecord(
                record_id=record_id,
                subject_id=subject.id,
                external_system_id=es.id,
                path=protocol_data_source.path,
                label_id=label
            )

            errh = ServiceClient.get_rh_for(
                record_type=ServiceClient.EXTERNAL_RECORD
            )

            response = errh.create(er)[0]

            if(response.get('success')):

                SubjectUtils.add_record_to_subject_record_group(
                    protocol_data_source.protocol,
                    subject,
                    er
                )

                return er

            else:

                errors = response.get('errors')

                raise RecordCreationError(
                    'electronic Honest Broker',
                    '',
                    record_id,
                    errors
                )

        except RecordCreationError as rce:
            raise rce

        except Exception as e:

            raise RecordCreationError(
                'electronic Honest Broker',
                '',
                record_id,
                str(e)
            )
