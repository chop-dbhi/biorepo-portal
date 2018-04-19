from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from api.models.protocols import Protocol, ProtocolUserCredentials
from brp_admin.forms import ProtocolForm, UserForm, NautilusCredentialForm
from django.core import management
from django.contrib.auth.models import User


class CacheSubjects(TemplateView):
    def get_context_data(self):
        context = {}
        context['form_title'] = "Cache Subjects"
        context['message1'] = "select a protocol to cache subject in the protocol"
        context['message2'] = "This function may take a few minutes, you will receive confirmation shortly"
        context['form'] = ProtocolForm()
        return context

    def post(self, request):
        print(request)
        protocol = request.POST['protocol']
        try:
            if (protocol):
                management.call_command('cache_subjects', protocol, verbosity=0)
            else:
                management.call_command('cache_subjects', "all", verbosity=0)
            context = {}
            context['message'] = "Caching complete"
            return render(request, 'confirmation.html', context)
        except(Exception):
            context = self.get_context_data()
            context['error'] = "There was an error processing your request"
            return render(request, 'form.html', context)

    def get(self, request):
        context = self.get_context_data()
        return render(request, 'form.html', context)

class UpdateNautilusCredentials(TemplateView):
    """
        This generates the logic and display information for changing the
    """
    def get_context_data(self):
        context = {}
        context['form_title'] = "Update Nautilus Credentials"
        context['message1'] = "Update a user's Nautilus credentials"
        context['message2'] = ""
        context['form'] = NautilusCredentialForm()
        return context

    def post(self, request):
        context = {}
        usernum = request.POST['username']
        password = request.POST['password']
        if (usernum and password):
            user = User.objects.get(pk=usernum)
            context = {}
            #context = self.get_context_data()
            set = ProtocolUserCredentials.objects.filter(user=user, data_source__driver=0)
            set.update(data_source_password=password)
            context['message'] = "Altered the following entries:\n"
            for ent in set:
                context['message'] += str(user) + ": " + str(ent.protocol.name) + "\n"
            return render(request, 'confirmation.html', context)
        elif (usernum):
            user = User.objects.get(pk=usernum)
            context = self.get_context_data()
            context['error'] = "Please include the new password"
            return render(request, 'form.html', context)
        elif (password):
            context = self.get_context_data()
            context['error'] = "Please include the user you want to edit"
            return render(request, 'form.html', context)
        else:
            context = self.get_context_data()
            context['error'] = "Please include literally anything"
            return render(request, 'form.html', context)

    def get(self, request):
        context = self.get_context_data()
        return render(request, 'form.html', context)

class ReactivateUsers(TemplateView):

    def get_context_data(self):
        context = {}
        context['form_title'] = "Reactivate User"
        context['message1'] = "select a user to Reactivate"
        context['message2'] = "This function may take a few seconds, you will receive confirmation shortly"
        context['form'] = UserForm()
        return context

    def post(self, request):
        context = {}
        user = request.POST['user']
        if (user):
            try:
                management.call_command('reactivate_user', user)
                context['message'] = "User Reactivated"
                return render(request, 'confirmation.html', context)
            except(Exception):
                context = self.get_context_data()
                context['error'] = "there was an error processing your request"
                return render(request, 'form.html', context)
        else:
            context = self.get_context_data()
            context['error'] = "please select a user"
            return render(request, 'form.html', context)

    def get(self, request):
        context = self.get_context_data()
        return render(request, 'form.html', context)


class CacheLabels(TemplateView):
    def get_context_data(self):
        context = {}
        context['form_title'] = "Cache labels"
        context['message1'] = "select submit to cache all ehb labels"
        context['message2'] = "This function may take a few minutes, you will receive confirmation shortly"
        return context

    def post(self, request):
        print(request)
        try:
            management.call_command('cache_ehb_labels', verbosity=0)
            context = {}
            context['message'] = "Caching complete"
            return render(request, 'confirmation.html', context)
        except(Exception):
            context = self.get_context_data()
            context['error'] = "There was an error processing your request"
            return render(request, 'form.html', context)

    def get(self, request):
        context = self.get_context_data()
        return render(request, 'form.html', context)
