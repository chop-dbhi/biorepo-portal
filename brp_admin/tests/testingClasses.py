from django.test import RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from api.models.protocols import ProtocolUserCredentials
from api.models.constants import ProtocolDataSourceConstants

from brp_admin.views.protocol import UpdateNautilusCredentials, ProtocolUserView

from .parseBRPTemplateHTML import *


factory = RequestFactory()
naut = UpdateNautilusCredentials.as_view()
url = reverse('update_nautilus_credentials')
url2 = reverse('UserProtocolCredential')


class ParameterizedTestCase(object):
    def __init__(self, names, params):
        self.params = {}
        for i in range(len(names)):
            self.params[names[i]] = params[i]

    def RunTest(self):
        print("The test: " + self.params["comment"])


class ProtocolErrorMessagesTest(ParameterizedTestCase):
    def __init__(self, name, params):
        super().__init__(name, params)

    def RunTest(self):
        super().RunTest()
        postRequest = factory.post(url, self.params["case"])
        message = extractErrors(str(naut(postRequest).content))
        if not self.params["expectedMessage"] == message:
            print("Was expecting: " + self.params["expectedMessage"] + " but got: " + message)
            return False
        return True


class DatabaseStateTest(ParameterizedTestCase):
    def __init__(self, name, params):
        super().__init__(name, params)

    def RunTest(self):
        super().RunTest()
        count = 0
        set = ProtocolUserCredentials.objects.filter(data_source_password="anyOldThing",
                                                     data_source__driver=ProtocolDataSourceConstants.nautilus_driver)
        user = User.objects.get(pk=self.params["user"])
        print("Set size: " + str(len(set)))
        for i in range(len(set)):
            if str(user) == str(set[i].user):
                count += 1
        if count != self.params["count"]:
            print ("Test failed on user: " + str(user) + " was expecting " + str(self.params["count"]) + " instances, but had " + str(count))
            return False
        return True


class ProtocolRenderTest(ParameterizedTestCase):
        def __init__(self, name, params):
            super().__init__(name, params)

        def RunTest(self):
            super().RunTest()
            request = factory.post(url2, self.params["case"])
            protoView = ProtocolUserView()
            context = protoView.processProtocolUserForm(request)
            if ('form_errors' in context) != self.params["errorExpected"]:
                print("Failed during error check because: " +
                      str(self.params["errorExpected"]) + " != " +
                      str('form_errors' in context))
                print(str(context))
                return False
            return True
