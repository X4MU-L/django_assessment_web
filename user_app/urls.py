# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.homePage, name="home"),
    path("login/", views.loginPage, name="login"),
    path("signup/", views.signup, name="signup"),
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('health-worker-dashboard/', views.health_worker_dashboard, name='health_worker_dashboard'),
    path('create-medical-record/', views.create_medical_record, name='create_medical_record'),
    path('book-appointment/',views. book_appointment, name='book_appointment'),
]