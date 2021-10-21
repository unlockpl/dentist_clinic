import pytest
from dentist_clinic.models import Room, Procedure, Appointment, PatientHistory, UserData
from django.contrib.auth.models import User, Group
from datetime import datetime

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
def user_data():
    return UserData.objects.create(
        phone='12345',
        address='test_address',

    )


@pytest.fixture
def room():
    return Room.objects.create(name=i)


@pytest.fixture
def rooms():
    test_list = []
    for i in range(10):
        test_list.append(Room.objects.create(name=i))
    return test_list


@pytest.fixture
def procedure(doctors):
    x = 'x'
    return Procedure.objects.create(name=x, price=x, doctors=doctors)


@pytest.fixture
def procedures(doctors):
    test_list = []
    for i in range(10):
        test_list.append(Procedure.objects.create(name=i, price=i, doctors=doctors))
    return test_list


@pytest.fixture
def appointment(room, patient, doctor, procedure):
    return Appointment.objects.create(
        date=datetime.now(),
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
            date=datetime.now(),
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
        creation_time=datetime.now(),
        patient=patient,
        doctor=doctor,
    )


@pytest.fixture
def patient_histories(patients, doctors):
    test_list = []
    for i in range(10):
        test_list.append(PatientHistory.objects.create(
            entry=i,
            creation_time=datetime.now(),
            patient=patients[i],
            doctor=doctors[i],
        ))
    return test_list


@pytest.fixture
def doctor():
    user = User.objects.create(username='x')
    user.groups.add(Group.objects.get(name='Doctor'))
    return user


@pytest.fixture
def doctors():
    test_list = []
    for i in range(10):
        user = User.objects.create(username='i')
        user.groups.add(Group.objects.get(name='Doctor'))
        test_list.append(user)
    return test_list


@pytest.fixture
def patient():
    user = User.objects.create(username='y')
    user.groups.add(Group.objects.get(name='Patient'))
    return user


@pytest.fixture
def patients():
    test_list = []
    for i in range(10):
        user = User.objects.create(username='i')
        user.groups.add(Group.objects.get(name='Patient'))
        test_list.append(user)
    return test_list
