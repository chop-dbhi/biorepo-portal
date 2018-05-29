import json

from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.management import call_command

from brp_admin.views.protocol import UpdateNautilusCredentials, ProtocolUserView

from api.models.constants import ProtocolDataSourceConstants
from api.models.protocols import DataSource, ProtocolUser, \
                                 ProtocolUserCredentials, \
                                 ProtocolDataSource, Protocol

from .parseBRPTemplateHTML import *

from unittest.mock import MagicMock
import pytest


factory = RequestFactory()
naut = UpdateNautilusCredentials.as_view()
url = reverse('update_nautilus_credentials')


databaseCases = (("case", "expectedOutcome", "comment"), [
    ("UnitTestUser", 1, 'User with change'),
    ("UnitTestUser1", 0, 'User without change'),
    ("UnitTestUser2", 0, 'User without change'),
    ("admin", 0, 'User without change')
])


@pytest.mark.django_db
@pytest.mark.parametrize(*databaseCases)
def test_database_status(case, expectedOutcome, comment):
    call_command("loaddata", "unit_test_demo_data.json", verbosity=0)
    postRequest = factory.post(url, {'username': "UnitTestUser",
                                     'password': "anyOldThing"})
    naut(postRequest)
    set = ProtocolUserCredentials.objects.filter(data_source_password="anyOldThing",
                                                 data_source_username=case)
    assert len(set) == expectedOutcome


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


@pytest.mark.django_db
def test_that_user_is_alerted_to_mismatched_usernames():
    call_command("loaddata", "unit_test_demo_data.json", verbosity=0)
    postRequest = factory.post(url, {'username': "UnitTestUser",
                                     'password': "anyOldThing"})
    changed = extractUserCredentialInformation(str(naut(postRequest).content))
    assert len(changed[1]) == 1
