from django.contrib import admin
from dentist_clinic.models import Appointment, PatientHistory, Procedure, Room, UserData
# Register your models here.

admin.site.register(Appointment)
admin.site.register(PatientHistory)
admin.site.register(Procedure)
admin.site.register(Room)
admin.site.register(UserData)
