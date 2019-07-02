from unittest.mock import MagicMock, patch, call
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.test import Client

from registration.models import RegistrationProfile

from accounts.forms import ChopRegistrationForm
from accounts.models import UserProfile
from accounts.backends import LdapBackend


class AccountsModuleTests(TestCase):

    client = Client()
    test_user = {
        'first_name': 'John',
        'last_name': 'Sample',
        'email': 'admin@email.chop.edu',
        'password': 'Chop1234',
        'institution': 'The Children\'s Hospital of Philadelphia',
        'reason': 'Making the world a better place',
        'eula': True
    }
    existing_user = {
        'first_name': 'Jane',
        'last_name': 'Sample',
        'username': 'jane',
        'email': 'jane@email.chop.edu',
        'password': 'Chopchop1234',
    }
    test_user_object = None
    form_data = {
        'first_name': 'John',
        'last_name': 'Sample',
        'email': 'test@email.chop.edu',
        'password': 'Chop1234',
        'institution': 'The Children\'s Hospital of Philadelphia',
        'reason': 'Making the world a better place',
        'eula': True
    }
    valid_form = ChopRegistrationForm(form_data)

    def setUp(self):
        form = ChopRegistrationForm(self.test_user)
        form.save()
        # Manually create existing user with profile.
        existing_user = User(**self.existing_user)
        existing_user.set_password(self.existing_user['password'])
        existing_user.save()
        UserProfile(user=existing_user).save()
        test_user = User.objects.get(email=self.test_user['email'])
        UserProfile(user=test_user).save()

    def tearDown(self):
        User.objects.get(email=self.test_user['email']).delete()
        User.objects.get(email=self.existing_user['email']).delete()

    # Hangs in CI
    # def test_throttled_login(self):
    #     response = self.client.get('/login/')
    #     self.assertEqual(response.status_code, 200)

    def test_new_registration_form(self):
        form = self.valid_form
        self.assertTrue(form.is_valid())

    def test_registration_form_empty_reason(self):
        form = ChopRegistrationForm({
            'first_name': 'John',
            'last_name': 'Sample',
            'email': 'test@email.chop.edu',
            'password': 'Chop1234',
            'institution': 'The Children\'s Hospital of Philadelphia',
            'reason': '',
            'eula': True
        })
        self.assertFalse(form.is_valid())

    def test_registration_form_eula(self):
        form = ChopRegistrationForm({
            'first_name': 'John',
            'last_name': 'Sample',
            'email': 'test@email.chop.edu',
            'password': 'Chop1234',
            'institution': 'The Children\'s Hospital of Philadelphia',
            'reason': '',
            'eula': False
        })
        self.assertFalse(form.is_valid())

    def test_empty_registration_form(self):
        form = ChopRegistrationForm({})
        self.assertFalse(form.is_valid())

    def test_new_reg_creates_user(self):
        form = self.valid_form
        form.save()
        user = User.objects.get(email='test@email.chop.edu')
        self.assertTrue(isinstance(user, User))

    def test_new_reg_creates_user_profile(self):
        response = self.client.post('/accounts/register/', self.form_data)
        # Check that form submit is ok.
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(email='test@email.chop.edu')
        up = UserProfile.objects.get(user=user)
        self.assertEqual(str(up), 'John Sample\'s Profile')
        self.assertTrue(up.user, user)
        self.assertTrue(isinstance(up, UserProfile))

    def test_new_reg_creates_registration_profile(self):
        response = self.client.post('/accounts/register/', self.form_data)
        # Check that form submit is ok.
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(email='test@email.chop.edu')
        rp = RegistrationProfile.objects.get(user=user)
        self.assertTrue(rp.user, user)
        # Check that the newly registered user is neither activated or moderated
        self.assertFalse(rp.activated)
        self.assertFalse(rp.moderated)
        self.assertTrue(isinstance(rp, RegistrationProfile))

    @override_settings(AUTHENTICATION_BACKENDS=['accounts.backends.LdapBackend'])
    def test_ldap_login_email(self):
        backend = LdapBackend()
        with patch('ldap3.Connection') as MockLDAP:
            backend.get_ad_timestamp = MagicMock(return_value=datetime.now())
            ldap = MockLDAP.return_value
            ldap.search.return_value = [{'dn': 'test'}]
            ldap.response = [{'dn': 'test'}]
            user = backend.authenticate('admin@email.chop.edu', 'Chop1234')
            # Check search calls
            search_call_list = ldap.search.call_args_list
            self.assertTrue(call('searchdn', '(sAMAccountName=admin)') in search_call_list)
            # Check binds
            self.assertTrue(ldap.bind.called)
            self.assertTrue(ldap.unbind.called)
            # Check is User
            self.assertTrue(isinstance(user, User))

    @override_settings(AUTHENTICATION_BACKENDS=['accounts.backends.LdapBackend'])
    def test_ldap_login_expired(self):
        backend = LdapBackend()
        with patch('ldap3.Connection') as MockLDAP:
            backend.get_ad_timestamp = MagicMock(return_value=datetime.now() - timedelta(days=181))
            ldap = MockLDAP.return_value
            ldap.search.return_value = [{'dn': 'test'}]
            ldap.response = [{'dn': 'test'}]
            user = backend.authenticate('admin@email.chop.edu', 'Chop1234')
            # Check search calls
            search_call_list = ldap.search.call_args_list
            self.assertTrue(call('searchdn', '(sAMAccountName=admin)') in search_call_list)
            # Check binds
            self.assertTrue(ldap.bind.called)
            self.assertTrue(ldap.unbind.called)
            # Check is User
            self.assertTrue(isinstance(user, User))
            # Check User is expired
            self.assertTrue(user.profile.password_expired)

    @override_settings(AUTHENTICATION_BACKENDS=['accounts.backends.LdapBackend'])
    def test_ldap_login_username(self):
        backend = LdapBackend()
        with patch('ldap3.Connection') as MockLDAP:
            backend.get_ad_timestamp = MagicMock(return_value=datetime.now())
            ldap = MockLDAP.return_value
            ldap.search.return_value = [{'dn': 'test'}]
            ldap.response = [{'dn': 'test'}]
            user = backend.authenticate('admin', 'Chop1234')
            # Check search calls
            search_call_list = ldap.search.call_args_list
            self.assertTrue(call('searchdn', '(sAMAccountName=admin)') in search_call_list)
            self.assertTrue(call('dc=chop,dc=edu', '(sAMAccountName=admin)', attributes=['pwdLastSet']) in search_call_list)
            # Check binds
            self.assertTrue(ldap.bind.called)
            self.assertTrue(ldap.unbind.called)
            # Check is User
            self.assertTrue(isinstance(user, User))

    @override_settings(AUTHENTICATION_BACKENDS=['accounts.backends.LdapBackend'])
    def test_ldap_login_user_does_not_exist(self):
        backend = LdapBackend()
        with patch('ldap3.Connection') as MockLDAP:
            backend.get_ad_timestamp = MagicMock(return_value=datetime.now())
            ldap = MockLDAP.return_value
            ldap.search.return_value = [{'dn': 'test'}]
            ldap.response = [{'dn': 'test'}]
            user = backend.authenticate('none@email.chop.edu', 'xxxxx')
            self.assertEqual(user, None)

    def test_ldap_ad_timestamp_conversion(self):
        backend = LdapBackend()
        mock_response = [{'attributes': {'pwdLastSet': ['131157000000000000']}}]
        d = backend.get_ad_timestamp(mock_response)
        self.assertEqual(datetime(2016, 8, 15, 2), d)

    def test_login_allowed(self):
        s = self.client.session
        s['login_allowed'] = True
        s.save()
        response = self.client.get('/login/', HTTP_USER_AGENT='Mozilla/5.0',)
        # Should redirect to login.
        self.assertEqual(response.status_code, 200)

    def test_login_not_allowed(self):
        s = self.client.session
        s['login_allowed'] = False
        s.save()
        response = self.client.get('/login/', HTTP_USER_AGENT='Mozilla/5.0',)
        # Should redirect to login.
        self.assertTrue('You have reached the maximum number of login attempts.' in str(response.content))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_login_redirect(self):
        user = User.objects.get(email='jane@email.chop.edu')
        # Accept the EULA for this user
        user.profile.eula = True
        user.profile.save()
        self.client.force_login(user)
        response = self.client.get('/login/', HTTP_USER_AGENT='Mozilla/5.0',)
        # Should redirect to root.
        self.assertEqual(response.status_code, 302)

    def test_block_disabled_user_login(self):
        s = self.client.session
        s['login_allowed'] = False
        s.save()
        response = self.client.post('/login/', {'username': 'admin@email.chop.edu', 'password': 'Chopchop1234'}, HTTP_USER_AGENT='Mozilla/5.0',)
        # Should redirect to login.
        self.assertEqual(response.status_code, 302)

    def test_throttled_user_login(self):
        s = self.client.session
        s['login_allowed'] = True
        s.save()
        with self.settings(CACHES={
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'test-cache',
            }
        }):
            form_data = {'email': 'jane@email.chop.edu', 'username': 'jane', 'password': 'Chopchop1234'}
            response = self.client.post('/login/', form_data, HTTP_USER_AGENT='Mozilla/5.0',)
            # Should redirect to root.
            self.assertEqual(response.status_code, 302)

    def test_throttled_user_login_bad_payload(self):
        s = self.client.session
        s['login_allowed'] = True
        s.save()
        with self.settings(CACHES={
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'test-cache',
            }
        }):
            form_data = {'email': 'jane@email.chop.edu', 'username': 'jane'}
            response = self.client.post('/login/', form_data, HTTP_USER_AGENT='Mozilla/5.0',)
            # Should not redirect...
            self.assertEqual(response.status_code, 200)

    def test_max_attempts(self):
        from django.core.cache import cache
        s = self.client.session
        s['login_allowed'] = True
        s.save()
        with self.settings(CACHES={
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'test-cache2',
            }
        }):
            form_data = {'email': 'jane@email.chop.edu', 'username': 'jane', 'password': 'wrongpass'}
            user = User.objects.get(email='jane@email.chop.edu')
            self.assertTrue(user.is_active)
            # Make 11 bogus login attempts (10 is max)
            cache.set('jane@email.chop.edu_127.0.0.1_login_attempts', 10)
            self.client.post('/login/', form_data, HTTP_USER_AGENT='Mozilla/5.0',)
            user = User.objects.get(email='jane@email.chop.edu')
            self.assertFalse(user.is_active)

    def test_max_attempts_user_already_inactive(self):
        s = self.client.session
        s['login_allowed'] = True
        s.save()
        with self.settings(CACHES={
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'test-cache2',
            }
        }):
            form_data = {'email': 'jane@email.chop.edu', 'username': 'jane', 'password': 'wrongpass'}
            user = User.objects.get(email='jane@email.chop.edu')
            user.is_active = False
            user.save()
            self.assertFalse(user.is_active)
            # Should fail immediately
            response = self.client.post('/login/', form_data, HTTP_USER_AGENT='Mozilla/5.0',)
            self.assertTrue('You have reached the maximum number of login attempts.' in str(response.content))
            user = User.objects.get(email='jane@email.chop.edu')
            self.assertFalse(user.is_active)

    def test_throttled_login_user_not_found(self):
        s = self.client.session
        s['login_allowed'] = True
        s.save()
        with self.settings(CACHES={
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'test-cache2',
            }
        }):
            form_data = {'email': 'none@email.chop.edu', 'username': 'none', 'password': 'wrongpass'}
            # Should fail immediately
            response = self.client.post('/login/', form_data, HTTP_USER_AGENT='Mozilla/5.0',)
            self.assertTrue('Please enter a correct email and password.' in str(response.content))

    def test_clear_throttled_login(self):
        from django.core.cache import cache
        s = self.client.session
        s['login_allowed'] = True
        s.save()
        with self.settings(CACHES={
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'test-cache2',
            }
        }):
            form_data = {'email': 'jane@email.chop.edu', 'username': 'jane', 'password': 'Chopchop1234'}
            user = User.objects.get(email='jane@email.chop.edu')
            self.assertTrue(user.is_active)
            # Make 3 bogus login attempts (5 is max)
            cache.set('jane@email.chop.edu_127.0.0.1_login_attempts', 3)
            self.client.post('/login/', form_data, HTTP_USER_AGENT='Mozilla/5.0',)
            user = User.objects.get(email='jane@email.chop.edu')
            self.assertTrue(user.is_active)
            # when login successful user should be deleted from cache.
            self.assertFalse(cache.get('jane@email.chop.edu_127.0.0.1_login_attempts'))

    def test_eula(self):
        response = self.client.get('/eula/')
        self.assertTrue('End User License Agreement', str(response.content))
        self.assertEqual(response.status_code, 200)

    def test_agree_to_eula(self):
        user = User.objects.get(email='jane@email.chop.edu')
        self.client.force_login(user)
        self.assertFalse(user.profile.eula)
        response = self.client.post('/eula/', {'decision': 'i agree'})
        # Get user again to update state
        user = User.objects.get(email='jane@email.chop.edu')
        self.assertTrue(user.profile.eula)
        # Should redirect if accepted
        self.assertEqual(response.status_code, 302)

    def test_reject_to_eula(self):
        user = User.objects.get(email='jane@email.chop.edu')
        self.client.force_login(user)
        self.assertFalse(user.profile.eula)
        response = self.client.post('/eula/', {'decision': ''})
        # Should redirect if accepted and profile should reflect unaccepted eula
        self.assertFalse(user.profile.eula)
        self.assertEqual(response.status_code, 302)

    def test_eula_middleware(self):
        user = User.objects.get(email='jane@email.chop.edu')
        self.client.force_login(user)
        self.assertFalse(user.profile.eula)
        response = self.client.get('/')
        self.assertTrue('END-USER LICENSE AGREEMENT' in str(response.content))

    def test_eula_middleware_static(self):
        user = User.objects.get(email='jane@email.chop.edu')
        self.client.force_login(user)
        self.assertFalse(user.profile.eula)
        response = self.client.get('/static/css/style.css')
        self.assertFalse('END-USER LICENSE AGREEMENT' in str(response.content))
