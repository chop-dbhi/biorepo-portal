from api.models.protocols import ProtocolDataSource
from django.http import HttpResponseForbidden, HttpResponseNotFound


class CheckPdsCredentialsMiddleware(object):

    def process_view(self, request, view_func, *args):
        if request.user.is_authenticated:
            view_args_dict = args[1]
            if 'pds_id' in view_args_dict:
                try:
                    pds = ProtocolDataSource.objects.get(pk=view_args_dict['pds_id'])
                except ProtocolDataSource.DoesNotExist:
                    return HttpResponseNotFound()

                if (pds.protocol.isUserAuthorized(request.user)):
                    return
                return HttpResponseForbidden()
