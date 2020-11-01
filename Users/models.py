# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    is_alumini = models.BooleanField(default=False)
    is_college = models.BooleanField(default=False)

class Topic(models.Model):
    text=models.CharField(max_length=200)
    date_added=models.DateTimeField(auto_now_add=True)
    owner=models.ForeignKey('College',on_delete=models.CASCADE)
    def __str__(self):
        return self.text
class Entry(models.Model):
    topic=models.ForeignKey('Topic',on_delete=models.CASCADE)
    text=models.TextField()
    date_added=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural='entries'
    def __str__(self):
        return self.text[:50]+'...'


class College(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    def __str__(self):
        return self.user.username
class Alumini(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    college=models.ForeignKey('College',on_delete=models.CASCADE,default=1)
    location=models.ForeignKey('Locations',on_delete=models.CASCADE,default=1)
    salary=models.ForeignKey('Salary',on_delete=models.CASCADE,default=1)
    def __str__(self):
        return self.user.username

class Locations(models.Model):
    location=models.CharField(max_length=200)
    def __str__(self):
        return self.location

class Salary(models.Model):
    salary=models.CharField(max_length=200)
    def __str__(self):
        return self.salary