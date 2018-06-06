import pytest

from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.db.models import Q

from brp_admin.views.protocol import UpdateNautilusCredentials, \
                                     ProtocolUserView

from .parseBRPTemplateHTML import *

from api.models.constants import ProtocolDataSourceConstants
from api.models.protocols import DataSource, ProtocolUser, \
                                 ProtocolUserCredentials, \
                                 ProtocolDataSource, Protocol

from unittest.mock import MagicMock


#
# Environmental constants to be used in the tests
#
factory = RequestFactory()
naut = UpdateNautilusCredentials.as_view()
url = reverse('update_nautilus_credentials')


#           UpdateNautilusCredentials LOGIC VALIDATION TESTS
# ----------------------------------------------------------------------
#
databaseCases = (("username", "driver", "password", "datasource_username", "empty", "comment"), [
    ("UnitTestUser", 1, "newPassword", "UnitTestUser", False, "User gets their valid credentials changed."),
    ("UnitTestUser", 2, "newPassword", "UnitTestUser", True, "User's non-nautilus credentials are untouched."),
    ("UnitTestUser", 1, "", "UnitTestUser", False, "User's nautilus credentials with empty password fields are untouched."),
    ("UnitTestUser", 1, "newPassword", "Bob", True, "User's nautilus credentials with mismatched username fields are untouched."),
    ("admin", 1, "newPassword", "admin", True, "Other users credentials are untouched.")
])


@pytest.mark.django_db
@pytest.mark.parametrize(*databaseCases)
def test_database_status(username, driver, password, datasource_username, empty, comment):
    call_command("loaddata", "unit_test_demo_data.json", verbosity=0)
    postRequest = factory.post(url, {'username': "UnitTestUser",
                                     'password': "newPassword"})
    naut(postRequest)
    tempUser = User.objects.get(username=username)
    set = ProtocolUserCredentials.objects.filter(Q(user=tempUser),
                                                 Q(data_source__driver=driver),
                                                 Q(data_source_password=password),
                                                 Q(data_source_username=datasource_username))
    if empty:
        assert len(set) == 0
    else:
        assert len(set) > 0
#
# -----------------------------------------------------------------------
#                                  END


#        UpdateNautilusCredentials ERROR MESSAGE VALIDATION TESTS
# -----------------------------------------------------------------------
#
errorCases = (("case", "expectedMessage", "comment"), [
    ({'username': "UnitTestUser", 'password': "aValidOne"}, "no errors", 'Included both username and password'),
    ({'username': "", 'password': "aValidOne"}, "Please select a user.", 'Only included password.'),
    ({'username': "UnitTestUser", 'password': ""}, "Please enter the new password.", 'Only included username'),
    ({'username': "", 'password': ""}, "Please select a user.Please enter the new password.", 'Left out both username and password')
])


@pytest.mark.django_db
@pytest.mark.parametrize(*errorCases)
def test_error_handling(case, expectedMessage, comment):
    call_command("loaddata", "unit_test_demo_data.json", verbosity=0)
    postRequest = factory.post(url, case)
    assert expectedMessage == extractErrors(str(naut(postRequest).content))
#
# -----------------------------------------------------------------------
#                                   END


#                UpdateNautilusCredentials USER ALERT TEST
# -----------------------------------------------------------------------
#
"""

    We may not need this test case.
    Or perhaps it needs to be reworked.
    If we rework it, we will need to improve the extractUserCredentialInformation
    function within parseBRPTemplateHTML.py

@pytest.mark.django_db
def test_that_user_is_alerted_to_mismatched_usernames():
    call_command("loaddata", "unit_test_demo_data.json", verbosity=0)
    postRequest = factory.post(url, {'username': "UnitTestUser",
                                     'password': "anyOldThing"})
    changed = extractUserCredentialInformation(str(naut(postRequest).content))
    assert len(changed[1]) == 1
"""
#
# -----------------------------------------------------------------------
#                                    END
