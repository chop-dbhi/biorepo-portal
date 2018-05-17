import json
import pytest

from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from brp_admin.views.protocol import UpdateNautilusCredentials, \
                                     ProtocolUserView, \
                                     ProtocolUserCredentialForm
from .parseBRPTemplateHTML import *
from .testingClasses import ProtocolErrorMessagesTest, DatabaseStateTest, \
                            ProtocolRenderTest

from api.models.constants import ProtocolDataSourceConstants
from api.models.protocols import DataSource, ProtocolUser, \
                                 ProtocolUserCredentials, \
                                 ProtocolDataSource, Protocol

from unittest.mock import MagicMock


factory = RequestFactory()
naut = UpdateNautilusCredentials.as_view()
url = reverse('update_nautilus_credentials')
user = None
user2 = None

"""
    Cases for TestUpdateNautilusCredentials
"""
errorCases = (("case", "expectedMessage", "comment"), [
    ({'username': "UnitTestUser", 'password': "aValidOne"}, "no errors", 'Included both username and password'),
    ({'username': "", 'password': "aValidOne"}, "Please select a user.", 'Only included password.'),
    ({'username': "UnitTestUser", 'password': ""}, "Please enter the new password.", 'Only included username'),
    ({'username': "", 'password': ""}, "Please select a user.Please enter the new password.", 'Left out both username and password')
])
databaseCases = (("user", "count", "comment"), [
    (2, 1, "Password has changed on all of user's Nautilus credentials"),
    (2, 1, "Only the user's Nautilus credentials have changed"),
    (2, 1, "Mismatched usernames are not touched"),
    (3, 0, "Other users with Nautilus credentials do not get touched"),
    (4, 0, "Blank usernames do not throw false positives")
])

"""
    Cases for TestProtocolUserView
"""
renderCases = (("case", "errorExpected", "comment"), [
    ({'protocol': 2, 'user': 2, 'role': 0}, False, "Testing that valid input does not raise error"),
    ({'protocol': 2, 'user': 1, 'role': ""}, False, "Testing that missing role coupled with a user that is already on the protocol doesn't throw error"),
    ({'protocol': 2, 'user': 3, 'role': ""}, True, "Testing that missing role throws error"),
    ({'protocol': 2, 'user': "", 'role': 0}, True, "Testing that missing user throws error"),
    ({'protocol': "", 'user': 3, 'role': 0}, True, "Testing that missing protocol throws error")
])


class TestUpdateNautilusCredentials(TestCase):
    fixtures = ['unit_test_demo_data']

    def setUp(self):
        self.errorTests = []
        self.databaseTests = []
        postRequest = factory.post(url, {'username': "UnitTestUser",
                                         'password': "anyOldThing"})
        naut(postRequest)
        for params in errorCases[1]:
            self.errorTests.append(ProtocolErrorMessagesTest(errorCases[0], params))
        for params in databaseCases[1]:
            self.databaseTests.append(DatabaseStateTest(databaseCases[0], params))

    def test_database_status(self):
        for test in self.databaseTests:
            self.assertTrue(test.RunTest())

    def test_error_handling(self):
        for test in self.errorTests:
            self.assertTrue(test.RunTest())


class TestProtocolUserView(TestCase):
    fixtures = ['unit_test_demo_data']

    def setUp(self):
        self.renderTests = []
        for params in renderCases[1]:
            self.renderTests.append(ProtocolRenderTest(renderCases[0], params))

    # @pytest.mark.skip(reason="Found a potential bug")
    def test_processProtocolUserForm(self):
        for test in self.renderTests:
            self.assertTrue(test.RunTest())


class TestProtocolUserCredentialsForm(TestCase):
    fixtures = ['unit_test_demo_data']

    def setUp(self):
        self.renderTests = []

    def test_getCred_formset(self):
        protoForm = ProtocolUserCredentialForm()
        form1 = str(protoForm.getCred_formset(1, 1, 1))
        form2 = str(protoForm.getCred_formset(1, 2, 1))
        form3 = str(protoForm.getCred_formset(1, 3, 1))
        # the cases below makes sure that protocols with users on them create
        # different HTML than those without. It also checks that protocols
        # without a user match create the same form despite which user was queried.
        self.assertEqual(form2, form3)
        self.assertNotEqual(form1, form2)
