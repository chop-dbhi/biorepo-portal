import json
import datetime
from unittest.mock import MagicMock, patch

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from rest_framework.test import APIRequestFactory, APITestCase, \
    force_authenticate, APIClient
from rest_framework.authtoken.models import Token
from ehb_client.requests.subject_request_handler import Subject
from ehb_client.requests.organization_request_handler import Organization
from ehb_client.requests.external_record_request_handler import ExternalRecord
from ehb_client.requests.group_request_handler import Group
from ehb_client.requests.exceptions import PageNotFound
from ..models.protocols import Protocol, ProtocolDataSource
from ..views.protocol import ProtocolViewSet, ProtocolDataSourceView, \
    ProtocolOrganizationView, ProtocolSubjectsView, ProtocolSubjectDetailView
from ..views import PDSViewSet, PDSSubjectView, PDSSubjectRecordsView, \
    PDSSubjectRecordDetailView, PDSRecordLinkDetailView, PDSAvailableLinksView
from api.views.base import BRPApiView

factory = APIRequestFactory()


TestSubject = Subject(
    id=2,
    first_name='Jane',
    last_name='Sample',
    organization_id=1,
    organization_subject_id='MRN123',
    dob=datetime.date(1990, 1, 1),
    modified=datetime.datetime(2015, 1, 1),
    created=datetime.datetime(2015, 1, 1)
)
TestOrganization = Organization(
    id=1,
    name='Amazing Children\'s Hospital',
    subject_id_label='Subject',
    modified=datetime.datetime(2015, 1, 1),
    created=datetime.datetime(2015, 1, 1)
)
TestExternalRecord = ExternalRecord(
    record_id='xyz123',
    external_system_id=1,
    subject_id=1,
    path='testpath',
    modified=datetime.datetime(2014, 1, 1),
    created=datetime.datetime(2014, 1, 1),
    id=1,
    label_id=1
)
TestGroup = Group(
    id=1,
    name='TestGroup',
    is_locking=False,
    client_key='testck',
    description='A test group'
)


BRPApiView.s_rh.get = MagicMock(return_value=TestSubject)
BRPApiView.s_rh.update = MagicMock(return_value=[{'success': True, 'errors': [], 'subject': TestSubject}])
BRPApiView.o_rh.get = MagicMock(return_value=TestOrganization)
BRPApiView.er_rh.get = MagicMock(return_value=[
    ExternalRecord(
        record_id='xyz123',
        external_system_id=1,
        subject_id=1,
        path='testpath',
        modified=datetime.datetime(2014, 1, 1),
        created=datetime.datetime(2014, 1, 1),
        id=1,
        label_id=1
    )])
BRPApiView.erl_rh.query = MagicMock(return_value=[{"id": 1, "label": ""}, {"id": 2, "label": "SSN"}, {"id": 3, "label": "Initial Diagnosis"}])


class BRPTestCase(APITestCase):

    fixtures = ['demo_data']

    def setUp(self):
        self.test_user = User.objects.get(username='admin')
        self.test_protocol = Protocol.objects.get(pk=1)
        self.test_pds = ProtocolDataSource.objects.get(pk=1)

    def cleanUp(self):
        token = Token.objects.get(user__username='admin')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse(
            'protocol-subject-view',
            kwargs={
                'pk': self.test_protocol.id,
                'subject': 2
            })
        client.delete(url)


