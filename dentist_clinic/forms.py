from django import forms
from django.contrib.auth.models import User
from dentist_clinic.models import Appointment, UserData


class UserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
        )
        labels = {
            'username': 'Username',
            'password': 'Password',
            'email': 'E-mail address',
            'first_name': 'First name',
            'last_name': 'Last name',
        }


class UserDataModelForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = (
            'phone',
            'address'
        )
        labels = {
            'phone': 'Phone number',
            'address': 'Full address'
        }


