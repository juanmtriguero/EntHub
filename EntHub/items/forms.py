#encoding:utf-8

from django import forms
from items import models

class ItemForm(forms.ModelForm):
    class Meta:
        abstract = True
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

class BookForm(ItemForm):
    class Meta(ItemForm.Meta):
        model = models.Book

class MovieForm(ItemForm):
    class Meta(ItemForm.Meta):
        model = models.Movie
        fields = ItemForm.Meta.fields + ['duration','category']
        labels = {
            'duration': 'Duración',
            'category': 'Categoría',
        }
        labels.update(ItemForm.Meta.labels)
        widgets = {
            'duration': forms.NumberInput(attrs={'class':'form-control'}),
            'category': forms.RadioSelect(),
        }
        widgets.update(ItemForm.Meta.widgets)

class SeriesForm(ItemForm):
    class Meta(ItemForm.Meta):
        model = models.Series
        fields = ItemForm.Meta.fields + ['status','category']
        labels = {
            'status': 'Status',
            'category': 'Categoría',
        }
        labels.update(ItemForm.Meta.labels)
        widgets = {
            'status': forms.RadioSelect(),
            'category': forms.RadioSelect(),
        }
        widgets.update(ItemForm.Meta.widgets)