from django.db import models

# Create your models here.
class Task(models.Model):
    DoesNotExist = None
    name=models.CharField(max_length=100)
    description=models.TextField()
    status=models.CharField(max_length=1000)
