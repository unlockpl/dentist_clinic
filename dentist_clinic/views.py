from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView, UpdateView

from dentist_clinic.models import Appointment, PatientHistory, Procedure, Room, UserData


# Create your views here.


def doctor_login_check(user):
    return user.groups.filter(name='Doctor').exists()


class HomeView(View):

    def get(self, request):
        return render(request, 'home.html')


class AboutContactView(ListView):
    pass


class UserLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    redirect_field_name = 'home'


class UserLogoutView(LogoutView):
    next_page = 'home'


class UserFormView(View):
    pass


class UserDataFormView(View):
    pass


class DoctorListView(ListView):
    model = UserData
    template_name = 'lists/doctor-list.html'
    paginate_by = 50

    def get_queryset(self):
        return UserData.objects.filter(user__groups=Group.objects.filter(name='Doctor').first())\
            .order_by('user__last_name')


class PatientListView(ListView):
    model = UserData
    template_name = 'lists/patient-list.html'
    paginate_by = 50

    def get_queryset(self):
        return UserData.objects.filter(user__groups=Group.objects.filter(name='Patient').first())\
            .order_by('user__last_name')


class RoomListView(ListView):
    model = Room
    template_name = 'lists/room-list.html'
    paginate_by = 50


class AppointmentListByPatientView(View):
    pass


class AppointmentListByDoctorView(View):
    pass


class AppointmentListByRoomView(View):
    pass


class AppointmentFormView(View):
    pass
