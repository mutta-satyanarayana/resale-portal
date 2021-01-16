from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import UserProfile
from django.forms import ModelForm
#from django.contrib.auth import authenticate,LoginForm

class UserRegisterForm(UserCreationForm):
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={
		"class":"form-control",
		"placeholder":"Enter Password",
		}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={
		"class":"form-control",
		"placeholder":"Enter Confirm Password",
		}))
	class Meta:
		model = User
		fields = ["username",'email','password1','password2']
		widgets = {
		"username":forms.TextInput(attrs={
			"class":"form-control",
			"placeholder":"Enter Your Username",
			"required":True,
			}),
		}


class UpdateProfile(forms.ModelForm):
	email = forms.EmailField(widget = forms.EmailInput(attrs= {'readonly':'readonly'}))
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email']


class ViewProfile(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['mobile','address','city','country','image']

