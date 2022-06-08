from django.contrib.auth.models import User
from django.db import models
# Create your models here.


class ToDoList(models.Model):
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=10000, blank=True)
    end_date = models.DateTimeField(auto_now=False, blank=True)
    is_completed = models.BooleanField(default=False)
    is_late = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title
