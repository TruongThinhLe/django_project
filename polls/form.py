from django import forms
from .models import *

class Word_form(forms.ModelForm):
    class Meta:
        model =English
        fields=['word']

class Form_mean(forms.Form):
    mean=forms.CharField(label="Mean",max_length=50)
    example=forms.CharField(label="Example",max_length=100)

class DateInput(forms.DateInput):
    input_type='date'
    
class Plan_form(forms.ModelForm):
    class Meta:
        model=Plan
        fields=['plan','date_end','date_start']
        widgets={'date_end':DateInput(),'date_start':DateInput()}