class ProtocolViewTests(BRPTestCase):
    def test_retrieve_all_protocols(self):
        '''
        Ensure we can retrieve all protocols
        '''
        view = ProtocolViewSet.as_view({'get': 'list'})
        url = reverse('protocol-list')
        request = factory.get(url)
        force_authenticate(request, user=self.test_user)
        response = view(request)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'Demonstration Protocol')

    def test_retrieve_pds_from_protocol(self):
        '''
        Ensure we can retrieve all ProtocolDataSources associated with a
        Protocol
        '''
        view = ProtocolDataSourceView.as_view()
        url = reverse(
            'protocol-datasources-list',
            kwargs={'pk': self.test_protocol.id})
        request = factory.get(url)
        force_authenticate(request, user=self.test_user)
        response = view(request, pk=self.test_protocol.id)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_retrieve_pds_from_protocol_badpk(self):
        '''
        Ensure we get a proper error code when trying to retrieve
        ProtocolDatasources associated with a non-existent Protocol
        '''
        view = ProtocolDataSourceView.as_view()
        url = reverse(
            'protocol-datasources-list',
            kwargs={'pk': 99})
        request = factory.get(url)
        force_authenticate(request, user=self.test_user)
        response = view(request, pk=99)
        response.render()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['error'], 'Protocol requested not found')

    def test_retrieve_orgs_from_protocol(self):
        '''
        Ensure we can retrieve all Organizations associated with a
        Protocol
        '''
        view = ProtocolOrganizationView.as_view()
        url = reverse(
            'protocol-organization-list',
            kwargs={'pk': self.test_protocol.id})
        request = factory.get(url)
        force_authenticate(request, user=self.test_user)
        response = view(request, pk=self.test_protocol.id)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_orgs_from_protocol_badpk(self):
        '''
        Ensure we get a proper error code when trying to retrieve
        Organizations associated with a non-existent Protocol
        '''
        view = ProtocolOrganizationView.as_view()
        url = reverse(
            'protocol-organization-list',
            kwargs={'pk': 99})
        request = factory.get(url)
        force_authenticate(request, user=self.test_user)
        response = view(request, pk=99)
        response.render()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['error'], 'Protocol requested not found')

    @patch('api.views.base.BRPApiView.g_rh.get_subjects')
    def test_retrieve_subjects_from_protocol(self, mock_grh):
        '''
        Ensure we can retrieve all Subjects associated with a Protocol
        '''
        view = ProtocolSubjectsView.as_view()
        url = reverse(
            'protocol-subject-list',
            kwargs={'pk': self.test_protocol.id})
        mock_grh.return_value = [TestSubject]
        request = factory.get(url)
        force_authenticate(request, user=self.test_user)
        response = view(request, pk=self.test_protocol.id)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_subjects_from_protocol_badpk(self):
        '''
        Ensure we get a proper error code when trying to retrieve
        Subjects associated with a Protocol with a non-existent Protocol
        '''
        view = ProtocolSubjectsView.as_view()
        url = reverse(
            'protocol-subject-list',
            kwargs={'pk': 99})
        request = factory.get(url)
        force_authenticate(request, user=self.test_user)
        response = view(request, pk=99)
        response.render()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['error'], 'Protocol requested not found')

    @patch('api.models.protocols.Protocol._subject_group')
    @patch('api.views.base.BRPApiView.s_rh.get')
    @patch('api.views.base.BRPApiView.g_rh.create')
    @patch('api.views.base.BRPApiView.g_rh.add_subjects')
    @patch('api.views.base.BRPApiView.s_rh.create')
    def test_create_and_delete_subject_on_protocol(self, screate_mock, gadd_mock, gcreate_mock, sget_mock, subject_group_mock):
        '''
        Ensure that we can create a subject on a Protocol
        '''
        subject = {
            'first_name': 'John',
            'last_name': 'Doe',
            'organization_subject_id': '1234',
            'organization': '1',
            'dob': '2000-01-01'
        }
        url = reverse(
            'protocol-subject-create',
            kwargs={
                'pk': self.test_protocol.id
            })
        token = Token.objects.get(user__username='admin')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        # Mock subject not found
        sget_mock.side_effect = PageNotFound(path='/')
        # Mock subject group creation
        gcreate_mock.return_value = [{'success': True}]
        # Mock addition of subject to group
        gadd_mock.add_subjects.return_value = [{'success': True}]
        screate_mock.return_value = [{
            'success': True,
            'errors': [],
            'subject': Subject(
                id=2,
                first_name='John',
                last_name='Doe',
                organization_id=1,
                organization_subject_id='1234',
                dob=datetime.date(1990, 1, 1),
                modified=datetime.datetime(2015, 1, 1),
                created=datetime.datetime(2015, 1, 1)
            )
        }]
        subject_group_mock.return_value.id = "12345"

        response = client.post(url, subject, format='json')
        success, subject, errors = response.data
        if errors:
            print(errors)
        self.assertTrue(success)
        self.assertEqual(len(errors), 0)
        url = reverse(
            'protocol-subject-view',
            kwargs={
                'pk': self.test_protocol.id,
                'subject': subject['id']
            })
        response = client.delete(url)

    @patch('api.ehb_service_client.ServiceClient.ehb_api')
    @patch('api.views.base.BRPApiView.o_rh.get')
    @patch('api.views.base.BRPApiView.g_rh.get')
    @patch('api.views.protocol.ProtocolSubjectDetailView.update_subject_group')
    @patch('api.views.protocol.ProtocolSubjectDetailView.updateEhbSubject')
    def test_update_subject_on_protocol(self, mock_subject_update, mock_grh_update, mock_grh_get, mock_orh, mock_srh):
        '''
        Ensure that we can create a subject on a Protocol
        '''
        subject = {
            'id': 1,
            'first_name': 'Johnny',
            'last_name': 'Sample',
            'organization_subject_id': '42424242',
            'organization': '1',
            'dob': '2000-01-01',
            'modified': '2015-01-01 00:00:00.000',
            'created': '2015-01-01 00:00:00.000'
        }
        url = reverse(
            'protocol-subject-view',
            kwargs={
                'pk': self.test_protocol.id,
                'subject': self.test_user.id
            })
        token = Token.objects.get(user__username='admin')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        mock_orh.return_value = TestOrganization
        mock_srh.return_value.json.return_value = subject
        mock_grh_get.return_value = TestGroup
        mock_grh_update.return_value = {'success': True}
        response = client.put(url, subject, format='json')
        self.assertTrue(response.status_code, 200)
        self.assertEqual(response.data['first_name'], 'Johnny')

    def test_retrieve_subject_detail_from_protocol(self):
        '''
        Ensure we can retrieve details regarding Subject associated with Protocol
        '''
        view = ProtocolSubjectDetailView.as_view()
        url = reverse(
            'protocol-subject-view',
            kwargs={
                'pk': self.test_protocol.id,
                'subject': 2
            })
        request = factory.get(url)
        force_authenticate(request, user=self.test_user)
        response = view(
            request,
            pk=self.test_protocol.id,
            subject=2)
        response.render()
        self.assertEqual(response.status_code, 200)
        # Check structure
        self.assertTrue('first_name' in list(response.data.keys()))
        self.assertTrue('last_name' in list(response.data.keys()))
        self.assertTrue('created' in list(response.data.keys()))
        self.assertTrue('modified' in list(response.data.keys()))
        self.assertTrue('dob' in list(response.data.keys()))
        self.assertTrue('external_records' in list(response.data.keys()))
        self.assertTrue('external_ids' in list(response.data.keys()))
        self.assertTrue('organization_name' in list(response.data.keys()))
        self.assertTrue('organization_subject_id' in list(response.data.keys()))
        self.assertTrue('organization' in list(response.data.keys()))
        self.assertTrue('group_name' in list(response.data.keys()))
        self.assertTrue('id' in list(response.data.keys()))
        # Check for records
        self.assertEqual(len(response.data['external_records']), 3)
        record = response.data['external_records'][0]
        # Check record structure
        self.assertTrue('id' in list(record.keys()))
        self.assertTrue('label_desc' in list(record.keys()))
        self.assertTrue('created' in list(record.keys()))
        self.assertTrue('pds' in list(record.keys()))
        self.assertTrue('modified' in list(record.keys()))
        self.assertTrue('label' in list(record.keys()))
        self.assertTrue('record_id' in list(record.keys()))
        self.assertTrue('path' in list(record.keys()))
        self.assertTrue('external_system' in list(record.keys()))
        self.assertTrue('subject' in list(record.keys()))

    def test_retrieve_subject_detail_from_protocol_badpk(self):
        '''
        Ensure we get a proper error code when trying to retrieve
        Subject details associated with a Protocol with a non-existent Protocol
        '''
        view = ProtocolSubjectDetailView.as_view()
        url = reverse(
            'protocol-subject-view',
            kwargs={
                'pk': 99,
                'subject': 1
            })
        request = factory.get(url)
        force_authenticate(request, user=self.test_user)
        response = view(
            request,
            pk=99,
            subject=1)
        response.render()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['error'], 'Protocol requested not found')

    @patch('api.views.base.BRPApiView.s_rh.get')
    def test_retrieve_subject_detail_from_protocol_badsubject(self, mock_srh):
        '''
        Ensure we get a proper error code when trying to retrieve
        Subject details associated with a Protocol with a non-existent Subject
        '''
        view = ProtocolSubjectDetailView.as_view()
        url = reverse(
            'protocol-subject-view',
            kwargs={
                'pk': self.test_protocol.id,
                'subject': 99
            })
        mock_srh.side_effect = PageNotFound
        request = factory.get(url)
        force_authenticate(request, user=self.test_user)
        response = view(
            request,
            pk=self.test_protocol.id,
            subject=99)
        response.render()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['error'], 'Subject not found')


