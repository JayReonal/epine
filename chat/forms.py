from django.forms import ModelForm
from django import forms
from .models import *

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'slug', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control',})
        self.fields['slug'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Number of pineapple planted'})

