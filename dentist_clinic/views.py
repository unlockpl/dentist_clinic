from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.contrib import messages

from dentist_clinic.models import Appointment, PatientHistory, Procedure, Room, UserData
from dentist_clinic.forms import AppointmentModelForm, PatientHistoryModelForm, UserDataModelForm, UserModelForm


# Create your views here.

class DoctorUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Doctor').exists()


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')


class AboutContactView(ListView):
    model = UserData
    template_name = 'lists/about-contact.html'
    paginate_by = 5

    def get_queryset(self):
        return UserData.objects.filter(user__groups=Group.objects.get(name='Doctor')) \
            .order_by('user__last_name')


class ProcedureListView(ListView):
    model = Procedure
    template_name = 'lists/procedure-list.html'
    paginate_by = 5


class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    redirect_field_name = 'home'


class UserLogoutView(LogoutView):
    next_page = 'home'


class UserFormView(View):
    def get(self, request):
        context = {
            'userform': UserModelForm(),
            'userdataform': UserDataModelForm(),
        }
        return render(request, 'forms/profile-form.html', context)

    def post(self, request):
        user_form = UserModelForm(request.POST)
        user_data_form = UserDataModelForm(request.POST)

        if user_form.is_valid() and user_data_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            user.groups.add(Group.objects.get(name="Patient"))
            user.save()
            user_form.save_m2m()
            user_data = user_data_form.save(commit=False)
            user_data.user = user
            user_data.save()
            messages.success(request, "OK")
        else:
            messages.error(request, "error")

        return redirect('home')


class AppointmentFormView(CreateView):
    model = Appointment
    form_class = AppointmentModelForm
    template_name = 'forms/appointment-form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.patient_id = self.kwargs['pk']
        for room in Room.objects.all():
            if not Appointment.objects.filter(room=room).filter(date=obj.date):
                obj.room = room
                break
        obj.save()
        self.object = obj
        return redirect(self.get_success_url())


class PatientHistoryFormView(CreateView):
    model = PatientHistory
    form_class = PatientHistoryModelForm
    template_name = 'forms/history-form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.patient_id = self.kwargs['pk']
        obj.doctor = self.request.user
        obj.save()
        self.object = obj
        return redirect(self.get_success_url())


class DoctorListView(DoctorUserMixin, ListView):
    model = UserData
    template_name = 'lists/doctor-list.html'
    paginate_by = 5

    def get_queryset(self):
        return UserData.objects.filter(user__groups=Group.objects.get(name='Doctor')) \
            .order_by('user__last_name')


class PatientListView(DoctorUserMixin, ListView):
    model = UserData
    template_name = 'lists/patient-list.html'
    paginate_by = 5

    def get_queryset(self):
        return UserData.objects.filter(user__groups=Group.objects.get(name='Patient')) \
            .order_by('user__last_name')


class RoomListView(DoctorUserMixin, ListView):
    model = Room
    template_name = 'lists/room-list.html'
    paginate_by = 5


class AppointmentListByPatientView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Appointment
    template_name = 'lists/appointment-list.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(AppointmentListByPatientView, self).get_context_data(**kwargs)
        patient = User.objects.get(pk=self.kwargs['pk'])
        context['header'] = f"Appointments of patient {patient.first_name} {patient.last_name}"
        return context

    def get_queryset(self):
        return Appointment.objects.filter(patient__pk=self.kwargs['pk']).order_by('date')

    def test_func(self):
        return self.request.user.groups.filter(name='Doctor').exists() or self.request.user.pk == self.kwargs['pk']


class AppointmentListByDoctorView(DoctorUserMixin, ListView):
    model = Appointment
    template_name = 'lists/appointment-list.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(AppointmentListByDoctorView, self).get_context_data(**kwargs)
        doctor = User.objects.get(pk=self.kwargs['pk'])
        context['header'] = f"Appointments of doctor {doctor.first_name} {doctor.last_name}"
        return context

    def get_queryset(self):
        return Appointment.objects.filter(doctor__pk=self.kwargs['pk']).order_by('date')


