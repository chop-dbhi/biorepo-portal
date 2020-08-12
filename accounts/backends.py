import ldap3 as ldap
import logging
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db import transaction
from registration.models import RegistrationProfile
from registration.backends.default import Backend

from accounts.models import UserProfile
from accounts.forms import ChopRegistrationForm

log = logging.getLogger(__name__)


class DefaultBackend(Backend):
    @transaction.atomic
    def register(self, request, form):
        cleaned_data = form.cleaned_data

        user = form.save(commit=False)
        # new user registration requires review, so we set the user to inactive
        # by default
        user.is_active = False
        user.save()

        # create user profile
        profile = UserProfile(user=user, reason=cleaned_data['reason'],
                              eula=cleaned_data['eula'],
                              institution=cleaned_data['institution'])
        profile.save()

        # create the registration profile
        registration_profile = RegistrationProfile.objects.create_profile(user)

        # provide the ``moderated`` to the user registration email to
        # determine whether the activation or verification link should
        # be sent in the email
        self._send_registration_email(request, registration_profile)
        return user

    def get_registration_form_class(self, request):
        return ChopRegistrationForm


class LdapBackend:
    '''
    Authenticate a user against an Active Directory server using LDAP.
    '''
    settings = {
        'SERVER_URI': 'ldap://localhost',
        'SEARCHDN': 'dc=localhost',
        'SCOPE': None,
        'SEARCH_FILTER': 'cn={0}',
        'UPDATE_FIELDS': True,
        'PREBINDDN': None,
        'PREBINDPW': None,
        'BINDDN': None,
        'BIND_ATTRIBUTE': None,
        'OPTIONS': None,
        'DEBUG': True,
    }

    def __init__(self):
        ldap_settings = getattr(settings, 'LDAP', {})
        self.settings.update(ldap_settings)

    # Functions provided to override to customize to your LDAP configuration.
    def _pre_bind(self, server, username):
        "Function that returns the dn to bind against LDAP with"
        conn = ldap.Connection(
            server,
            user=self.settings['PREBINDDN'],
            password=self.settings['PREBINDPW'])
        try:
            conn.bind()
        except ldap.LDAPSocketOpenError:
            log.error('Unable to connect to LDAP server')
            return
        _filter = self.settings['SEARCH_FILTER'].format(username)
        try:
            search = conn.search(
                self.settings['SEARCHDN'],
                _filter)
            if search:
                dn = conn.response[0]['dn']
                conn.unbind()
                return dn
        except ldap.LDAPInvalidFilterError:
            log.error('Error performing prebind LDAP search')
            return

    def get_ad_timestamp(self, ldap_response):
        ''' returns datetime password was last set '''
        timestamp = int(ldap_response[0]['attributes']['pwdLastSet'][0])
        epoch_start = datetime(year=1601, month=1, day=1)
        seconds_since_epoch = timestamp / 10**7
        return epoch_start + timedelta(seconds=seconds_since_epoch)

    def authenticate(self, request, username=None, password=None):
        # handle an email address being supplied
        idx = username.find('@')
        if idx > -1:
            email = username.lower()
            username = username[:idx].lower()
        else:
            email = '%s@email.chop.edu' % username.lower()

        # test up front if an account for this user exists before testing it
        # against the LDAP connection
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            log.error('Unable to find user with email {0}'.format(email))
            return None

        # initialize connection to the server
        server = ldap.Server('chop.edu', port=3268)
        bind_string = self._pre_bind(server, username)

        if not bind_string:
            log.error('Unable to initialize connection to LDAP server')
            return None

        conn = ldap.Connection(
            server,
            user=bind_string,
            password=password)
        # _filter = self.settings['SEARCH_FILTER'].format(username)
        conn.bind()
        # res = conn.search('dc=chop,dc=edu', _filter, attributes=['pwdLastSet'])
        #
        # if res:
        #     pwdLastSet = self.get_ad_timestamp(conn.response)
        #     pwdAge = (datetime.now() - pwdLastSet).days
        #     if pwdAge > self.settings['MAX_AGE']:
        #         log.error('User {0}: Password has expired'.format(username))
        #         user.profile.password_expired = True
        #         user.is_active = False
        #         return user

        if conn.bind():
            conn.unbind()
            user = User.objects.get(username=user)
            return user
        else:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
