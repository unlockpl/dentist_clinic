"""dentist_clinic_v2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from dentist_clinic.views import AboutContactView, AppointmentDeleteView, AppointmentFormView, \
    AppointmentListByDoctorView, AppointmentListByPatientView, AppointmentListByRoomView, AppointmentUpdateView, \
    DoctorHistoryListView, DoctorListView, HomeView, PatientHistoryDeleteView, PatientHistoryDetailView, \
    PatientHistoryFormView, PatientHistoryListView, PatientHistoryUpdateView, PatientListView, ProcedureListView, \
    RoomListView, UserDetailView, UserFormView, UserLoginView, UserLogoutView, UserUpdateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('login/', include('django.contrib.auth.urls')),
    path('login/', UserLoginView.as_view(), name='login-user'),
    path('logout/', UserLogoutView.as_view(), name='logout-user'),
    path('register/', UserFormView.as_view(), name='register-user'),
    path('profile/', UserDetailView.as_view(), name='profile-user'),
    path('profile/update/', UserUpdateView.as_view(), name='update-user'),
    path('about-contact/', AboutContactView.as_view(), name='about-contact'),
    path('services/', ProcedureListView.as_view(), name='procedure-list'),
    path('patient/<int:pk>/appointments/new/', AppointmentFormView.as_view(), name='appointment-form'),
    path('patient/<int:pk>/appointments/', AppointmentListByPatientView.as_view(), name='appointment-list-by-patient'),
    path('doctor/<int:pk>/appointments/', AppointmentListByDoctorView.as_view(), name='appointment-list-by-doctor'),
    path('room/<int:pk>/appointments/', AppointmentListByRoomView.as_view(), name='appointment-list-by-room'),
    path('patient/<int:pk>/history/new/', PatientHistoryFormView.as_view(), name='patient-history-form'),
    path('patient/<int:pk>/history/', PatientHistoryListView.as_view(), name='patient-history-list'),
    path('doctor/<int:pk>/history/', DoctorHistoryListView.as_view(), name='doctor-history-list'),
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('patients/', PatientListView.as_view(), name='patient-list'),
    path('rooms/', RoomListView.as_view(), name='room-list'),
    path('appointment/<int:pk>/update/', AppointmentUpdateView.as_view(), name='appointment-update'),
    path('appointment/<int:pk>/delete/', AppointmentDeleteView.as_view(), name='appointment-delete'),
    path('history/<int:pk>/update/', PatientHistoryUpdateView.as_view(), name='patient-history-update'),
    path('history/<int:pk>/delete/', PatientHistoryDeleteView.as_view(), name='patient-history-delete'),
    path('history/<int:pk>/details/', PatientHistoryDetailView.as_view(), name='patient-history-details'),
]
