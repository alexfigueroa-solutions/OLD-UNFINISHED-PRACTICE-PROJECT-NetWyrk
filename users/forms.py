from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

#creates form for users to register as a new user
class UserRegisterForm(UserCreationForm):
    #creates email field 
    email = forms.EmailField()
    
    class Meta:
        #tels django that this model is a user
        model = User
        #tell django the fields that we would ask users to fill out
        fields = ['username', 'email','password1','password2']

#creates form for users to update their username or email
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']

#creates form for users to update profile
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','profile_pic','industry','occupational_title','specialization','display_name']
