from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView, UpdateView

from dentist_clinic.models import Appointment, PatientHistory, Procedure, Room, UserData


# Create your views here.

class DoctorUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Doctor').exists()


class PatientUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Patient').exists()


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


class AppointmentFormView(View):
    pass


class DoctorListView(DoctorUserMixin, ListView):
    model = UserData
    template_name = 'lists/doctor-list.html'
    paginate_by = 50

    def get_queryset(self):
        print(UserData.objects.filter(user__groups=Group.objects.filter(name='Doctor').first()).order_by('user__last_name'))
        return UserData.objects.filter(user__groups=Group.objects.filter(name='Doctor').first())\
            .order_by('user__last_name')


class PatientListView(DoctorUserMixin, ListView):
    model = UserData
    template_name = 'lists/patient-list.html'
    paginate_by = 50

    # def get_queryset(self):
    #     return UserData.objects.filter(user__groups=Group.objects.filter(name='Patient').first())\
    #         .order_by('-user__last_name')


class RoomListView(DoctorUserMixin, ListView):
    model = Room
    template_name = 'lists/room-list.html'
    paginate_by = 50


class AppointmentListByPatientView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Appointment
    template_name = 'lists/appointment-list-by-patient.html'
    paginate_by = 50

    def get_queryset(self):
        return Appointment.objects.filter(patient__pk=self.kwargs['pk']).order_by('-date')

    def test_func(self):
        return self.request.user.groups.filter(name='Doctor').exists() or self.request.user.pk == self.kwargs['pk']


class AppointmentListByDoctorView(DoctorUserMixin, ListView):
    model = Appointment
    template_name = 'lists/appointment-list-by-doctor.html'
    paginate_by = 50

    def get_queryset(self):
        return Appointment.objects.filter(doctor__pk=self.kwargs['pk']).order_by('-date')


class AppointmentListByRoomView(ListView):
    model = Appointment
    template_name = 'lists/appointment-list-by-room.html'
    paginate_by = 50

    def get_queryset(self):
        return Appointment.objects.filter(room__pk=self.kwargs['pk']).order_by('-date')


class AppointmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        appointment = Appointment.objects.get(pk=self.kwargs['pk'])
        return self.request.user.groups.filter(name='Doctor').exists() or self.request.user == appointment.patient


class AppointmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Appointment
    success_url = reverse_lazy('home')
    template_name = 'home.html'

    def test_func(self):
        appointment = Appointment.objects.get(pk=self.kwargs['pk'])
        return self.request.user.groups.filter(name='Doctor').exists() or self.request.user == appointment.patient
