import json

from rest_framework.response import Response

from ehb_client.requests.pedigree_relationship_handler import PedigreeRelationship
from .base import BRPApiView


class RelationshipDetailView(BRPApiView):
    def check_subject(self, subject_1, subject_2):
        try:
            self.s_rh.get(id=subject_1)
            self.s_rh.get(id=subject_2)
        except:
            return Response({'error': 'Invalid subject Selected'}, status=400)

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

        new_relationship = PedigreeRelationship(
            subject_1=relationship['subject_1'],
            subject_2=relationship['subject_2'],
            subject_1_role=relationship['subject_1_role'],
            subject_2_role=relationship['subject_2_role'],
            protocol_id=relationship['protocol_id']
        )
        r = self.relationship_HB_handler.create(new_relationship)[0]
        success = r.get('success')
        errors = r.get('errors')
        relationship = r.get(PedigreeRelationship.identityLabel)

        # Dont proceed if creation was not a success
        if not success:
            relationship = json.loads(PedigreeRelationship.json_from_identity(relationship))
            return Response([success, relationship, errors], status=422)

        return Response(
            [success, relationship, errors],
            headers={'Access-Control-Allow-Origin': '*'},
            status=200
        )

    def get(self):
        pass
