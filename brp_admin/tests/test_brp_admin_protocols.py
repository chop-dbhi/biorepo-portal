import json

from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.urlresolvers import reverse

from rest_framework.test import APIRequestFactory, APITestCase, \
                                force_authenticate

from brp_admin.views.protocol import UpdateNautilusCredentials, ProtocolUserView

from api.models.constants import ProtocolDataSourceConstants
from api.models.protocols import DataSource, ProtocolUser, \
                                 ProtocolUserCredentials, \
                                 ProtocolDataSource, Protocol

from unittest.mock import MagicMock
import pytest

restFactory = APIRequestFactory()
djangoFactory = RequestFactory()
client = Client()

class BRPTestCase(APITestCase):

    fixtures = ['demo_data']

    def setUp(self):
        self.test_user = User.objects.get(username='admin')
        self.test_protocol = Protocol.objects.get(name='Demonstration Protocol')

        DataSource.objects.create(
            name='UnitTestDataSource',
            url='http://example.com',
            description='A test data source',
            ehb_service_es_id=1
            )
        self.datasource = DataSource.objects.get(name='UnitTestDataSource')

        Protocol.objects.create(
            name="UnitTestProtocol"
            )
        self.protocol = Protocol.objects.get(name='UnitTestProtocol')

        User.objects.create(
            username='UnitTestUser',
            first_name='UnitJohn',
            last_name='UnitDoe',
            email='unit_test_user@example.com'
            )
        self.user = User.objects.get(username='UnitTestUser')
        User.objects.create(
            username='UnitTestUser2',
            first_name='UnitJane',
            last_name='UnitDoe',
            email='unit_test_user@example.com'
            )
        self.user2 = User.objects.get(username='UnitTestUser2')
        User.objects.create(
            username='UnitTestUser3',
            first_name='UnitJim',
            last_name='UnitDoe',
            email='unit_test_user@example.com'
            )
        self.user3 = User.objects.get(username='UnitTestUser3')

        ProtocolUser.objects.create(
            protocol=self.protocol,
            user=self.user,
            role=1
            )
        self.protocoluser = ProtocolUser.objects.get(protocol=self.protocol)

        ProtocolDataSource.objects.create(
            protocol=self.protocol,
            data_source=self.datasource,
            path="UNIT TEST SUBJECTS",
            driver=1,
            driver_configuration="\{\}",
            display_label="UNIT TEST PROTOCOL DATA SOURCE",
            max_records_per_subject=-1
            )
        self.protocoldatasource = ProtocolDataSource.objects.get(display_label="UNIT TEST PROTOCOL DATA SOURCE")
        ProtocolDataSource.objects.create(
            protocol=self.protocol,
            data_source=self.datasource,
            path="UNIT TEST SUBJECTS 2",
            driver=1,
            driver_configuration="\{\}",
            display_label="UNIT TEST PROTOCOL DATA SOURCE 2",
            max_records_per_subject=-1
            )
        ProtocolDataSource.objects.create(
            protocol=self.protocol,
            data_source=self.datasource,
            path="UNIT TEST SUBJECTS 3",
            driver=2,
            driver_configuration="\{\}",
            display_label="UNIT TEST PROTOCOL DATA SOURCE 3",
            max_records_per_subject=-1
            )
        self.protocoldatasource2 = ProtocolDataSource.objects.get(display_label="UNIT TEST PROTOCOL DATA SOURCE 2")
        self.protocoldatasource3 = ProtocolDataSource.objects.get(display_label="UNIT TEST PROTOCOL DATA SOURCE 3")

        ProtocolUserCredentials.objects.create(
            protocol=self.protocol,
            data_source=self.protocoldatasource,
            user=self.user,
            protocol_user=self.protocoluser,
            data_source_username=self.user.username,
            data_source_password="unitPassword"
            )
        ProtocolUserCredentials.objects.create(
            protocol=self.protocol,
            data_source=self.protocoldatasource2,
            user=self.user,
            protocol_user=self.protocoluser,
            data_source_username=self.user.username,
            data_source_password="unitPassword"
            )
        ProtocolUserCredentials.objects.create(
            protocol=self.protocol,
            data_source=self.protocoldatasource3,
            user=self.user,
            protocol_user=self.protocoluser,
            data_source_username=self.user.username,
            data_source_password="unitPassword"
            )
        ProtocolUserCredentials.objects.create(
            protocol=self.protocol,
            data_source=self.protocoldatasource2,
            user=self.user2,
            protocol_user=self.protocoluser,
            data_source_username=self.user2.username,
            data_source_password="unitPassword"
            )
        ProtocolUserCredentials.objects.create(
            protocol=self.protocol,
            data_source=self.protocoldatasource,
            user=self.user2,
            protocol_user=self.protocoluser,
            data_source_username=self.user2.username
            )
        ProtocolUserCredentials.objects.create(
            protocol=self.protocol,
            data_source=self.protocoldatasource,
            user=self.user3,
            protocol_user=self.protocoluser,
            data_source_password="unitPassword"
            )


