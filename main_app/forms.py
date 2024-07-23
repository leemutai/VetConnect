from django import forms
from django.contrib.auth.models import User

from  django.contrib.auth.forms import  UserCreationForm 

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password1','password2']
        labels = {

            "email": "Email Address"
        }





# loginform
class LoginForm(forms.Form):
    username = forms.CharField(max_length=10)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)