class PDSViewTests(BRPTestCase):

    def test_retrieve_pds_list(self):
        '''
        Ensure we can retrieve all protocols
        '''
        view = PDSViewSet.as_view({'get': 'list'})
        url = reverse('protocoldatasource-list')
        request = factory.get(url)
        force_authenticate(request, user=self.test_user)
        response = view(request)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 6)

    @patch('api.models.protocols.Protocol.getSubjects')
    @patch('api.views.base.BRPApiView.er_rh.query')
    def test_retrieve_pds_subject_list(self, mock_errh, mock_getsubs):
        view = PDSSubjectView.as_view()
        url = reverse(
            'pds-subject-list',
            kwargs={
                'pk': 1
            })
        mock_getsubs.return_value = [Subject(
            id=2,
            first_name='John',
            last_name='Doe',
            organization_id=1,
            organization_subject_id='1234',
            dob=datetime.date(1990, 1, 1),
            modified=datetime.datetime(2015, 1, 1),
            created=datetime.datetime(2015, 1, 1)
        )]
        mock_errh.return_value = [{
            'success': True,
            'external_record': [TestExternalRecord]
        }]
        request = factory.get(url)
        force_authenticate(request, user=self.test_user)
        response = view(
            request,
            pk=self.test_pds.id
        )
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['subjects']), 1)
        self.assertEqual(response.data['count'], 1)

    @patch('api.views.base.BRPApiView.er_rh.query')
    def test_retrieve_pds_subject_records(self, mock_errh):
        view = PDSSubjectRecordsView.as_view()
        url = reverse(
            'pds-subject-record-list',
            kwargs={
                'pk': self.test_pds.id,
                'subject': 1
            })
        mock_errh.return_value = [{
            'success': True,
            'external_record': [TestExternalRecord]
        }]
        request = factory.get(url)
        force_authenticate(request, user=self.test_user)
        response = view(
            request,
            pk=self.test_pds.id,
            subject=1
        )
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    @patch('api.views.base.BRPApiView.er_rh.get')
    def test_retrieve_pds_subject_record_detail(self, mock_errh):
        view = PDSSubjectRecordDetailView.as_view()
        url = reverse(
            'pds-subject-record',
            kwargs={
                'pk': self.test_pds.id,
                'subject': 1,
                'record': 1
            })
        mock_errh.return_value = TestExternalRecord
        request = factory.get(url)
        force_authenticate(request, user=self.test_user)
        response = view(
            request,
            pk=self.test_pds.id,
            subject=1,
            record=1
        )
        response.render()
        self.assertEqual(response.status_code, 200)
        # Check Record structure
        record = response.data
        self.assertTrue('id' in list(record.keys()))
        self.assertTrue('created' in list(record.keys()))
        self.assertTrue('modified' in list(record.keys()))
        self.assertTrue('label' in list(record.keys()))
        self.assertTrue('record_id' in list(record.keys()))
        self.assertTrue('path' in list(record.keys()))
        self.assertTrue('external_system' in list(record.keys()))
        self.assertTrue('subject' in list(record.keys()))

    @patch('api.views.base.BRPApiView.er_rh.get')
    def test_retrieve_pds_subject_record_links(self, mock_errh):
        view = PDSRecordLinkDetailView.as_view()
        url = reverse(
            'pds-subject-record-links',
            kwargs={
                'pk': self.test_pds.id,
                'subject': 1,
                'record': 1
            })
        mock_errh.return_value = [{
            'external_record': {},
            'type': 'familial',
            'description': 'lorem ipsum',
            'id': 1,
            'primary': True
        }]
        request = factory.get(url)
        force_authenticate(request, user=self.test_user)
        response = view(
            request,
            pk=self.test_pds.id,
            subject=1,
            record=1
        )
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        # Check structure
        link = response.data[0]
        self.assertTrue('external_record' in list(link.keys()))
        self.assertTrue('id' in list(link.keys()))
        self.assertTrue('type' in list(link.keys()))
        self.assertTrue('description' in list(link.keys()))
        self.assertTrue('primary' in list(link.keys()))

    @patch('api.views.base.BRPApiView.err_rh.get')
    def test_retrieve_pds_links(self, mock_errrh):
        view = PDSAvailableLinksView.as_view()
        url = reverse(
            'pds-links',
            kwargs={
                'pk': self.test_pds.id,
            })
        mock_errrh.return_value = [{
            'typ': 'Test',
            'id': 1,
            'desc': 'lorem ipsum'
        }]
        request = factory.get(url)
        force_authenticate(request, user=self.test_user)
        response = view(
            request,
            pk=self.test_pds.id,
        )
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        # Check link structure
        link = response.data[0]
        self.assertTrue('typ' in list(link.keys()))
        self.assertTrue('id' in list(link.keys()))
        self.assertTrue('desc' in list(link.keys()))

# TODO Test update subject (PDS, Protocol)
# TODO Test add and delete record link
# TODO Test cache behavior.
#
#  * Adding a subject to a protocol should also update the corresponding cache key
#  * Adding a record to a subject should update corresponding cache key (PDS/Protocol?)
