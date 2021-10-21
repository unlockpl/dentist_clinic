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
@pytest.mark.django_db
def test_details_profile_doctor_logged_in(doctor, doctor_data):
    client = Client()
    client.force_login(doctor)
    response = client.get(reverse('profile-user'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_details_profile_patient_logged_in(patient, patient_data):
    client = Client()
    client.force_login(patient)
    response = client.get(reverse('profile-user'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_details_profile_not_logged_in():
    client = Client()
    response = client.get(reverse('profile-user'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_update_profile_doctor_logged_in(doctor, doctor_data):
    client = Client()
    client.force_login(doctor)
    response = client.get(reverse('update-user'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_profile_patient_logged_in(patient, patient_data):
    client = Client()
    client.force_login(patient)
    response = client.get(reverse('update-user'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_profile_not_logged_in():
    client = Client()
    response = client.get(reverse('update-user'))
    assert response.status_code == 302


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
    response = client.get(reverse('appointment-list-by-patient', kwargs={'pk': patient.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_by_patient_own_appointment_patient_logged_in(patient, appointments):
    client = Client()
    client.force_login(patient)
    response = client.get(reverse('appointment-list-by-patient', kwargs={'pk': patient.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_by_patient_not_own_appointment_patient_logged_in(patients, appointments):
    client = Client()
    client.force_login(patients[0])
    response = client.get(reverse('appointment-list-by-patient', kwargs={'pk': patients[1].pk}))
    assert response.status_code == 403


@pytest.mark.django_db
def test_list_by_patient_appointment_not_logged_in(patient):
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
def test_list_by_doctor_appointment_not_logged_in(patient):
    client = Client()
    response = client.get(reverse('appointment-list-by-doctor', kwargs={'pk': patient.pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_list_by_room_appointment_doctor_logged_in(doctor, room, appointments):
    client = Client()
    client.force_login(doctor)
    response = client.get(reverse('appointment-list-by-room', kwargs={'pk': room.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_by_room_appointment_patient_logged_in(patient, room, appointments):
    client = Client()
    client.force_login(patient)
    response = client.get(reverse('appointment-list-by-room', kwargs={'pk': room.pk}))
    assert response.status_code == 403


@pytest.mark.django_db
def test_list_by_room_appointment_not_logged_in(room):
    client = Client()
    response = client.get(reverse('appointment-list-by-room', kwargs={'pk': room.pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_form_patient_history_doctor_logged_in(doctor, patient):
    client = Client()
    client.force_login(doctor)
    response = client.get(reverse('patient-history-form', kwargs={'pk': patient.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_form_patient_history_patient_logged_in(patient):
    client = Client()
    client.force_login(patient)
    response = client.get(reverse('patient-history-form', kwargs={'pk': patient.pk}))
    assert response.status_code == 403


@pytest.mark.django_db
def test_form_patient_history_not_logged_in(patient):
    client = Client()
    response = client.get(reverse('patient-history-form', kwargs={'pk': patient.pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_list_patient_history_doctor_logged_in(doctor, patient):
    client = Client()
    client.force_login(doctor)
    response = client.get(reverse('patient-history-list', kwargs={'pk': patient.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_own_patient_history_patient_logged_in(patient):
    client = Client()
    client.force_login(patient)
    response = client.get(reverse('patient-history-list', kwargs={'pk': patient.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_not_own_patient_history_patient_logged_in(patient, patients):
    client = Client()
    client.force_login(patients[0])
    response = client.get(reverse('patient-history-list', kwargs={'pk': patient.pk}))
    assert response.status_code == 403


@pytest.mark.django_db
def test_list_patient_history_not_logged_in(patient):
    client = Client()
    response = client.get(reverse('patient-history-form', kwargs={'pk': patient.pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_list_doctor_history_doctor_logged_in(doctor):
    client = Client()
    client.force_login(doctor)
    response = client.get(reverse('doctor-history-list', kwargs={'pk': doctor.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_doctor_history_patient_logged_in(patient, doctor):
    client = Client()
    client.force_login(patient)
    response = client.get(reverse('doctor-history-list', kwargs={'pk': doctor.pk}))
    assert response.status_code == 403


@pytest.mark.django_db
def test_list_doctor_history_not_logged_in(doctor):
    client = Client()
    response = client.get(reverse('doctor-history-list', kwargs={'pk': doctor.pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_list_doctor_doctor_logged_in(doctor):
    client = Client()
    client.force_login(doctor)
    response = client.get(reverse('doctor-list'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_doctor_patient_logged_in(patient):
    client = Client()
    client.force_login(patient)
    response = client.get(reverse('doctor-list'))
    assert response.status_code == 403


@pytest.mark.django_db
def test_list_doctor_not_logged_in():
    client = Client()
    response = client.get(reverse('doctor-list'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_list_patient_doctor_logged_in(doctor):
    client = Client()
    client.force_login(doctor)
    response = client.get(reverse('patient-list'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_patient_patient_logged_in(patient):
    client = Client()
    client.force_login(patient)
    response = client.get(reverse('patient-list'))
    assert response.status_code == 403


@pytest.mark.django_db
def test_list_patient_not_logged_in():
    client = Client()
    response = client.get(reverse('patient-list'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_list_room_doctor_logged_in(doctor):
    client = Client()
    client.force_login(doctor)
    response = client.get(reverse('room-list'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_room_patient_logged_in(patient):
    client = Client()
    client.force_login(patient)
    response = client.get(reverse('room-list'))
    assert response.status_code == 403


@pytest.mark.django_db
def test_list_room_not_logged_in():
    client = Client()
    response = client.get(reverse('room-list'))
    assert response.status_code == 302
    

@pytest.mark.django_db
def test_update_appointment_doctor_logged_in(doctor, appointment):
    client = Client()
    client.force_login(doctor)
    response = client.get(reverse('appointment-update', kwargs={'pk': appointment.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_own_appointment_patient_logged_in(patient, appointment):
    client = Client()
    client.force_login(patient)
    response = client.get(reverse('appointment-update', kwargs={'pk': appointment.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_not_own_appointment_patient_logged_in(patient, patients, appointment):
    client = Client()
    client.force_login(patients[0])
    response = client.get(reverse('appointment-update', kwargs={'pk': appointment.pk}))
    assert response.status_code == 403


@pytest.mark.django_db
def test_update_appointment_not_logged_in(appointment):
    client = Client()
    response = client.get(reverse('appointment-update', kwargs={'pk': appointment.pk}))
    assert response.status_code == 302
    
    
@pytest.mark.django_db
def test_update_appointment_doctor_logged_in(doctor, appointment):
    client = Client()
    client.force_login(doctor)
    response = client.get(reverse('appointment-update', kwargs={'pk': appointment.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_own_appointment_patient_logged_in(patient, appointment):
    client = Client()
    client.force_login(patient)
    response = client.get(reverse('appointment-update', kwargs={'pk': appointment.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_not_own_appointment_patient_logged_in(patient, patients, appointment):
    client = Client()
    client.force_login(patients[0])
    response = client.get(reverse('appointment-update', kwargs={'pk': appointment.pk}))
    assert response.status_code == 403


@pytest.mark.django_db
def test_update_appointment_not_logged_in(patient, appointment):
    client = Client()
    response = client.get(reverse('appointment-update', kwargs={'pk': appointment.pk}))
    assert response.status_code == 302
    

@pytest.mark.django_db
def test_delete_appointment_doctor_logged_in(doctor, appointment):
    client = Client()
    client.force_login(doctor)
    response = client.get(reverse('appointment-delete', kwargs={'pk': appointment.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_own_appointment_patient_logged_in(patient, appointment):
    client = Client()
    client.force_login(patient)
    response = client.get(reverse('appointment-delete', kwargs={'pk': appointment.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_not_own_appointment_patient_logged_in(patients, appointment):
    client = Client()
    client.force_login(patients[0])
    response = client.get(reverse('appointment-delete', kwargs={'pk': appointment.pk}))
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_appointment_not_logged_in(appointment):
    client = Client()
    response = client.get(reverse('appointment-delete', kwargs={'pk': appointment.pk}))
    assert response.status_code == 302
    
    
@pytest.mark.django_db
def test_details_patient_history_doctor_logged_in(doctor, patient_history):
    client = Client()
    client.force_login(doctor)
    response = client.get(reverse('patient-history-details', kwargs={'pk': patient_history.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_details_own_patient_history_patient_logged_in(patient, patient_history):
    client = Client()
    client.force_login(patient)
    response = client.get(reverse('patient-history-details', kwargs={'pk': patient_history.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_details_not_own_patient_history_patient_logged_in(patients, patient_history):
    client = Client()
    client.force_login(patients[0])
    response = client.get(reverse('patient-history-details', kwargs={'pk': patient_history.pk}))
    assert response.status_code == 403


@pytest.mark.django_db
def test_details_patient_history_not_logged_in(patient_history):
    client = Client()
    response = client.get(reverse('patient-history-details', kwargs={'pk': patient_history.pk}))
    assert response.status_code == 302
    

@pytest.mark.django_db
def test_update_patient_history_doctor_logged_in(doctor, patient_history):
    client = Client()
    client.force_login(doctor)
    response = client.get(reverse('patient-history-update', kwargs={'pk': patient_history.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_patient_history_patient_logged_in(patient, patient_history):
    client = Client()
    client.force_login(patient)
    response = client.get(reverse('patient-history-update', kwargs={'pk': patient_history.pk}))
    assert response.status_code == 403


@pytest.mark.django_db
def test_update_patient_history_not_logged_in(patient_history):
    client = Client()
    response = client.get(reverse('patient-history-update', kwargs={'pk': patient_history.pk}))
    assert response.status_code == 302
    
    
@pytest.mark.django_db
def test_delete_patient_history_doctor_logged_in(doctor, patient_history):
    client = Client()
    client.force_login(doctor)
    response = client.get(reverse('patient-history-delete', kwargs={'pk': patient_history.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_patient_history_patient_logged_in(patient, patient_history):
    client = Client()
    client.force_login(patient)
    response = client.get(reverse('patient-history-delete', kwargs={'pk': patient_history.pk}))
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_patient_history_not_logged_in(patient_history):
    client = Client()
    response = client.get(reverse('patient-history-delete', kwargs={'pk': patient_history.pk}))
    assert response.status_code == 302