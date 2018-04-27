from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views.protocol import Fn_in_progress, ProtocolUserView, UpdateNautilusCredentials

from .views.brp_commands import CacheSubjects, ReactivateUsers, CacheLabels


urlpatterns = [
    url(
        r'^new_protocol_usr/$',
        login_required(ProtocolUserView.as_view()),
        name='UserProtocolCredential'),
    url(
        r'^fn_in_progress/$',
        login_required(Fn_in_progress.as_view())),
    url(
        r'^cache_subjects/$',
        login_required(CacheSubjects.as_view()),
        name='cache_subjects'),
    url(
        r'^reactivate_user/$',
        login_required(ReactivateUsers.as_view()),
        name='cache_subjects'),
    url(
        r'^cache_labels/$',
        login_required(CacheLabels.as_view()),
        name='cache_labels'),
    url(
        r'^update_nautilus_credentials/$',
        login_required(UpdateNautilusCredentials.as_view()),
        name='update_nautilus_credentials'),
]
