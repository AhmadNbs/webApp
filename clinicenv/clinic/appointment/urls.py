from django.contrib import admin
from django.urls import path
from . import views
urlpatterns =[
    path('', views.homepage, name='homepage'),
    path('manage', views.manage_page, name='manage'),
    path('appointment/', views.appointment, name='appointment'),
    path('success_page/', views.success_page, name='success_page'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('appointment_list_doctor', views.appointment_list_doctor, name='appointment_list_doctor'),

    path('manage_working_schedule/', views.manage_working_schedule, name='manage_working_schedule'),
    path('manage_unavailable_dates/', views.manage_unavailable_dates, name='manage_unavailable_dates'),
    path('update_clinic_appointment_list/', views.update_clinic_appointment_list, name = 'update_clinic_appointment_list'),
    path('clinic_appointment_list/', views.clinic_appointment_list, name = 'clinic_appointment_list'),

]