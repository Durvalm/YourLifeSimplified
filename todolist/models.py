from django.db import models

# Create your models here.


class ToDoList(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=10000, blank=True)
    end_date = models.DateTimeField(auto_now=False, blank=True)
    end_hour = models.TimeField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
