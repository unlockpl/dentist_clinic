from django.test import TestCase, Client
import pytest
from django.urls import reverse


# Create your tests here.
from dentist_clinic.conftest import *


@pytest.mark.django_db
def test_login():
    client = Client()
    response = client.get(reverse('login-user'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_register():
    client = Client()
    response = client.get(reverse('register-user'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_about_contact(doctors):
    client = Client()
    response = client.get(reverse('about-contact'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_services():
    client = Client()
    response = client.get(reverse('procedure-list'))
    assert response.status_code == 200


# GROUP TESTS
# @pytest.mark.django_db
# def test_details_profile_doctor_logged_in(doctor):
#     client = Client()
#     client.force_login(doctor)
#     response = client.get(reverse('profile-user', kwargs={'pk': doctor.pk}))
#     assert response.status_code == 200
#
#
# @pytest.mark.django_db
# def test_details_own_profile_patient_logged_in(patient):
#     client = Client()
#     client.force_login(patient)
#     response = client.get(reverse('profile-user', kwargs={'pk': patient.pk}))
#     assert response.status_code == 200
#
#
# @pytest.mark.django_db
# def test_details_not_own_profile_patient_logged_in(patients):
#     client = Client()
#     client.force_login(patients[0])
#     response = client.get(reverse('profile-user', kwargs={'pk': patients[1].pk}))
#     assert response.status_code == 403
#
#
# @pytest.mark.django_db
# def test_details_profile_not_logged_in(patient):
#     client = Client()
#     response = client.get(reverse('profile-user', kwargs={'pk': patient.pk}))
#     assert response.status_code == 302
#
#
# @pytest.mark.django_db
# def test_update_profile_doctor_logged_in(doctor):
#     client = Client()
#     client.force_login(doctor)
#     response = client.get(reverse('update-user', kwargs={'pk': doctor.pk}))
#     assert response.status_code == 200
#
#
# @pytest.mark.django_db
# def test_update_own_profile_patient_logged_in(patient):
#     client = Client()
#     client.force_login(patient)
#     response = client.get(reverse('update-user', kwargs={'pk': patient.pk}))
#     assert response.status_code == 200
#
#
# @pytest.mark.django_db
# def test_update_not_own_profile_patient_logged_in(patients):
#     client = Client()
#     client.force_login(patients[0])
#     response = client.get(reverse('update-user', kwargs={'pk': patients[1].pk}))
#     assert response.status_code == 403
#
#
# @pytest.mark.django_db
# def test_update_profile_not_logged_in(patient):
#     client = Client()
#     response = client.get(reverse('update-user', kwargs={'pk': patient.pk}))
#     assert response.status_code == 302
#
#
@pytest.mark.django_db
def test_form_appointment_doctor_logged_in(doctor, patient):
    client = Client()
    client.force_login(doctor)
    response = client.get(reverse('appointment-form', kwargs={'pk': patient.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_form_own_appointment_patient_logged_in(patient):
    client = Client()
    client.force_login(patient)
    response = client.get(reverse('appointment-form', kwargs={'pk': patient.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_form_not_own_appointment_patient_logged_in(patients):
    client = Client()
    client.force_login(patients[0])
    response = client.get(reverse('appointment-form', kwargs={'pk': patients[1].pk}))
    assert response.status_code == 403


@pytest.mark.django_db
def test_form_appointment_not_logged_in(patient):
    client = Client()
    response = client.get(reverse('appointment-form', kwargs={'pk': patient.pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_list_by_patient_appointment_doctor_logged_in(doctor, patient, appointments):
    client = Client()
    client.force_login(doctor)
    response = client.get(reverse('appointment-list', kwargs={'pk': patient.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_by_patient_own_appointment_patient_logged_in(patient, appointments):
    client = Client()
    client.force_login(patient)
    response = client.get(reverse('appointment-list-by-patient', kwargs={'pk': patient.pk}))
    assert response.status_code == 403


@pytest.mark.django_db
def test_list_by_patient_not_own_appointment_patient_logged_in(patients, appointments):
    client = Client()
    client.force_login(patients[0])
    response = client.get(reverse('appointment-list-by-patient', kwargs={'pk': patients[1].pk}))
    assert response.status_code == 403


@pytest.mark.django_db
def test_list_by_patient_appointment_not_logged_in(patient, appointments):
    client = Client()
    response = client.get(reverse('appointment-list-by-patient', kwargs={'pk': patient.pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_list_by_doctor_appointment_doctor_logged_in(doctor, patient, appointments):
    client = Client()
    client.force_login(doctor)
    response = client.get(reverse('appointment-list-by-doctor', kwargs={'pk': patient.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_by_doctor_appointment_patient_logged_in(patient, appointments):
    client = Client()
    client.force_login(patient)
    response = client.get(reverse('appointment-list-by-doctor', kwargs={'pk': patient.pk}))
    assert response.status_code == 403


@pytest.mark.django_db
def test_list_by_doctor_appointment_not_logged_in(patient, appointments):
    client = Client()
    response = client.get(reverse('appointment-list-by-doctor', kwargs={'pk': patient.pk}))
    assert response.status_code == 302
