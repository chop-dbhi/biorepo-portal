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


class TestUpdateNautilusCredentials(TestCase):

    fixtures = ['unit_test_demo_data']

    def setUp(self):
        postRequest = factory.post(url, {'username': "UnitTestUser",
                                         'password': "anyOldThing"})
        naut(postRequest)

    def test_that_valid_post_data_has_no_errors(self):
        postRequest = factory.post(url, {'username': "UnitTestUser",
                                         'password': "anyOldThing"})
        naut(postRequest)
        self.assertEqual("no errors", extractErrors(str(naut(postRequest).content)))

    def test_that_missing_user_field_has_error(self):
        postRequest = factory.post(url, {'username': "",
                                         'password': "anyOldThing"})
        naut(postRequest)
        self.assertEqual("Please select a user.", extractErrors(str(naut(postRequest).content)))

    def test_that_missing_password_field_has_error(self):
        postRequest = factory.post(url, {'username': "UnitTestUser",
                                         'password': ""})
        naut(postRequest)
        self.assertEqual("Please enter the new password.", extractErrors(str(naut(postRequest).content)))

    def test_that_multiple_empty_fields_combine_errors(self):
        postRequest = factory.post(url, {'username': "",
                                         'password': ""})
        naut(postRequest)
        self.assertEqual("Please select a user.Please enter the new password.", extractErrors(str(naut(postRequest).content)))

# The test below actually checks for multiple factors.
#   First : did the user's credentials actually change?
#   Second: did credentials with a mismatched username field change?
#   Third : did credentials without a password change?
#   Fourth: did non-nautilus credentials get changed?
# The criteria for alteration is that the usernames have to match and the
# password cannot be blank. These different cases are established in the fixtures.
    def test_that_all_relevant_user_credentials_get_changed(self):
        set = ProtocolUserCredentials.objects.filter(data_source_password="anyOldThing",
                                                     data_source_username="UnitTestUser")
        self.assertEqual(1, len(set))

# This test increases scope dynamically with the number of different users.
    def test_that_the_only_effected_user_was_the_one_specified(self):
        allUsers = User.objects.all()
        for user in allUsers:
            set = ProtocolUserCredentials.objects.filter(data_source_password="anyOldThing",
                                                         data_source_username=user.username)
            if user.username == "UnitTestUser":
                self.assertEqual(1, len(set))
            else:
                self.assertEqual(0, len(set))

    def test_that_user_is_alerted_to_mismatched_usernames(self):
        postRequest = factory.post(url, {'username': "UnitTestUser",
                                         'password': "anyOldThing"})
        page = str(naut(postRequest).content)
        start = page.rfind("<p>") + len("<p>")
        stop = page.rfind("</p>")
        self.assertEqual("UnitTestUser: Demonstration Protocol II", page[start:stop])
        # NOTE: fix the method below in parseBRPTemplateHTML.py and adapt this
        # test to use it.
        # extractUserCredentialInformation(page.content)
