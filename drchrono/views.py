from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .util import (get_patient_data,
                   get_patients_with_recent_birthday,
                   send_email_util)


@login_required
def home(request):
    """
    home view to display patient data whose birthday is nearby.
    """

    access_token = request.user.social_auth.get(provider='drchrono').extra_data['access_token']

    patients = get_patient_data(access_token)

    sorted_patients_with_daydiff = get_patients_with_recent_birthday(patients)

    context = {'patient_list': sorted_patients_with_daydiff}

    return render(request, 'home.html', context)

def login_view(request):

    return render(request, 'login.html')

@login_required
def logout_view(request):

    auth_logout(request)

    return redirect('/')

def send_email(request):

    if request.method == "POST":
        greet_message = request.POST.get("greet_message", "")
        greet_email = request.POST.get("greet_email", "")

        if send_email_util(greet_email, greet_message):
            return HttpResponse("Greeted")

    return HttpResponse("Failed")
