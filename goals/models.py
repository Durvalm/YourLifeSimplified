from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=10000, blank=True)
    end_date = models.DateTimeField(auto_now=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=100, blank=True)

    def time_left(self):
        time_left = self.end_date - timezone.now()
        days_left = time_left.days
        return days_left

    def __str__(self):
        return self.title
