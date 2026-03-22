from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    number = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Task(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='tasks')
    task = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.person.email}- {self.task}"