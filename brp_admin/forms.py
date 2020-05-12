from django.forms import ModelForm, Form
from django import forms
from api.models.protocols import ProtocolUserCredentials, ProtocolUser, Protocol, ProtocolDataSource, DataSource
from django.contrib.auth.models import User
from django.db.models import Q

class ProtocolUserForm(ModelForm):
    class Meta:
        model = ProtocolUser
        fields = ('protocol', 'user', 'role')

class ProtocolUserCredentialsForm(ModelForm):
    class Meta:
        model = ProtocolUserCredentials
        fields = ('data_source', 'data_source_username', 'data_source_password')

class NautilusCredentialsForm(Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), empty_label="Select a User")
    data_source = forms.ModelChoiceField(queryset=DataSource.objects.filter(name__contains='Nautilus'), empty_label="Select a Data Source")
    data_source_username = forms.CharField(max_length=100)
    data_source_password = forms.CharField(max_length=100)

class ProtocolForm(forms.Form):
    protocol = forms.ModelChoiceField(queryset=Protocol.objects.all(), empty_label="All")

class UserForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), empty_label="Select a User")
