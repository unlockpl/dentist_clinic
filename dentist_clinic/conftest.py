import pytest
from dentist_clinic.models import Room, Procedure, Appointment, PatientHistory, UserData
from django.contrib.auth.models import User, Group
from django.utils import timezone
import pytz

@pytest.fixture
def user():
    return User.objects.create(
        username='test_user',
        password='testpassword123',
        first_name='test_fn',
        last_name='test_ln',
        email='testemail@email.com',
    )


@pytest.fixture
def user_data(user):
    return UserData.objects.create(
        phone='12345',
        address='test_address',
        user=user,
    )


@pytest.fixture
def room():
    return Room.objects.create(name='x')


@pytest.fixture
def rooms():
    test_list = []
    for i in range(10):
        test_list.append(Room.objects.create(name=i))
    return test_list


@pytest.fixture
def procedure(doctors):
    obj = Procedure.objects.create(name='x', price=1)
    obj.doctors.set(doctors)
    return obj


@pytest.fixture
def procedures(doctors):
    test_list = []
    for i in range(10):
        obj = Procedure.objects.create(name=i, price=i)
        obj.doctors.set(doctors)
        test_list.append(obj)
    return test_list


@pytest.fixture
def appointment(room, patient, doctor, procedure):
    return Appointment.objects.create(
        date=timezone.now(),
        room=room,
        patient=patient,
        doctor=doctor,
        procedure=procedure,
    )


@pytest.fixture
def appointments(rooms, patients, doctors, procedures):
    test_list = []
    for i in range(10):
        test_list.append(Appointment.objects.create(
            date=timezone.now(),
            room=rooms[i],
            patient=patients[i],
            doctor=doctors[i],
            procedure=procedures[i],
        ))
    return test_list


@pytest.fixture
def patient_history(patient, doctor):
    return PatientHistory.objects.create(
        entry='x',
        creation_time=timezone.now(),
        patient=patient,
        doctor=doctor,
    )


@pytest.fixture
def patient_histories(patients, doctors):
    test_list = []
    for i in range(10):
        test_list.append(PatientHistory.objects.create(
            entry=i,
            creation_time=timezone.now(),
            patient=patients[i],
            doctor=doctors[i],
        ))
    return test_list


@pytest.fixture
def doctor(doctor_group):
    user = User.objects.create(username='x')
    user.groups.add(doctor_group)
    return user


@pytest.fixture
def doctor_data(doctor):
    return UserData.objects.create(
        phone='12345',
        address='test_address',
        user=doctor,
    )


@pytest.fixture
def doctors(doctor_group):
    test_list = []
    for i in range(10):
        user = User.objects.create(username=i)
        user.groups.add(doctor_group)
        test_list.append(user)
    return test_list


@pytest.fixture
def patient(patient_group):
    user = User.objects.create(username='y')
    user.groups.add(patient_group)
    return user


@pytest.fixture
def patient_data(patient):
    return UserData.objects.create(
        phone='12345',
        address='test_address',
        user=patient,
    )



@pytest.fixture
def patients(patient_group):
    test_list = []
    for i in range(10, 20):
        user = User.objects.create(username=i)
        user.groups.add(patient_group)
        test_list.append(user)
    return test_list


@pytest.fixture
def doctor_group():
    return Group.objects.create(name='Doctor')


@pytest.fixture
def patient_group():
    return Group.objects.create(name='Patient')
