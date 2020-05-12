from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.shortcuts import render
from django.forms.formsets import formset_factory
from django.forms import modelformset_factory
from django.core.exceptions import ObjectDoesNotExist

from brp_admin.forms import ProtocolUserForm, NautilusCredentialsForm, ProtocolForm
from api.models.protocols import ProtocolUser, ProtocolUserCredentials, Protocol, ProtocolDataSource
from django.views.generic.base import TemplateResponseMixin
from django.db.models import Q

class UpdateCredsView(TemplateView):

    template_name = 'update_user_creds.html'

    def __init__(self):
        self.protocol_user_credentials = NautilusCredentialsForm()

    def get(self, request):
        context = {}
        allcreds = ProtocolUserCredentials.objects.all()
        context = {'form1': NautilusCredentialsForm(), 'allcreds': allcreds}

        return render(request, 'update_user_creds.html', context)

    def post(self, request):
        post_data = request.POST
        creds_form = NautilusCredentialsForm(data=request.POST)

        context = {}

        # If the form is valid, clean the data
        # Retrieve data from creds_form containing POST data
        if creds_form.is_valid():
            data = creds_form.cleaned_data
            user=data['user']
            data_source=data['data_source']
            data_source_username=data['data_source_username']
            data_source_password=data['data_source_password']

        # Else display error messages for each field
        else:
            if not (creds_form.non_field_errors()):
                context['form_errors'] = creds_form.errors
                context['form1'] = NautilusCredentialsForm()
                return render(self.request, 'update_user_creds.html', context)

        # If user clicks submit button, go to the confirmation page
        if 'submit_nautilus_creds' in post_data:
            # Create an instance of ProtocolDataSource with the DataSource that the user entered
            # to put into filter since you cannot assign a DataSource to a ProtocolDataSource in the filter
            ds = ProtocolDataSource.objects.get(data_source=data_source)

            # Filter ProtocolUserCredentials objects by the credentials user entered
            credentials = ProtocolUserCredentials.objects.filter(Q(user=user),
            Q(data_source=ds), Q(data_source_username=data_source_username))

            # Update the data_source_password to the new password of objects with these credentials
            credentials.update(data_source_password=data_source_password)

            # Message that the creds were saved, also passing credentials to confirmation.html
            context = {}
            context['message'] = 'credentials saved for ' + str(user)
            context['credentials'] = credentials

            return render(self.request, 'confirmation.html', context)
