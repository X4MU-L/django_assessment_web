from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import UserProfile, MedicalRecord, Appointment
from . import forms



def loginPage(request):
    """Login user into application"""
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            # get email and password
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            # get user details or None
            userP = UserProfile.objects.filter(user__username=username).first()
            if userP:
                # authenticate user
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    # if user is a patient
                    if userP.user_type == "P":
                        # redirect to patient endpoint
                        return redirect("patient_dashboard")
                    # redirect to health worker dashboard
                    return redirect("health_worker_dashboard")
                else:
                    # on authentication failure
                    messages.error(request, "incorrect email or password")
                    form_data = request.POST.copy()
                    form_data['password'] = '' 
                    form = forms.LoginForm(form_data)
                    return render(request, "login.html", {"form" : form })
            else:
                # if user is not found
                messages.error(request, "User does not exist")
                form_data = request.POST.copy()
                form_data['password'] = '' 
                form = forms.LoginForm(form_data)
                return render(request, "login.html", {"form" : form })
    
    # get request
    form = forms.LoginForm()
    return render(request, "login.html", {"form" : form })


def signup(request):
    """Create a user account"""
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            try:
                # email used as username
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password1")
                form.save()
                # authenticate user
                new_user = authenticate(request, username=username, password=password)
                if new_user is not None:
                    login(request, new_user)
                    if form.cleaned_data.get("user_type") == "P":
                        return redirect('patient_dashboard')
                return redirect("health_worker_dashboard")
            except Exception as ex:
                print(ex.message)
        else:
            # if error on form flash error
            messages.error(request,list(form.errors.as_data().values())[0][0].message.replace("username", "Email"))
            form_data = request.POST.copy()
            form_data['password1'] = ''
            form_data["password2"] = ""
            form = forms.SignupForm(form_data)
            return render(request, "signup.html", {"form" : form }) 
    
    # get request 
    form = forms.SignupForm()
    return render(request, "signup.html", {"form" : form})


@login_required(login_url="login")
def patient_dashboard(request):
    # get patient
    patient = request.user.userprofile
    if patient.user_type == "P":
        medical_records = MedicalRecord.objects.filter(patient=patient)
        appointments = Appointment.objects.filter(patient=patient)
        return render(request, 'patient_dashboard.html', {'medical_records': medical_records, 'appointments': appointments})
    # if not patient redirect to health worker dashboard
    return redirect('health_worker_dashboard')


@login_required(login_url="login")
def health_worker_dashboard(request):
    # get health worker
    health_worker = request.user.userprofile
    if health_worker.user_type == "H":
        appointments = Appointment.objects.filter(health_worker=health_worker)
        rejected_appointments = Appointment.objects.filter(health_worker=health_worker, is_rejected=True)
        return render(request, 'health_worker_dashboard.html', {'appointments': appointments, 'rejected_appointments': rejected_appointments})
    # if not a health worker redirect to patient dashboard
    return redirect('patient_dashboard')


@login_required(login_url="login")
def create_medical_record(request):
    if request.method == 'POST':
        form = forms.MedicalRecordForm(request.POST)
        if form.is_valid():
            medical_record = form.save(commit=False)
            medical_record.patient = request.user
            medical_record.save()
            return redirect('patient_dashboard')
    else:
        form = forms.MedicalRecordForm()
    return render(request, 'create_medical_record.html', {'form': form})


@login_required(login_url="login")
def book_appointment(request):
    if request.method == 'POST':
        form = forms.AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            return redirect('patient_dashboard')
    else:
        form = forms.AppointmentForm()
    return render(request, 'book_appointment.html', {'form': form})