class AppointmentListByRoomView(DoctorUserMixin, ListView):
    model = Appointment
    template_name = 'lists/appointment-list.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(AppointmentListByRoomView, self).get_context_data(**kwargs)
        context['header'] = f"Appointments in room {Room.objects.get(pk=self.kwargs['pk'])}"
        return context

    def get_queryset(self):
        return Appointment.objects.filter(room__pk=self.kwargs['pk']).order_by('date')


class PatientHistoryListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = PatientHistory
    template_name = 'lists/history-list.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(PatientHistoryListView, self).get_context_data(**kwargs)
        patient = User.objects.get(pk=self.kwargs['pk'])
        context['header'] = f"Patient history of {patient.first_name} {patient.last_name}"
        return context

    def get_queryset(self):
        return PatientHistory.objects.filter(patient__pk=self.kwargs['pk']).order_by('creation_time')

    def test_func(self):
        return self.request.user.groups.filter(name='Doctor').exists() or self.request.user.pk == self.kwargs['pk']


class DoctorHistoryListView(DoctorUserMixin, ListView):
    model = PatientHistory
    template_name = 'lists/history-list.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(DoctorHistoryListView, self).get_context_data(**kwargs)
        doctor = User.objects.get(pk=self.kwargs['pk'])
        context['header'] = f"Patient histories written by {doctor.first_name} {doctor.last_name}"
        return context

    def get_queryset(self):
        return PatientHistory.objects.filter(doctor__pk=self.kwargs['pk']).order_by('creation_time')


class AppointmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Appointment
    template_name = 'forms/update.html'
    form_class = AppointmentModelForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super(AppointmentUpdateView, self).get_context_data(**kwargs)
        context['header'] = "Update patient history"
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        for room in Room.objects.all():
            if not Appointment.objects.filter(room=room).filter(date=obj.date):
                obj.room = room
                break
        obj.save()
        self.object = obj
        return redirect(self.get_success_url())

    def test_func(self):
        appointment = Appointment.objects.get(pk=self.kwargs['pk'])
        return self.request.user.groups.filter(name='Doctor').exists() or self.request.user == appointment.patient


class AppointmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Appointment
    success_url = reverse_lazy('home')
    template_name = 'delete.html'

    def test_func(self):
        appointment = Appointment.objects.get(pk=self.kwargs['pk'])
        return self.request.user.groups.filter(name='Doctor').exists() or self.request.user == appointment.patient


class PatientHistoryUpdateView(DoctorUserMixin, UpdateView):
    model = PatientHistory
    template_name = 'forms/update.html'
    form_class = PatientHistoryModelForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super(PatientHistoryUpdateView, self).get_context_data(**kwargs)
        context['header'] = "Update patient history"
        return context


class PatientHistoryDeleteView(DoctorUserMixin, DeleteView):
    model = PatientHistory
    success_url = reverse_lazy('home')
    template_name = 'delete.html'


class PatientHistoryDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = PatientHistory
    template_name = 'details/history-details.html'

    def test_func(self):
        history = PatientHistory.objects.get(pk=self.kwargs['pk'])
        return self.request.user.groups.filter(name='Doctor').exists() or self.request.user == history.patient


class UserUpdateView(LoginRequiredMixin, View):

    def get(self, request):
        user = self.request.user
        context = {
            'user': user,
            'user_data': UserData.objects.get(user=user),
            'user_form': UserModelForm(),
            'user_data_form': UserDataModelForm(),
        }
        return render(request, 'forms/update-user.html', context)

    def post(self, request):
        pass



class UserDetailView(LoginRequiredMixin, View):
    def get(self, request):
        user = self.request.user
        user_data = UserData.objects.get(user=user)
        context = {
            'user': user,
            'user_data': user_data
        }
        return render(request, 'details/profile-details.html', context)
