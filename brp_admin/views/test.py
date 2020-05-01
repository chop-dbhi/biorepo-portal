from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.shortcuts import render
from django.forms.formsets import formset_factory
from django.forms import modelformset_factory
from django.core.exceptions import ObjectDoesNotExist

from brp_admin.forms import ProtocolUserForm, ProtocolUserCredentialsForm, ProtocolForm
from api.models.protocols import ProtocolUser, ProtocolUserCredentials, Protocol, ProtocolDataSource
from django.views.generic.base import TemplateResponseMixin

class UpdateCredsView(TemplateView):

    template_name = 'update_user_creds.html'

    def __init__(self):
        self.protocol_user_credentials = ProtocolUserCredentialsForm()

    def processCredsForm(self, request):

        context = {}
        creds_form = ProtocolUserCredentialsForm(data=request.POST)

        # If the form is valid and the method is POST
        if creds_form.is_valid() and request.method == 'POST':
            # Clean the data
            data = creds_form.cleaned_data

            # Filter based on the credentials the user gave in the input
            credentials = ProtocolUserCredentials.objects.filter(protocol=data['protocol'],user=data['user'],
            protocol_user=data['protocol_user'],
            data_source=data['data_source'],data_source_username=data['data_source_username'])

            data_source_password = data['data_source_password']

            # Iterate through the queryset, set the old password to the new password user gave
            # for each password in every object with the criteria above
            for cred in credentials:
                cred.data_source_password = data_source_password

        if not creds_form.is_valid():
            if not (creds_form.non_field_errors()):
                context['form_errors'] = creds_form.errors
                context['form1'] = creds_form


    def get(self, request):
        context = {}
        allcreds = ProtocolUserCredentials.objects.all()
        context = {'form1': ProtocolUserCredentialsForm()}

        return render(request, 'update_user_creds.html', context)

    def post(self, request):
        post_data = request.POST
        context = {}

        # If user clicks submit button, go to the confirmation page
        if 'submit_nautilus_creds' in post_data:
            form = self.processCredsForm(request)
            context = {'form': form}
            return render(request, 'confirm_nautilus_creds.html', context)
