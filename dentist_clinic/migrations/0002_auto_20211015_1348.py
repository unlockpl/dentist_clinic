# Generated by Django 3.2.7 on 2021-10-15 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dentist_clinic', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdata',
            name='patient_histories',
        ),
        migrations.AddField(
            model_name='userdata',
            name='patient_histories',
            field=models.ManyToManyField(to='dentist_clinic.PatientHistory'),
        ),
    ]
