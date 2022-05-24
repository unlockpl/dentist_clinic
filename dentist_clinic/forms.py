import re

from django import forms
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError

from dentist_clinic.models import Appointment, PatientHistory, Room, UserData


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

    def clean(self):
        data = super().clean()
        pattern = re.compile("^\d+$")
        if not pattern.match(data.get('phone')):
            raise ValidationError("Only numeric values accepted in the phone field")
        return data


class AppointmentModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = User.objects.filter(groups__in=Group.objects.filter(name="Doctor"))

    class Meta:
        model = Appointment
        fields = (
            'date',
            'doctor',
            'procedure'
        )
        labels = {
            'date': 'Date and time',
            'doctor': 'Doctor',
            'procedure': 'Procedure'
        }

    def clean(self):

        data = super().clean()
        date = data.get('date')
        doctor = data.get('doctor')
        procedure = data.get('procedure')

        procedure_check = False
        for item in procedure.doctors.all():
            if item == doctor:
                procedure_check = True
        if not procedure_check:
            raise ValidationError("This doctor cannot perform this procedure")

        if Appointment.objects.filter(doctor=doctor).filter(date=date):
            raise ValidationError("This doctor is not available at this time")

        room_check = False
        for room in Room.objects.all():
            if not Appointment.objects.filter(room=room).filter(date=date):
                room_check = True
                break
        if not room_check:
            raise ValidationError("No rooms available at this time")


class PatientHistoryModelForm(forms.ModelForm):
    class Meta:
        model = PatientHistory
        fields = (
            'entry',
        )
        labels = {
            'entry': 'Entry',
        }
