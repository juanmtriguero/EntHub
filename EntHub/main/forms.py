#encoding:utf-8

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from items import models

class UserForm(UserCreationForm):
	class Meta:
		model = User
		fields = [
			'username',
			'first_name',
			'last_name',
			'email',
		]
		labels = {
			'username': 'Nombre de usuario',
			'first_name': 'Nombre',
			'last_name': 'Apellidos',
			'email': 'Correo electrónico',
		}

class AccountForm(forms.ModelForm):
	class Meta:
		model = models.Account
		fields = [
			'birth',
			'text',
			'avatar',
		]
		labels = {
			'birth': 'Fecha de nacimiento',
			'text': 'Texto personal',
			'avatar': 'Avatar',
		}
		widgets = {
			'birth': forms.DateInput(attrs={'class':'form-control'}),
			'text': forms.Textarea(attrs={'class':'form-control'}),
			'avatar': forms.URLInput(attrs={'class':'form-control'}),
		}