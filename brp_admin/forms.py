from django.forms import ModelForm
from django import forms

from api.models.protocols import ProtocolUserCredentials, ProtocolUser, Protocol, ProtocolDataSource
from django.contrib.auth.models import User


class ProtocolUserForm(ModelForm):
    class Meta:
        model = ProtocolUser
        fields = ('protocol', 'user', 'role')


class ProtocolUserCredentialsForm(ModelForm):
    class Meta:
        model = ProtocolUserCredentials
        fields = ('data_source', 'data_source_username', 'data_source_password')

class ProtocolForm(forms.Form):
    protocol = forms.ModelChoiceField(queryset=Protocol.objects.all(), empty_label="All")


class UserForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), empty_label="Select a User")

class NautilusCredentialForm(forms.Form):
    username = forms.ModelChoiceField(queryset=User.objects.all(), empty_label="Select a User")
    password = forms.CharField(max_length=50, label='New Nautilus Password')
