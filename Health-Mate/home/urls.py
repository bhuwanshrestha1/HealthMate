from django.contrib import admin
from django.urls import path
from home import views
from django.conf import settings
from django.conf.urls.static import static
from .views import my_appointment, cancel_appointment
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


urlpatterns = [
    path("",views.index, name='index'),
    path("home",views.index, name='index'),
    path("about",views.about, name="about"),
    path("patient_login",views.patient_login, name="patient_login"),
    path("patient_list",views.patient_list, name="patient_list"),
    path("patient_register",views.patient_register, name="patient_register"),
    path("doctor_login",views.doctor_login, name="doctor_login"),
    path("admin_login",views.admin_login, name="admin_login"),
    path("admin_profile",views.admin_profile, name="admin_profile"),
    path("patient_profile",views.patient_profile, name="patient_profile"),
    path("log_out",views.log_out, name="log_out"),
     path("log_out1",views.log_out1, name="log_out1"),    
    path("book_appointment",views.book_appointment, name="book_appointment"),
    path("book_now/<int:doctor_id>/",views.book_now, name="book_now"),
    path("patient_details",views.patient_details, name="patient_details"),
    path("book_no_recommendation",views.book_no_recommendation, name="book_no_recommendation"),
    path("book_recommendation",views.book_recommendation, name="book_recommendation"),
    path("doctor_home",views.doctor_home, name="doctor_home"),
    path("doctor_list",views.doctor_list, name="doctor_list"),
    path("doctor_profile",views.doctor_profile, name="doctor_profile"),
    path("add_doctor",views.add_doctor, name="add_doctor"),
    path("result_template",views.result_template, name="result_template"),
    path("my_appointment",views.my_appointment, name="my_appointment"),
    path("doctor_appointments",views.doctor_appointments, name="doctor_appointments"),
    path("review/<int:appointment_id>/", views.review, name="review"),
    path("edit_doctor/<int:doctor_id>/", views.edit_doctor, name="edit_doctor"),
    path("cancel_appointment/<int:appointment_id>/", login_required(cancel_appointment), name="cancel_appointment"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)