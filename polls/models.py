from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import BooleanField, DateField, DecimalField, IntegerField, TextField
from django.db.models.fields.related import ForeignKey
	
class English(models.Model):
    word=models.CharField(max_length=20)
    pub_date=models.DateField(auto_now_add=True)
    meaning= models.TextField(max_length=50,null=True)
    example=models.TextField(max_length=100,null=True)
    type=models.TextField(max_length=10,null=True)
    def __str__ (self):
        return self.word

class Plan(models.Model):
    plan=models.CharField(max_length=50)
    date_end=models.DateField()
    date_start=models.DateField()
    status=models.IntegerField(null=True)
    time_todo=models.DecimalField(max_digits=10,decimal_places=2)
    period_day=models.IntegerField(default=1)
    
class List_todo(models.Model):
    Day_todo=DateField(null=True)
    Task_todo=TextField(max_length=50)   
    Check_done=BooleanField(default=False)
    Time_todo=DecimalField(null=True,max_digits=10,decimal_places=2)
    def __str__(self):
        return self.Task_todo

class Sub_do():
    def __init__(self,day):
        self.tasks=list(List_todo.objects.filter(Day_todo=day))
        self.day=day.strftime('%A')
    def __str__(self):
        return self.day

class Note(models.Model):
    Note=TextField(max_length=50)
    Time_pub=DateField(auto_now_add=True)
    Detail=TextField(max_length=100)
    def __str__(self):
        return self.Note

class Challenge(models.Model):
    Challenge=TextField(max_length=50)
    Time_pub=DateField(auto_now_add=True)
    Status=BooleanField(default=False)
    def __str__(self):
        return self.Challenge
    
# Create your models here