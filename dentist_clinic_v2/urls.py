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
from dentist_clinic.views import AboutContactView, AppointmentFormView, AppointmentListByDoctorView, AppointmentListByPatientView, DoctorListView, HomeView, PatientListView, RegisterView, RoomListView, UserLoginView, UserLogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('site/', include('django.contrib.auth.urls')),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('about-contact/', AboutContactView.as_view(), name='about-contact'),
    path('site/patient/appointments/<int:pk>/', AppointmentListByPatientView.as_view(), name='patient-appointment-list'),
    path('site/patient/appointments/<int:pk>/new', AppointmentFormView.as_view(), name='appointment-form'),
    path('site/doctor/appointments/<int:pk>/', AppointmentListByDoctorView.as_view(), name='doctor-appointment-list'),
    path('site/doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('site/patients/', PatientListView.as_view(), name='patient-list'),
    path('site/rooms/', RoomListView.as_view(), name='room-list'),

]
