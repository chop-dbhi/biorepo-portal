from django.forms import ModelForm, Form
from django import forms
from api.models.protocols import ProtocolUserCredentials, ProtocolUser, Protocol, ProtocolDataSource, DataSource
from django.contrib.auth.models import User


class ProtocolUserForm(ModelForm):
    class Meta:
        model = ProtocolUser
        fields = ('protocol', 'user', 'role')

class ProtocolUserCredentialsForm(Form):
    protocol = forms.ModelChoiceField(queryset=Protocol.objects.all(), empty_label="Select a Protocol")
    user = forms.ModelChoiceField(queryset=User.objects.all(), empty_label="Select a User")
    protocol_user = forms.ModelChoiceField(queryset=ProtocolUser.objects.all(), empty_label="Select a Protocol User")
    data_source = forms.ModelChoiceField(queryset=ProtocolDataSource.objects.all(), empty_label="Select a Data Source")
    data_source_username = forms.CharField(max_length=100)
    data_source_password = forms.CharField(max_length=100)

class ProtocolForm(forms.Form):
    protocol = forms.ModelChoiceField(queryset=Protocol.objects.all(), empty_label="All")

class UserForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), empty_label="Select a User")