class UpdateNautilusCredentialsTest(BRPTestCase):

    """
    def setUp(self):
        #DataSource.createEhbInstance = MagicMock(return_value=True)
        #Protocol.createEhbProtocolGroup = MagicMock()
        #self.factory = RequestFactory()



        set = ProtocolUserCredentials.objects.filter(user=self.user, data_source__driver=ProtocolDataSourceConstants.nautilus_driver)
        set.update(data_source_password="newPassword")
        """

    def test_post_reply(self):
        url = reverse('update_nautilus_credentials')
        #url = reverse('UserProtocolCredential')
        #postRequest = restFactory.post(url, {'username': self.test_user.username, 'password': "anyOldThing", 'user': self.test_user, 'protocol': self.test_protocol})
        postRequest = restFactory.post(url, {'username': self.user.username, 'password': "anyOldThing"})
        #testView = UpdateNautilusCredentials.as_view()
        #testView = ProtocolUserView.as_view()
        #force_authenticate(postRequest, user=self.user)
        #print(str(self.test_user))
        #print(str(postRequest))
        #print(str(testView))
        #response = testView(postRequest)
        response = client.post(url, {'username': self.user.username, 'password': "something"})
        naut = UpdateNautilusCredentials()
        try:
            naut.post(postRequest)
        except(Exception):
            pass
        print("")
        for key, val in response.items():
            print(str(key) + ": " + str(val))
        print(str(response.status_code))
        print("Content  : " + str(response.content))
        print("Templates: " + str(response.templates))
        print("Context  : " + str(response.context))
        otherOtherSet = ProtocolUserCredentials.objects.all()
        otherSet = ProtocolUserCredentials.objects.filter(data_source__driver=ProtocolDataSourceConstants.nautilus_driver)
        set = ProtocolUserCredentials.objects.filter(data_source_password="anyOldThing", data_source__driver=ProtocolDataSourceConstants.nautilus_driver)
        print(str(otherOtherSet))
        print(str(otherSet))
        print(str(set))
        pass

    """
    def test_that_protocoldatasource_has_nautilus_driver(self):
        self.assertEqual(self.protocoldatasource.driver, ProtocolDataSourceConstants.nautilus_driver)

    def test_that_nautilus_password_is_changed(self):
        self.assertEqual(self.protocolusercredentials2.data_source_password, "newPassword")

    def test_that_non_nautilus_passwords_are_left_alone(self):
        self.assertNotEqual(self.protocolusercredentials3.data_source_password, "newPassword")

    def test_that_other_users_nautilus_credentials_are_left_alone(self):
        self.assertNotEqual(self.protocolusercredentials4.data_source_password, "newPassword")

    def test_that_all_of_users_nautilus_credentials_are_updated(self):
        self.assertEqual(self.protocolusercredentials.data_source_password, "newPassword")
        self.assertEqual(self.protocolusercredentials2.data_source_password, "newPassword")

    def test_that_user_credentials_with_blank_passwords_are_left_alone(self):
        self.assertNotEqual(self.protocolusercredentials5.data_source_password, "newPassword")
    """

    @pytest.mark.skip(reason="For debugging output only")
    def test_DEBUGGING_MODE(self):
        print("Datasource: " + str(self.datasource))
        print("Protocol: " + str(self.protocol))
        print("User: " + str(self.user))
        print("Protocol: " + str(self.protocol))
        print("ProtocolUser: " + str(self.protocoluser))
        print("ProtocolDataSource: " + str(self.protocoldatasource))
        print("ProtocolUserCredentials: " + str(self.protocolusercredentials))
        pass
