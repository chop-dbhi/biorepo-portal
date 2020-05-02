from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.shortcuts import render
from django.forms.formsets import formset_factory
from django.forms import modelformset_factory
from django.core.exceptions import ObjectDoesNotExist

from brp_admin.forms import ProtocolUserForm, ProtocolUserCredentialsForm, ProtocolForm
from api.models.protocols import ProtocolUser, ProtocolUserCredentials, Protocol, ProtocolDataSource
from django.views.generic.base import TemplateResponseMixin
from django.db.models import F

class UpdateCredsView(TemplateView):

    template_name = 'update_user_creds.html'

    def __init__(self):
        self.protocol_user_credentials = ProtocolUserCredentialsForm()

    def get(self, request):
        context = {}
        allcreds = ProtocolUserCredentials.objects.all()
        context = {'form1': ProtocolUserCredentialsForm(), 'allcreds': allcreds}

        return render(request, 'update_user_creds.html', context)

    def post(self, request):
        post_data = request.POST
        creds_form = ProtocolUserCredentialsForm(data=request.POST)

        context = {}

        # If the form is valid, clean the data
        # Retrieve data and set database records with new data
        if creds_form.is_valid():
            data = creds_form.cleaned_data
            protocol=data['protocol']
            user=data['user']
            protocol_user=data['protocol_user']
            data_source=data['data_source']
            data_source_username=data['data_source_username']
            data_source_password=data['data_source_password']

        # If user clicks submit button, go to the confirmation page
        if 'submit_nautilus_creds' in post_data:
            # Filter ProtocolUserCredentials objects by the credentials user entered
            # Update the data_source_password to the new password of objects with these credentials
            credentials = ProtocolUserCredentials.objects.filter(protocol=protocol,user=user,protocol_user=protocol_user,
            data_source=data_source,data_source_username=data_source_username).update(data_source_password=data_source_password)


        context = {'protocol':protocol, 'user': user, 'protocol_user':protocol_user,
        'data_source':data_source,'data_source_username':data_source_username, 'data_source_password': data_source_password}

        return render(self.request, 'confirm_nautilus_creds.html', context)
