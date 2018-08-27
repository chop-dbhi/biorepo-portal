import logging
import json
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist

from .base import BRPApiView

from api.models.protocols import ProtocolDataSource, ProtocolUserCredentials
from api.serializers import eHBSubjectSerializer, \
    ProtocolDataSourceSerializer

from ehb_client.requests.exceptions import PageNotFound
from ehb_client.requests.external_record_request_handler import ExternalRecord

from rest_framework.response import Response
from rest_framework import viewsets

logger = logging.getLogger(__name__)


class PDSViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows protocols to be viewed.
    """
    queryset = ProtocolDataSource.objects.all()
    serializer_class = ProtocolDataSourceSerializer

    def list(self, request, *args, **kwargs):
        pds = []
        for p in ProtocolDataSource.objects.all():
            if request.user in p.protocol.users.all():
                pds.append(ProtocolDataSourceSerializer(p, context={'request': request}).data)

        return Response(pds)


class PDSRecordLinkDetailView(BRPApiView):
    def get(self, request, pk, subject, record, *args, **kwargs):
        '''Retrieve links for a given record
        '''
        try:
            pds = ProtocolDataSource.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'error': 'ProtocolDatasource requested not found'}, status=404)

        if pds.protocol.isUserAuthorized(request.user):
            try:
                res = self.er_rh.get(id=record, links=True)
                return Response(res)
            except PageNotFound:
                return Response([])
        else:
            return Response(
                {"detail": "You are not authorized to view record links from this protocol"},
                status=403
            )

    def post(self, request, pk, subject, record, *args, **kwargs):
        '''Create a link between two subject records in the eHB
        '''
        try:
            pds = ProtocolDataSource.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'error': 'ProtocolDatasource requested not found'}, status=404)

        if pds.protocol.isUserAuthorized(request.user):
            data = request.data
            primary_rec = data['primaryRecord']
            secondary_rec = data['secondaryRecord']
            link_type = data['linkType']
            # Serialize
            primary_rec = ExternalRecord.identity_from_json(json.dumps(primary_rec))
            secondary_rec = ExternalRecord.identity_from_json(json.dumps(secondary_rec))
            res = self.er_rh.link(primary_rec, secondary_rec, link_type)
            if res['success']:
                return Response(res)
            else:
                return Response({'success': False, 'error': res['error']}, status=422)
            return Response({'success': False, 'error': 'Unknown Error'}, status=422)

    def delete(self, request, pk, subject, record, *args, **kwargs):
        '''Delete a link between two subject records in the eHB
        '''
        try:
            pds = ProtocolDataSource.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'error': 'ProtocolDatasource requested not found'}, status=404)

        if pds.protocol.isUserAuthorized(request.user):
            data = json.loads(request.body.decode('utf-8'))
            primary_rec = data['primaryRecord']
            link_id = data['linkId']
            # Serialize
            primary_rec = ExternalRecord.identity_from_json(json.dumps(primary_rec))
            res = self.er_rh.unlink(primary_rec, link_id)
            if res['success']:
                return Response(res)
            return Response({'success': False}, status=422)


class PDSAvailableLinksView(BRPApiView):
    def get(self, request, pk, *args, **kwargs):
        try:
            pds = ProtocolDataSource.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'error': 'ProtocolDatasource requested not found'}, status=404)

        if pds.protocol.isUserAuthorized(request.user):
            res = self.err_rh.get()
            if pds.driver_configuration != '':
                dc = json.loads(pds.driver_configuration)
            else:
                return Response([])
            links = []
            if not res:
                return Response([])
            for link in res:
                if 'links' in list(dc.keys()) and link['id'] in dc['links']:
                    links.append(link)
            return Response(links)


class PDSSubjectRecordDetailView(BRPApiView):

    def get(self, request, pk, subject, record, *args, **kwargs):
        try:
            pds = ProtocolDataSource.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'error': 'ProtocolDatasource requested not found'}, status=404)

        if pds.protocol.isUserAuthorized(request.user):
            res = self.er_rh.get(id=record)
            d = json.loads(res.json_from_identity(res))
            return Response(d)
        else:
            return Response(
                {"detail": "You are not authorized to view records from this protocol"},
                status=403
            )

    def put(self, request, pk, subject, record, *args, **kwargs):
        '''
        Updates the subject record. Currently only changing the records label is
        supported.

        If successful the updated external record is returned
        '''
        try:
            pds = ProtocolDataSource.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'error': 'ProtocolDatasource requested not found'}, status=404)

        if pds.protocol.isUserAuthorized(request.user):
            ex_rec = json.loads(request.body.decode('utf-8'))
            rec = self.er_rh.get(id=ex_rec['id'])
            rec.label_id = ex_rec['label_id']
            rec.modified = datetime.now()
            res = self.er_rh.update(rec)[0]
            if res['success']:
                ex_rec = res['external_record']
                return Response(json.loads(ex_rec.json_from_identity(ex_rec)))
            else:
                return Response({
                    'success': res['success'],
                    'errors': res['errors']},
                    status=422)
        else:
            return Response(
                {"detail": "You are not authorized to view records from this protocol"},
                status=403
            )


class PDSSubjectRecordsView(BRPApiView):

    def get(self, request, pk, subject, *args, **kwargs):
        try:
            pds = ProtocolDataSource.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'error': 'ProtocolDatasource requested not found'}, status=404)

        ex_recs = []

        if pds.protocol.isUserAuthorized(request.user):
            try:
                ProtocolUserCredentials.objects.get(
                    protocol=pds.protocol, data_source=pds, user=request.user)
            except ProtocolUserCredentials.DoesNotExist:
                return Response([], status=403)

            res = self.er_rh.query({
                "subject_id": subject,
                "external_system_id": pds.data_source.ehb_service_es_id,
                "path": pds.path
            })[0]

            if res["success"]:
                for ex_rec in res["external_record"]:
                    t = json.loads(ex_rec.json_from_identity(ex_rec))
                    ex_recs.append(t)

        return Response(sorted(
            ex_recs, key=lambda ex_recs: ex_recs["created"]))


class PDSSubjectView(BRPApiView):

    def buildQueryParams(self, subjects, es_id, path):
        params = []
        for subject in subjects:
            params.append({
                "subject_id": subject.id,
                "external_system_id": es_id,
                "path": path
            })
        return params

    def get(self, request, pk, *args, **kwargs):
        """
        Returns a list of subjects associated with the protocol datasource and
        their external records
        """
        try:
            pds = ProtocolDataSource.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'error': 'ProtocolDatasource requested not found'}, status=404)

        subjects = pds.protocol.getSubjects()
        organizations = pds.protocol.organizations.all()
        if pds.protocol.isUserAuthorized(request.user):
            if subjects:
                params = self.buildQueryParams(subjects, pds.data_source.ehb_service_es_id, pds.path)
                # TODO: Cache check
                res = self.er_rh.query(*params)
                subjects = [eHBSubjectSerializer(subject).data for subject in subjects]

                ehb_orgs = []
                # We can't rely on Ids being consistent across apps so we must
                # append the name here for display downstream.
                for o in organizations:
                    ehb_orgs.append(o.getEhbServiceInstance())
                for sub in subjects:
                    sub.update({"external_records": []})
                    sub['organization'] = sub['organization_id']
                    sub.pop('organization_id')
                    for ehb_org in ehb_orgs:
                        if sub['organization'] == ehb_org.id:
                            sub['organization_name'] = ehb_org.name
                for ex_rec in res:
                    if ex_rec["success"]:
                        for sub in subjects:
                            for rec in ex_rec["external_record"]:
                                if rec.subject_id == sub["id"]:
                                    sub["external_records"].append(json.loads(rec.json_from_identity(rec)))

                return Response({
                    "subjects": subjects,
                    "count": len(subjects)})
            else:
                return Response({
                    "subjects": [],
                    "count": 0})
        else:
            return Response(
                {"detail": "You are not authorized to view subjects from this protocol datasource"},
                status=403
            )
