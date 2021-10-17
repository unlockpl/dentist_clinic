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
    model = UserData
    template_name = 'lists/about-contact.html'
    paginate_by = 50

    def get_queryset(self):
        return UserData.objects.filter(user__groups=Group.objects.get(name='Doctor'))\
            .order_by('user__last_name')


class UserLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    redirect_field_name = 'home'


class UserLogoutView(LogoutView):
    next_page = 'home'


class UserFormView(View):
    pass


class AppointmentFormView(View):
    pass


class PatientHistoryFormView(View):
    pass


class DoctorListView(DoctorUserMixin, ListView):
    model = UserData
    template_name = 'lists/doctor-list.html'
    paginate_by = 50

    def get_queryset(self):
        return UserData.objects.filter(user__groups=Group.objects.get(name='Doctor'))\
            .order_by('user__last_name')


class PatientListView(DoctorUserMixin, ListView):
    model = UserData
    template_name = 'lists/patient-list.html'
    paginate_by = 50

    def get_queryset(self):
        return UserData.objects.filter(user__groups=Group.objects.get(name='Patient'))\
            .order_by('user__last_name')


class RoomListView(DoctorUserMixin, ListView):
    model = Room
    template_name = 'lists/room-list.html'
    paginate_by = 50


class AppointmentListByPatientView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Appointment
    template_name = 'lists/appointment-list.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(AppointmentListByPatientView, self).get_context_data(**kwargs)
        patient = User.objects.get(pk=self.kwargs['pk'])
        context['title'] = f"Appointments of patient {patient.first_name} {patient.last_name}"
        return context

    def get_queryset(self):
        return Appointment.objects.filter(patient__pk=self.kwargs['pk']).order_by('date')

    def test_func(self):
        return self.request.user.groups.filter(name='Doctor').exists() or self.request.user.pk == self.kwargs['pk']


class AppointmentListByDoctorView(DoctorUserMixin, ListView):
    model = Appointment
    template_name = 'lists/appointment-list.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(AppointmentListByDoctorView, self).get_context_data(**kwargs)
        doctor = User.objects.get(pk=self.kwargs['pk'])
        context['title'] = f"Appointments of doctor {doctor.first_name} {doctor.last_name}"
        return context

    def get_queryset(self):
        return Appointment.objects.filter(doctor__pk=self.kwargs['pk']).order_by('date')


class AppointmentListByRoomView(DoctorUserMixin, ListView):
    model = Appointment
    template_name = 'lists/appointment-list.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(AppointmentListByRoomView, self).get_context_data(**kwargs)
        context['title'] = f"Appointments in room {Room.objects.get(pk=self.kwargs['pk'])}"
        return context

    def get_queryset(self):
        return Appointment.objects.filter(room__pk=self.kwargs['pk']).order_by('date')


class PatientHistoryListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = PatientHistory
    template_name = 'lists/history-list.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(PatientHistoryListView, self).get_context_data(**kwargs)
        patient = User.objects.get(pk=self.kwargs['pk'])
        context['title'] = f"Patient history of {patient.first_name} {patient.last_name}"
        return context

    def get_queryset(self):
        return PatientHistory.objects.filter(patient__pk=self.kwargs['pk']).order_by('creation_time')

    def test_func(self):
        return self.request.user.groups.filter(name='Doctor').exists() or self.request.user.pk == self.kwargs['pk']


class DoctorHistoryListView(DoctorUserMixin, ListView):
    model = PatientHistory
    template_name = 'lists/history-list.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(DoctorHistoryListView, self).get_context_data(**kwargs)
        doctor = User.objects.get(pk=self.kwargs['pk'])
        context['title'] = f"Patient histories written by {doctor.first_name} {doctor.last_name}"
        return context

    def get_queryset(self):
        return PatientHistory.objects.filter(doctor__pk=self.kwargs['pk']).order_by('creation_time')


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


class PatientHistoryUpdateView(DoctorUserMixin, UpdateView):
    pass


class PatientHistoryDeleteView(DoctorUserMixin, DeleteView):
    model = PatientHistory
    success_url = reverse_lazy('home')
    template_name = 'home.html'

    def get_object(self):
        return PatientHistory.objects.get(pk=self.kwargs['pk'])


class PatientHistoryDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):

    def test_func(self):
        history = PatientHistory.objects.get(pk=self.kwargs['pk'])
        return self.request.user.groups.filter(name='Doctor').exists() or self.request.user == history.patient
