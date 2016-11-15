#encoding:utf-8

from django import forms
from items import models

# Book

class BookForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = ['title','year','description','image','genres']
        labels = {
        	'title': 'Título',
        	'year': 'Año',
        	'description': 'Descripción',
        	'image': 'Imagen',
        	'genres': 'Géneros',
        }
        widgets = {
        	'title': forms.TextInput(attrs={'class':'form-control'}),
        	'year': forms.NumberInput(attrs={'class':'form-control'}),
        	'description': forms.Textarea(attrs={'class':'form-control'}),
        	'image': forms.URLInput(attrs={'class':'form-control'}),
        	'genres': forms.CheckboxSelectMultiple(),
        }
		