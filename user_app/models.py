from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager,User
from django.db import models


# Create your models here.

class UserProfile(models.Model):
    USER_HEALTH = "H"
    USER_PATIENT = "P"

    USER_TYPES_CHOICES = [
        (USER_HEALTH, "Heath Worker"),
        (USER_PATIENT, "Patient")
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Appointment(models.Model):
    patient = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='appointments')
    health_worker = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='appointments_assigned')
    date_time = models.DateTimeField()
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
