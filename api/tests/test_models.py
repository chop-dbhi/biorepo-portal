from django.test import TestCase
from django.contrib.auth.models import User
from ..models.protocols import Organization, DataSource, Protocol, \
    ProtocolUser
from unittest.mock import MagicMock


class OrganizationTest(TestCase):

    def setUp(self):
        # This also calls out to the eHB to create an org.
        Organization.createEhbInstance = MagicMock(return_value=True)
        Organization.objects.create(name='TestOrg', subject_id_label='MRN')
        Organization.objects.create(name='TestOrg2', subject_id_label='MRN')

    def test_immutable_key(self):
        '''
        Make sure Organization has an immutable key assigned
        '''
        org = Organization.objects.get(name='TestOrg', subject_id_label='MRN')
        # TODO: This should be random. Test with mock?
        # self.assertEqual(org.immutable_key.key, '28ZT3Z8WZ2')

    def test_random_of_immutable_key(self):
        '''
        Assert that the immutable key for each org is different
        '''
        org = Organization.objects.get(name='TestOrg', subject_id_label='MRN')
        org2 = Organization.objects.get(name='TestOrg2', subject_id_label='MRN')
        self.assertTrue(org.immutable_key.key != org2.immutable_key.key)

    def test_org_repr(self):
        org = Organization.objects.get(name='TestOrg', subject_id_label='MRN')
        self.assertEqual(str(org), 'TestOrg')

    def test_org_name(self):
        org = Organization.objects.get(name='TestOrg', subject_id_label='MRN')
        self.assertEqual(org.name, 'TestOrg')

    def test_org_subject_id_label(self):
        org = Organization.objects.get(name='TestOrg', subject_id_label='MRN')
        self.assertEqual(org.subject_id_label, 'MRN')

    def test_get_ehb_service_instance(self):
        '''
        Gets the record for this organization as maintained in the ehb service
        '''
        from ehb_client.requests.organization_request_handler import Organization as eHBOrg
        org = Organization.objects.get(name='TestOrg', subject_id_label='MRN')
        org.getEhbServiceInstance = MagicMock(
            return_value=eHBOrg(
                name='TestOrg',
                subject_id_label='MRN'))
        ehb_instance = org.getEhbServiceInstance()
        self.assertEqual(ehb_instance.name, 'TestOrg')

    def tearDown(self):
        org = Organization.objects.get(name='TestOrg', subject_id_label='MRN')
        org.delete()


class DataSourceTest(TestCase):

    def setUp(self):
        # This also calls out to the eHB to create a DataSource.
        DataSource.createEhbInstance = MagicMock(return_value=True)
        DataSource.objects.create(
            name='TestDataSource',
            url='http://example.com',
            description='A test data source',
            ehb_service_es_id=1)

    def test_get_name(self):
        src = DataSource.objects.get(name='TestDataSource')
        self.assertEqual(src.name, 'TestDataSource')

    def test_representitive_name(self):
        src = DataSource.objects.get(name='TestDataSource')
        self.assertEqual(str(src), 'TestDataSource')

    def test_get_url(self):
        src = DataSource.objects.get(name='TestDataSource')
        self.assertEqual(src.url, 'http://example.com')

    def test_get_description(self):
        src = DataSource.objects.get(name='TestDataSource')
        self.assertEqual(src.description, 'A test data source')

    def test_get_ehb_service_es_id(self):
        src = DataSource.objects.get(name='TestDataSource')
        self.assertEqual(src.ehb_service_es_id, 1)

    def tearDown(self):
        ds = DataSource.objects.get(name='TestDataSource')
        ds.delete()


class ProtocolTest(TestCase):

    def setUp(self):
        # This also calls out to the eHB to create a DataSource.
        self.ds = DataSource.objects.create(
            name='TestDataSource',
            url='http://example.com',
            description='A test data source',
            ehb_service_es_id=1)
        self.user = User.objects.create(
            username='TestUser',
            first_name='John',
            last_name='Doe',
            email='test_user@example.com'
        )
        Protocol.createEhbProtocolGroup = MagicMock()
        self.protocol = Protocol.objects.create(
            name='TestProtocol'
        )

    def test_protocol_group_name(self):
        p = Protocol.objects.get(name='TestProtocol')
        # TODO: This should be random. test with mock?
        # self.assertEqual(p.ehb_group_name(), 'BRP:NLZEPVE41A')

    def tearDown(self):
        p = Protocol.objects.get(name='TestProtocol')
        self.protocol.delete()
        self.user.delete()


class ProtocolDataSourceTest(TestCase):

    def setUp(self):
        # This also calls out to the eHB to create a DataSource.
        pass

    def test_p(self):
        pass

    def tearDown(self):
        pass


class ProtocolDataSourceLinkTest(TestCase):

    def setUp(self):
        # This also calls out to the eHB to create a DataSource.
        pass

    def test_p(self):
        pass

    def tearDown(self):
        pass


class ProtocolUserTest(TestCase):

    def setUp(self):
        # This also calls out to the eHB to create a DataSource.
        pass

    def test_p(self):
        pass

    def tearDown(self):
        pass


class ProtocolUserCredentialsTest(TestCase):

    def setUp(self):
        # This also calls out to the eHB to create a DataSource.
        pass

    def test_p(self):
        pass

    def tearDown(self):
        pass
