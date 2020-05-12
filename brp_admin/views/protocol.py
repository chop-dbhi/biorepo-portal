from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.shortcuts import render
from django.forms.formsets import formset_factory
from django.forms import modelformset_factory
from django.core.exceptions import ObjectDoesNotExist

from brp_admin.forms import ProtocolUserForm, NautilusCredentialsForm, ProtocolUserCredentialsForm
from api.models.protocols import ProtocolUser, ProtocolUserCredentials, Protocol, ProtocolDataSource
from django.db.models import Q

class ProtocolUserView(TemplateView):

    template_name = 'new_protocol_usr.html'

    def __init__(self):
        self.protocol_user_form = ProtocolUserForm()

    def processProtocolUserForm(self, request):

        context = {}

        post_info = request.POST
        protocolUserForm = ProtocolUserForm(data=request.POST)
        self.protocol = post_info['protocol']
        self.user = post_info['user']

        # if form is valid save
        if protocolUserForm.is_valid():
            protocolUserForm.save()
        # if form is not valid - send errors to UI
        if not protocolUserForm.is_valid():
            # ignore non_field_errors, it is okay if protocol user already exists for given protocol
            if not (protocolUserForm.non_field_errors()):
                context['form_errors'] = protocolUserForm.errors
                context['form1'] = ProtocolUserForm()

        return context

    def get(self, request):
        return render(request, 'new_protocol_usr.html', {'form1': ProtocolUserForm()})

    def post(self, request):
        post_data = request.POST
        user = post_data['user']
        protocol = post_data['protocol']

        # if the user is submmitting credentials go to ProtocolUserCredentialForm view
        # to process the user submmision
        if 'submit_creds' in post_data:
            return ProtocolUserCredentialForm.as_view()(self.request, protocol, user)

        context = self.processProtocolUserForm(request)
        if ('form_errors' in context):
            print (context['form_errors'])
            return render(request, 'new_protocol_usr.html', context)

        return ProtocolUserCredentialForm.as_view()(self.request, protocol, user)


class ProtocolUserCredentialForm(TemplateView):

    def getCred_formset(self, protocol, protocol_user, user):
        credentials = ''
        try:
            # if user already has credentials for given protocol, then collect
            # current credentials and pass into form as initial data.
            credentials = ProtocolUserCredentials.objects.filter(protocol=protocol, protocol_user=protocol_user)
            credential_data = [{'protocol': protocol,
                                'protocol_user': protocol_user,
                                'user': user,
                                'data_source': cred.data_source,
                                'data_source_username': cred.data_source_username,
                                'data_source_password': cred.data_source_password}
                               for cred in credentials]

        except(ObjectDoesNotExist):
            pass

        if (credentials):
            credential_form_set = (modelformset_factory(
                ProtocolUserCredentials,
                fields=('data_source', 'data_source_username', 'data_source_password'),
                can_delete=True,
                extra=0))
            self.credential_form_set = credential_form_set

            return credential_form_set(queryset=ProtocolUserCredentials.objects.filter(protocol=protocol, protocol_user=protocol_user))

            # if credentials do not exist for user on given protocol generate an
            # empty form for each datasource available for given protocol
        else:
            empty_credentials = ProtocolDataSource.objects.filter(protocol=protocol)
            credential_data = [{'protocol': protocol,
                                'data_source': item,
                                'user': user,
                                'protocol_user': protocol_user}
                               for item in empty_credentials]
            credential_form_set = (formset_factory(
                ProtocolUserCredentialsForm,
                can_delete=True,
                extra=0))
            self.credential_form_set = credential_form_set
            return credential_form_set(initial=credential_data)

    # get_confirmation_context should be used after protocolUserCredential form is
    # proccesed. It will grab current credentials for user on given protocol to
    # viewed on the UI so user can validate data entry was successful.
    def get_confirmation_context(self, protocol_user, protocol, user):

        protocol_user_cred = ProtocolUserCredentials.objects.filter(protocol=protocol,
                                                                    protocol_user=protocol_user)
        credential_data = [{'data_source': cred.data_source,
                            'data_source_username': cred.data_source_username,
                            'data_source_password': cred.data_source_password}
                           for cred in protocol_user_cred]
        print("credential data")
        print(credential_data)
        context = {}
        context['protocolUserCred'] = credential_data
        context['message'] = 'credentials saved for ' + str(user)
        return context

    def processProtocolUserCredForm(self, request, protocol, protocol_user, user):
        context = {}
        credentials_modified = False
        cred_formset = self.credential_form_set(request.POST)
        for cred_form in cred_formset:
            if cred_form.has_changed() and cred_form.is_valid():
                credentials = cred_form.save(commit=False)
                # before object is saved to the database add procol, user, and
                # protocol_user to object.
                credentials.protocol = protocol
                credentials.user = user
                credentials.protocol_user = protocol_user

                credentials.save()

                # a flag to determine if credentials were modified.
                credentials_modified = True

            if not cred_form.is_valid():
                context['errors'] = cred_formset.errors
        if (credentials_modified):
            context = self.get_confirmation_context(protocol_user, protocol, user)
        else:
            context['message'] = 'credentials not modified for ' + str(user)
        return context

    def get_context_data(self, request):
        request_info = request.POST
        user = request_info['user']
        protocol = request_info['protocol']
        protocol_user = ProtocolUser.objects.get(protocol=protocol, user=user)

        context = {}

        context['cred_formset'] = self.getCred_formset(protocol,
                                                       protocol_user,
                                                       user)
        context['user_str'] = User.objects.get(pk=user)
        context['protocol_str'] = Protocol.objects.get(pk=protocol)
        context['user'] = user
        context['protocol'] = protocol
        print("Context")
        print(context)
        return context

    def get(self, request):
        pass

    def post(self, request, protocol, user):
        post_data = request.POST

        if 'submit_creds' in post_data:

            # set values of fields in form not rendered on UI
            protocol_instance = Protocol.objects.get(pk=protocol)
            user_instance = User.objects.get(pk=user)
            protocol_user_instance = ProtocolUser.objects.get(protocol=protocol_instance, user=user_instance)
            self.getCred_formset(protocol_instance, protocol_user_instance, user_instance)
            context = self.processProtocolUserCredForm(request, protocol_instance, protocol_user_instance, user_instance)
            return render(request, 'confirmation.html', context)

        else:
            context = self.get_context_data(request)
            return render(request, 'protocol_user_credentials.html', context)

class UpdateNautilusCredentialsView(TemplateView):

    template_name = 'update_user_creds.html'

    def __init__(self):
        self.protocol_user_credentials = NautilusCredentialsForm()

    def get(self, request):
        context = {}

        context = {'form1': NautilusCredentialsForm()}

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

class Fn_in_progress(TemplateView):

    template_name = 'in_progress.html'
