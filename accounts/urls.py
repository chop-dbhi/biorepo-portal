from django.conf.urls import url
from django.views.generic import TemplateView
# views
from registration.views import register, verify, moderate, moderate_list

urlpatterns = [
    url(r'^register/$', register, name='register'),
    url(r'^register/complete/$', TemplateView.as_view(template_name='registration/registration_complete.html'),
        name='registration-complete'),
    url(r'^verify/(?P<activation_key>\w+)/$', verify, name='verify-registration'),
    url(r'^moderate/(?P<activation_key>\w+)/$', moderate, name='moderate-registration'),
    url(r'^moderate/$', moderate_list, name='moderate-registration-list'),
    url(r'^password_reset/$', TemplateView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
]
