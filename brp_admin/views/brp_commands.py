from django.views.generic import TemplateView
from django.shortcuts import render
from api.models.protocols import Protocol
from brp_admin.forms import ProtocolForm, UserForm
from django.core import management

from .base import JenkinsJob

import logging

log = logging.getLogger(__name__)


class CacheSubjects(TemplateView):
    #########################################################################
    # This class will remotely trigger a jenkins job to cache subjectsself.
    # the main command in the jenkins job is:
    # python manage.py cache_subjects <protocol # or 'all'>
    # the name of the jenkins job is: brp-caching-deploy-nightly
    #########################################################################
    def get_context_data(self):
        context = {}
        context['form_title'] = "Cache Subjects"
        context['message1'] = "select a protocol to cache subject in the protocol"
        context['message2'] = "This function will trigger a jenkins job to cache subjects"
        context['form'] = ProtocolForm()
        return context

    def post(self, request):
        protocol = request.POST['protocol']

        try:
            # url must be location of the jenkins job starting with '@' character.
            url = "@jenkins-ops-dbhi.research.chop.edu/view/EiG/job/brp-caching-deploy-nightly/buildWithParameters"

            # job_parameters must be parameters required for the jenkins job_parameters
            if (protocol):
                job_parameters = {"protocol": protocol}
            else:
                job_parameters = {"protocol": "all"}
            job = JenkinsJob(url, job_parameters)
            try:
                response = job.trigger_jenkins_job()
            except:
                context = self.get_context_data()
                context['error'] = "There was an error processing your request"
                log.error("there was an error processing brp-caching jenkins job")
                return render(request, 'form.html', context)

            try:
                if "error" in response:
                    context = self.get_context_data()
                    context['error'] = response['error']
                    log.error("there was an error processing brp-caching jenkins job")
                    return render(request, 'form.html', context)
            except:
                pass

            log.debug("BRP-caching jenkins job was initiated for protocol [{0}].".format(protocol))
            context = {}
            context['message'] = "The job was initiated in jenkins go to https://jenkins-ops-dbhi.research.chop.edu/view/EiG/job/brp-caching-deploy-nightly/ to check status."
            return render(request, 'confirmation.html', context)

        except:
            log.error("there was an error processing brp-caching jenkins job")
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
        try:
            management.call_command('cache_ehb_labels', interactive=True, verbosity=0)
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
