import json

from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from ehb_client.requests.pedigree_relationships_handler import PedigreeRelationship
from ehb_client.requests.subject_request_handler import Subject
from .base import BRPApiView
from api.models.protocols import Protocol


class RelationshipDetailView(BRPApiView):
    # will return True if subject inputs are valid
    def check_subject(self, subject_1, subject_2):
        try:
            subject_1_response = self.s_rh.get(id=subject_1)
            subject_2_response = self.s_rh.get(id=subject_2)
        except:
            return {'error': 'Invalid subject Selected'}

        sub1 = json.loads(Subject.json_from_identity(subject_1_response))
        sub2 = json.loads(Subject.json_from_identity(subject_2_response))
        if sub1['id'] is None or sub2['id'] is None:
            return {'error': 'Invalid subject Selected'}
        return True

    # will return true if request body is valid, otherwise will return error
    def validate_req_body(self, relationship):
        try:
            subject_1 = relationship['subject_1']
        except:
            return {'error': 'missing subject_1 from request'}

        try:
            subject_2 = relationship['subject_2']
        except:
            return {'error': 'missing subject_2 from request'}

        try:
            relationship['subject_1_role']
        except:
            return {'error': 'missing subject_1_role from request'}

        try:
            relationship['subject_2_role']
        except:
            return {'error': 'missing subject_2 from request'}

        valid_subjects = self.check_subject(subject_1, subject_2)
        if valid_subjects is not True:
            return (valid_subjects)

        return True

    def post(self, request):
        '''
        Add a subject relationship to the protocol

        Expects a request body of the form:
        {
            "subject_1": 1,
            "subject_2": 2,
            "subject_1_role": 3,
            "subject_2_role": 4,
            "protocol_id": 1
        }
        '''
        relationship = request.data
        req_body_valid = self.validate_req_body(relationship)
        if req_body_valid is not True:
            return Response(req_body_valid, status=400)

        try:
            new_relationship = PedigreeRelationship(
                subject_1=relationship['subject_1'],
                subject_2=relationship['subject_2'],
                subject_1_role=relationship['subject_1_role'],
                subject_2_role=relationship['subject_2_role'],
                protocol_id=relationship['protocol_id']
            )
        except:
            return Response({'error': 'Invalid subject or subject role Selected'}, status=400)

        r = self.relationship_HB_handler.create(new_relationship)[0]
        success = r.get('success')
        errors = r.get('errors')
        relationship = r.get(PedigreeRelationship.identityLabel)

        # Dont proceed if creation was not a success
        if not success:
            try:
                relationship = json.loads(PedigreeRelationship.json_from_identity(relationship))
            except:
                pass  # because either way we are replying with error info
            return Response(
                [{"success": success, "relationship": relationship, "errors": errors}],
                status=422)

        return Response(
            [{"success": success, "relationship": json.loads(PedigreeRelationship.json_from_identity(new_relationship)), "errors": errors}],
            headers={'Access-Control-Allow-Origin': '*'},
            status=200
        )

    def get(self, request, pk):
        # returns list of relationships
        try:
            p = Protocol.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'error': 'Protocol requested not found'}, status=404)
        # TODO: when cache added - check for cache data handleRecordClick
        if p.isUserAuthorized(request.user):
            print (request.data)
