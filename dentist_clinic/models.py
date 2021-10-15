import django.contrib.auth.models
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=255)


class Procedure(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    doctors = models.ManyToManyField(User)


class Appointment(models.Model):
    date = models.DateTimeField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE)


class PatientHistory(models.Model):
    description = models.TextField()


class UserData(models.Model):
    phone = models.CharField(max_length=32)
    address = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    appointments = models.ForeignKey(Appointment, on_delete=models.CASCADE, blank=True)
    patient_histories = models.ManyToManyField(PatientHistory, blank=True)
