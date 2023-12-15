from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    USER_HEALTH = "H"
    USER_PATIENT = "P"

    USER_TYPES_CHOICES = [
        (USER_HEALTH, "Heath Worker"),
        (USER_PATIENT, "Patient")
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    user_type = models.CharField(
        max_length=1, choices=USER_TYPES_CHOICES, default=USER_PATIENT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class MedicalRecord(models.Model):
    patient = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    malaria = models.BooleanField(default=False)
    ebola = models.BooleanField(default=False)
    typhoid = models.BooleanField(default=False)
    syphilis = models.BooleanField(default=False)
    tuberculosis = models.BooleanField(default=False)
    hiv_aids = models.BooleanField(default=False)
    blood_pressure = models.CharField(max_length=20, blank=True, null=True)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    genotype = models.CharField(max_length=5, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Appointment(models.Model):
    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='appointments')
    health_worker = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='appointments_assigned')
    date_time = models.DateTimeField()
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
