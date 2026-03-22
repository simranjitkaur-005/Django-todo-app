from django.contrib import admin
from todoapp.models import Person
from todoapp.models import Task
# Register your models here.

admin.site.register(Person),
admin.site.register(Task)