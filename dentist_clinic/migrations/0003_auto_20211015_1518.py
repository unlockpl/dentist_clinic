# Generated by Django 3.2.7 on 2021-10-15 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dentist_clinic', '0002_auto_20211015_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='appointments',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dentist_clinic.appointment'),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='patient_histories',
            field=models.ManyToManyField(null=True, to='dentist_clinic.PatientHistory'),
        ),
    ]
