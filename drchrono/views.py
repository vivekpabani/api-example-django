from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


def home(request):

    return render(request, 'home.html')

def login_view(request):

    return render(request, 'login.html')

@login_required
def logout_view(request):

    auth_logout(request)

    return redirect('/')
