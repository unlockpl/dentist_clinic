import django.contrib.auth.models
from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Procedure(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    doctors = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    date = models.DateTimeField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_appointment', null=True)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointment', null=True)
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE)

    def __str__(self):
        return f"Appointment on {self.date} to {self.doctor.first_name} {self.doctor.last_name}"


class PatientHistory(models.Model):
    entry = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_history', null=True)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_history', null=True)

    def __str__(self):
        return f"Patient history entry from {self.creation_time} written by {self.doctor.first_name} {self.doctor.last_name}"


class UserData(models.Model):
    phone = models.CharField(max_length=32)
    address = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
