from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Planner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now, blank=False, null=False, unique=True)
    before_lunch = models.TextField(help_text="Plans for before lunch", null=False, blank=False)
    after_lunch = models.TextField(help_text="Plans for after lunch", null=False, blank=False)

    def __str__(self):
        return f"{self.user} - {self.date}"
    
class Retrospect(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now, blank=False, null=False, unique=True)
    before_lunch = models.TextField(help_text="What did you do before lunch?", null=False, blank=False)
    after_lunch = models.TextField(help_text="What did you do after lunch?", null=False, blank=False)
    plans_before_lunch = models.BooleanField(default=False)
    plans_after_lunch = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.date}"