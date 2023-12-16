# forms.py

from typing import Any
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserModel
from .models import MedicalRecord, Appointment, UserProfile

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['malaria', 'ebola', 'typhoid', 'syphilis', 'tuberculosis', 'hiv_aids']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["date_time"]

class LoginForm(forms.Form):
    username = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}),
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Enter Password'}),
    )


    class Meta:
        model = User
        fields = ["username", "password"]
        
        
        
class SignupForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First Name'}),
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last Name'}),
    )
    # email used as username
    username = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}),
    )

    password1 = forms.CharField(
        label="Password",
        min_length=8,
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Enter Password'}),
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Confirm Password'}),
    )

    user_type = forms.ChoiceField(
        choices=UserProfile.USER_TYPES_CHOICES,
        widget=forms.Select(attrs={'class': 'form-input-select'}),
        label='Category',
        initial=UserProfile.USER_PATIENT,
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password1", "password2", "user_type"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

            user_profile = UserProfile.objects.create(
                user=user,
                user_type=self.cleaned_data["user_type"]
            )

        return user_profile