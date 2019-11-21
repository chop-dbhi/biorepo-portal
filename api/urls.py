from django.conf.urls import url, include
from rest_framework import routers
from api import views
router = routers.DefaultRouter()

# Basic root level object views
router.register(r'users', views.UserViewSet)
router.register(r'organizations', views.OrganizationViewSet)
router.register(r'protocols', views.ProtocolViewSet)
router.register(r'datasources', views.DataSourceViewSet)
router.register(r'protocoldatasources', views.PDSViewSet)
# router.register(r'subjFam', views.RelationshipDetailView)

# Wire up our API using automatic URL routing.
# Additionally, we include the login URLs for the browsable API
urlpatterns = [
    # Retrieve all subjects on a Protocol (with their external records)
    url(r'^protocols/(?P<pk>[0-9]+)/subjects/$',
        views.ProtocolSubjectsView.as_view(), name='protocol-subject-list'),
    url(r'^protocols/all/$',
        views.ProtocolAllViewSet.as_view(), name='protocol-all-list'),
    # Create a subject on a Protocol
    url(r'^protocols/(?P<pk>[0-9]+)/subjects/create$',
        views.ProtocolSubjectDetailView.as_view(), name='protocol-subject-create'),
    # Retrieve or Update Subject
    url(r'^protocols/(?P<pk>[0-9]+)/subjects/(?P<subject>[0-9]+)$',
        views.ProtocolSubjectDetailView.as_view(), name='protocol-subject-view'),
    url(r'^protocols/(?P<pk>[0-9]+)/data_sources/$',
        views.ProtocolDataSourceView.as_view(),
        name='protocol-datasources-list'),
    url(r'^protocols/(?P<pk>[0-9]+)/organizations/$',
        views.ProtocolOrganizationView.as_view(),
        name='protocol-organization-list'),
    # get all relationships for a given subject
    url(r'^protocols/(?P<pk>[0-9]+)/subj_fam/subject/(?P<subject>[0-9]+)$',
        views.ProtocolSubjFamDetailView.as_view(),
        name='protocol-subject-subjFam'),
    url(r'^protocols/(?P<pk>[0-9]+)/subj_fam/relationship_id/(?P<relationship_id>[0-9]+)$',
        views.ProtocolSubjFamDetailView.as_view(),
        name='protocol-specific-subjFam'),
    # Create subjFam Relationhip
    url(r'^protocols/(?P<pk>[0-9]+)/subj_fam/create/$',
        views.ProtocolSubjFamDetailView.as_view(),
        name='protocol-subjFam-create'),
    # get all realtionships in a protocol
    url(r'^protocols/(?P<pk>[0-9]+)/subj_fam/$',
        views.ProtocolSubjFamDetailView.as_view(),
        name='protocol-subjFam'),
    url(
        r'^protocoldatasources/(?P<pk>[0-9]+)/subjects/(?P<subject>[0-9]+)/records/$',
        views.PDSSubjectRecordsView.as_view(),
        name='pds-subject-record-list'),
    url(
        r'^protocoldatasources/(?P<pk>[0-9]+)/subjects/(?P<subject>[0-9]+)/record/(?P<record>[0-9]+)/$',
        views.PDSSubjectRecordDetailView.as_view(),
        name='pds-subject-record'),
    url(
        r'^protocoldatasources/(?P<pk>[0-9]+)/subjects/(?P<subject>[0-9]+)/record/(?P<record>[0-9]+)/links/$',
        views.PDSRecordLinkDetailView.as_view(),
        name='pds-subject-record-links'),
    url(
        r'^protocoldatasources/(?P<pk>[0-9]+)/subjects/$',
        views.PDSSubjectView.as_view(),
        name='pds-subject-list'),
    url(
        r'^protocoldatasources/(?P<pk>[0-9]+)/links/$',
        views.PDSAvailableLinksView.as_view(),
        name='pds-links'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # to create a relationship between subjects
    url(r'^subj_fam/create$',
        views.RelationshipDetailView.as_view(),
        name='subjFam-create'),
    # get relationships by subject id
    url(r'^subj_fam/subject_id/(?P<pk>[0-9]+)/$',
        views.RelationshipDetailView.as_view(),
        name='subjFam-get-by-subject-id'),
    # get relationships by protocol
    url(r'^subj_fam/protocol_id/(?P<pk>[0-9]+)/$',
        views.RelationshipDetailView.as_view(),
        name='subjFam-get-by-protocol-id'),
    url(r'^subj_fam/relationship_types/',
        views.RelationshipDetailView.as_view(),
        name='subjFam-get-rel-types'),
    url(r'^subj_fam/relationship_id/(?P<relationship_id>[0-9]+)/$',
        views.ProtocolSubjFamDetailView.as_view(),
        name='delete-subjFam')
]
