from django.test import TestCase
from django.contrib.auth.models import User

from brp_admin.forms import NautilusCredentialForm
from brp_admin.views.protocol import UpdateNautilusCredentials
from api.models.constants import ProtocolDataSourceConstants
from api.models.protocols import DataSource, ProtocolUser, ProtocolUserCredentials, ProtocolDataSource, Protocol, User

from unittest.mock import MagicMock
import pytest

# Create your tests here.
class UpdateNautilusCredentialsTest(TestCase):

    def setUp(self):
        DataSource.createEhbInstance = MagicMock(return_value=True)
        Protocol.createEhbProtocolGroup = MagicMock()

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
            data_source_username="unitName",
            data_source_password="unitPassword"
            )
        ProtocolUserCredentials.objects.create(
            protocol=self.protocol,
            data_source=self.protocoldatasource2,
            user=self.user,
            protocol_user=self.protocoluser,
            data_source_username="unitName",
            data_source_password="unitPassword"
            )
        ProtocolUserCredentials.objects.create(
            protocol=self.protocol,
            data_source=self.protocoldatasource3,
            user=self.user,
            protocol_user=self.protocoluser,
            data_source_username="unitName",
            data_source_password="unitPassword"
            )
        ProtocolUserCredentials.objects.create(
            protocol=self.protocol,
            data_source=self.protocoldatasource2,
            user=self.user2,
            protocol_user=self.protocoluser,
            data_source_username="unitName",
            data_source_password="unitPassword"
            )
        ProtocolUserCredentials.objects.create(
            protocol=self.protocol,
            data_source=self.protocoldatasource,
            user=self.user2,
            protocol_user=self.protocoluser,
            data_source_username="unitName"
            )
        """

            This case breaks the database...

        ProtocolUserCredentials.objects.create(
            protocol=self.protocol,
            data_source=self.protocoldatasource3,
            protocol_user=self.protocoluser,
            data_source_username="unitName2",
            data_source_password="unitPassword"
            )
        """
        """
            All tests require this change and the below updates so I moved them into the setup.
        """
        set = ProtocolUserCredentials.objects.filter(user=self.user, data_source__driver=ProtocolDataSourceConstants.nautilus_driver)
        set.update(data_source_password="newPassword")

        self.protocolusercredentials = ProtocolUserCredentials.objects.get(user=self.user, data_source=self.protocoldatasource)
        self.protocolusercredentials2 = ProtocolUserCredentials.objects.get(user=self.user, data_source=self.protocoldatasource2)
        self.protocolusercredentials3 = ProtocolUserCredentials.objects.get(user=self.user, data_source=self.protocoldatasource3)
        self.protocolusercredentials4 = ProtocolUserCredentials.objects.get(user=self.user2, data_source=self.protocoldatasource2)
        self.protocolusercredentials5 = ProtocolUserCredentials.objects.get(user=self.user2, data_source=self.protocoldatasource)
        """

            This case breaks the database...

        self.protocolusercredentials6 = ProtocolUserCredentials.objects.get(data_source_username="unitName2", data_source=self.protocoldatasource3)
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

    @pytest.mark.skip(reason="This particular test is impossible because not adding a user breaks the database.")
    def test_that_blank_user_fields_do_not_throw_false_positives(self):
        self.assertNotEqual(self.protocolusercredentials6.data_source_password, "newPassword")

    @pytest.mark.skip(reason="For debugging output only")
    def test_DEBUGGING_MODE(self):
        print("Datasource: " + str(self.datasource))
        print("Protocol: " + str(self.protocol))
        print("User: " + str(self.user))
        print("ProtocolUser: " + str(self.protocoluser))
        print("ProtocolDataSource: " + str(self.protocoldatasource))
        print("ProtocolUserCredentials: " + str(self.protocolusercredentials))
        pass
