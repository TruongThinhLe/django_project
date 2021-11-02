from django.db import models
	
class English(models.Model):
    word=models.CharField(max_length=20)
    pub_date=models.DateField(auto_now_add=True)
    meaning= models.TextField(max_length=50,null=True)
    example=models.TextField(max_length=50,null=True)
    def __str__ (self):
        return self.word
class Plan(models.Model):
    plan=models.CharField(max_length=50)
    date_end=models.DateField()
    date_start=models.DateField()
    status=models.IntegerField(null=True)
    
    
    def __str__(self):
        return self.plan
# Create your models here