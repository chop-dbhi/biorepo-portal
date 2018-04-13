from django.http import HttpResponse
from django.core.cache import cache
from django.template import RequestContext, loader
from redis.exceptions import ConnectionError
from api.models.protocols import ProtocolDataSource
from rest_framework.authtoken.models import Token
import datetime

import logging

log = logging.getLogger(__name__)


class MaintenanceMiddleware(object):

    def process_request(self, request):
        try:
            m_mode = cache.get('maintenance_mode', False)
        except ConnectionError:
            m_mode = False
        if m_mode:
            t = loader.get_template('maintenance.html')
            return HttpResponse(t.render(RequestContext(request)))


class LoggingMiddleware(object):

    def get_user(self, request):
        ''' Attempt to get the user if authenticated through session otherwise
        resolve the provided API token if it exists.
        '''
        if hasattr(request, 'user') and request.user.is_authenticated():
            return request.user
        else:
            try:
                token = request.META['HTTP_AUTHORIZATION'].split('token')[1].lstrip(' ')
                user = Token.objects.get(key=token).user
                return user
            except Token.DoesNotExist:
                return None
            except KeyError:
                return None
        return None

    def get_pds(self, request, view_args):
        ''' Attempt to get the ProtocolDataSource associated with the request
        '''
        if 'pds_id' in view_args[1].keys():
            try:
                pds = ProtocolDataSource.objects.get(pk=int(view_args[1]['pds_id']))
                return pds
            except ProtocolDataSource.DoesNotExist:
                return None
        return None

    def process_request(self, request, *args, **kwargs):
        request.start_ts = datetime.datetime.now()

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        request.META['pds'] = self.get_pds(request, view_args)

    def process_response(self, request, response):
        error = request.META.get('error', None)
        if error:
            logger = log.error
        else:
            logger = log.info
        # Get action from request META. Actions are set in their respective views
        if response.status_code > 400 and response.status_code != 404:
            log.error('Unspecified server error')
        action = request.META.get('action', None)
        if action:
            pds = request.META.get('pds')
            subject_id = request.META.get('subject_id')
            user_error_msg = request.META.get('user_error_msg')
            user = self.get_user(request)
            user_name = user.username if user else None
            response_time = (datetime.datetime.now() - request.start_ts).microseconds / 1000
            if pds:
                logger(
                    '{action} by {user} on PDS {pds_id} in {response_time}ms'.format(
                        action=action,
                        user=user_name,
                        pds_id=pds.id,
                        response_time=response_time),
                    extra={
                        'action': action,
                        'user': user_name,
                        'pds': pds.id,
                        'datasource': pds.data_source.name,
                        'protocol_name': pds.protocol.name,
                        'protocol': pds.protocol.id,
                        'subject_id': subject_id,
                        'user_error_msg': user_error_msg,
                        'response_time': response_time})
            else:
                logger('{action}'.format(action=action), extra={
                    'action': action,
                    'user': user,
                    'response_time': response_time
                })
        return response
