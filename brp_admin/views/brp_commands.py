from django.views.generic import TemplateView
from django.shortcuts import render
from api.models.protocols import Protocol
from brp_admin.forms import ProtocolForm, UserForm
from django.core import management


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
