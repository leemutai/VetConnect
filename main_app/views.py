from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
from .forms import UserRegistrationForm,LoginForm
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    return render(request, 'home.html')


def find(request):
    return render(request, 'find.html')


def supplies(request):
    return render(request, 'supplies.html')


def agrovet(request):
    return render(request, 'agrovet.html')


def community(request):
    return render(request, 'community.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


# signupview

def signup(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            messages.success(request, 'Account is created successful')
            return redirect('signin')
    else:
        form = UserRegistrationForm()
    return render(request, 'Accounts/register.html', {'form': form})


# loginview
@csrf_exempt
def signin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful')
                return redirect('home')
            else:
                messages.error(request, 'Invalid Credentials')
    else:
        form = LoginForm()

    return render(request, 'Accounts/login.html', {'form': form})


# logoutview
@csrf_exempt
@login_required
def signout(request):
    logout(request)
    messages.success(request, 'Logout successful')
    return redirect('index')