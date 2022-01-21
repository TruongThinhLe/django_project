from django import forms
from django.db.models import fields
from django.forms import widgets
from .models import *
from django.contrib.auth import get_user_model

User=get_user_model

class Word_form(forms.ModelForm):
    class Meta:
        model =English
        fields=['word']

class Num_form(forms.Form):
    number_quiz=forms.IntegerField(max_value=50)

class Form_mean(forms.Form):
    mean=forms.CharField(label="Mean",max_length=50)
    example=forms.CharField(label="Example",max_length=100)
    type=forms.CharField(label="Type",max_length=10)

class DateInput(forms.DateInput):
    input_type='date'
    
class Plan_form(forms.ModelForm):
    class Meta:
        model=Plan
        fields=['plan','date_end','date_start','time_todo','period_day']
        widgets={'date_end':DateInput(),'date_start':DateInput()}

class Todo_form(forms.ModelForm):
    class Meta:
        model=List_todo
        fields=['Task_todo','Time_todo']
        widgets={'Task_todo':forms.TextInput(attrs={'class':"form_task"})}

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"loginform"}))

class Note_Form(forms.ModelForm):
    class Meta:
        model=Note
        fields=["Note","Detail"]
        widgets={'Note':forms.Textarea(attrs={'rows':'2'}),'Detail':forms.Textarea(attrs={'rows':'2'})}

class Challenge_form(forms.ModelForm):
    class Meta:
        model=Challenge
        fields=["Challenge"]
        widgets={'Challenge':forms.Textarea(attrs={'rows':'1'})}