from django.forms import ModelForm
from django import forms
from .models import *
from django.forms.widgets import DateInput, Select 

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Input the type of pineapple here...'})

class DateInput(forms.DateInput):
    input_type = 'date'

class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['category', 'number_planted', 'plant_date']

        widgets = {
            'category': Select(attrs={'class': 'form-control'}),
            'number_planted': forms.TextInput(attrs={'class': 'form-control'}),
            'plant_date': DateInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'number_planted': 'Total Planted',
        }
class YieldForm(forms.ModelForm):
    class Meta:
        model = Yield
        fields = ['category', 'number_yield', 'harvest_date']
        
        widgets = {
            'category': Select(attrs={'class': 'form-control'}),
            'number_yield': forms.TextInput(attrs={'class': 'form-control'}),
            'harvest_date': DateInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'number_yield': 'Total Harvest',
        }

class BadPineForm(forms.ModelForm):
    class Meta:
        model = BadPine
        fields = ['category', 'number_yield', 'harvest_date']
        
        widgets = {
            'category': Select(attrs={'class': 'form-control'}),
            'number_yield': forms.TextInput(attrs={'class': 'form-control'}),
            'harvest_date': DateInput(attrs={'class': 'form-control'}),
        }

class WorkerPayForm(forms.ModelForm):
    class Meta:
        model = WorkerPays
        fields = ['name', 'price_pay', 'workers', 'date']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price_pay': forms.TextInput(attrs={'class': 'form-control'}),
            'workers': forms.TextInput(attrs={'class': 'form-control'}),
            'date': DateInput(attrs={'class': 'form-control'}),
        }
        
        labels = {
            'name': 'Expenses for',
            'price_pay': 'Price Expense',
            'workers': 'Number of Workers or Suckers of Pineapple'
        }

class YieldSearchForm(forms.ModelForm):
   export_to_CSV = forms.BooleanField(required=False)
   class Meta:
     model = Yield
     fields = ['category',]
     
   def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'form-control'})

class PriceForm(forms.ModelForm):
    class Meta:
        model = PinePrice
        fields = ['price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price'].widget.attrs.update({'class': 'form-control',})

class ValueForm(forms.ModelForm):
    class Meta:
        model = PineValue
        fields = ['value']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['value'].widget.attrs.update({'class': 'form-control',})


class BiddingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BiddingForm, self).__init__(*args, **kwargs)
        # Modify the user field queryset to only include users from the "buyer" group
        self.fields['user'].queryset = User.objects.filter(groups__name='buyer')

    class Meta:
        model = BiddingProcess
        fields = ['user', 'bid_price',]

        widgets = {
            'user': Select(attrs={'class': 'form-control'}),
            'bid_price': forms.TextInput(attrs={'class': 'form-control'}),
        }