from django.contrib.auth.mixins import LoginRequiredMixin
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


class RegisterView(CreateView):
    pass


class DoctorListView(View):
    pass


class PatientListView(View):
    pass


class RoomListView(View):
    pass


class AppointmentListByPatientView(View):
    pass


class AppointmentListByDoctorView(View):
    pass


class AppointmentListByRoom(View):
    pass


class AppointmentFormView(View):
    pass
