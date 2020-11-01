from django.contrib import admin
from .models import Topic,Entry,User,College,Alumini,Locations,Salary
# Register your models here.
admin.site.register(User)
admin.site.register(College)
admin.site.register(Alumini)
admin.site.register(Entry)
admin.site.register(Topic)
admin.site.register(Locations)
admin.site.register(Salary)
