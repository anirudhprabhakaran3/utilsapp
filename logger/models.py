from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    date = models.DateField(default=timezone.now, blank=False, null=False)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.date}"
    
class Task(models.Model):
    log = models.ForeignKey(Log, on_delete=models.CASCADE, blank=False, null=False)
    task = models.CharField(max_length=200, blank=False, null=False)
    completed = models.BooleanField(default=False)