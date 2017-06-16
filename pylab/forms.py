from django.forms import ModelForm
from django import forms
from .models import Names


class NamesForm(ModelForm):
    class Meta:
        model = Names
        fields = ['name']
        widgets = {
            'name': forms.TextInput(
                attrs={'id': 'name-text', 'required': True, 'placeholder': 'name...'}
            ),
        }
