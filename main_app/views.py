from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mass_mail
from django.shortcuts import render, redirect
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from authentication import settings
from django.contrib.sites.shortcuts import get_current_site

from main_app.tokens import account_activation_token


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


def register(request):
    username_error = first_name_error = last_name_error = email_error = password_error = confirm_password_error = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if not username:
            username_error = 'This field is required'
        if len(username) < 3:
            username_error = 'Minimum 3 character required'
        if User.objects.filter(username=username).exists():
            username_error = 'Username is already taken'
        if not first_name:
            first_name_error = 'This field is required'
        if not last_name:
            last_name_error = 'This field is required'
        if not email:
            email_error = 'This field is required'
        if User.objects.filter(email=email).exists():
            email_error = 'This email already exists'
        if not password:
            password_error = 'This field is required'
        if len(password) < 8:
            password_error = 'Minimum 8 characters required'
        # if not re.search(r"A-Z", password):
        #     password_error = 'At least one uppercase letter'
        # if not re.search(r"a-z", password):
        #     password_error = 'At least one lowercase letter'
        # if not re.search(r"\d", password):
        #     password_error = 'At least one digit '
        # if not re.search(r"[!@^#$%&*()+]", password):
        #     password_error = 'At least one special character'
        if not confirm_password:
            confirm_password_error = 'This field is required'
        if password != confirm_password:
            confirm_password_error = 'password did not match'
        if any([username_error, first_name_error, last_name_error, email_error, password_error,
                confirm_password_error]):
            context = {
                'username_error': username_error,
                'first_name_error': first_name_error,
                'last_name_error': last_name_error,
                'email_error': email_error,
                'password_error': password_error,
                'confirm_password_error': confirm_password_error,
            }
            return render(request, 'Accounts/register.html', {'context': context})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = False
        user.save()
        #     sending welcome email
        subject1 = 'Welcome to django authentication system'
        message1 = (f"Hello {user.get_full_name()}.\n\n Thank you for registering to our website!!!\n Please check "
                    f"your inbox and follow instruction to complete your registration.")
        from_email = settings.EMAIL_HOST_USER
        to_list1 = [email]
        email1 = (subject1, message1, from_email, to_list1)
        #  sending email activation
        current_site = get_current_site(request)
        subject2 = "Activate your account"
        message2 = render_to_string('Accounts/email_activation.html', {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user)
        })
        to_list2 = [email]
        email2 = (subject2, message2, settings.EMAIL_HOST_USER, to_list2)
        send_mass_mail((email1, email2), fail_silently=True)
        messages.success(request, 'Account created successfully Please check your email to confirm')
        return redirect('home')
    context = {
        'username_error': username_error,
        'first_name_error': first_name_error,
        'last_name_error': last_name_error,
        'email_error': email_error,
        'password_error': password_error,
        'confirm_password_error': confirm_password_error,
    }

    return render(request, 'Accounts/register.html', {'context': context})


def login_view(request):
    username_error = password_error = ""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username:
            username_error = 'This field is required'
        if not password:
            password_error = 'This field is required'
        if any([username_error, password_error]):
            context = {
                'username_error': username_error,
                'password_error': password_error,
            }
            return render(request, 'Accounts/login.html', {'context': context})

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have logged in successfully')
            return redirect('home')
        else:
            messages.error(request, 'invalid credentials')

    context = {
        'username_error': username_error,
        'password_error': password_error,
    }
    return render(request, 'Accounts/login.html', {'context': context})


# activate account
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Your account has been activated')
        return redirect('login')
    else:
        messages.error(request, 'Email activation failed')
        return redirect('home')


def logout_view(request):
    logout(request)
    messages.success(request, 'you have successfully logout')
    return redirect('home')
