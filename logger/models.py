from django.db import models
from users.models import CustomUser
from django.utils import timezone

# Create your models here.
STATUS_CHOICES = (
    ("IP", "In Progress"),
    ("DO", "Done"),
    ("WD", "Won't Do"),
    ("BL", "Blocked")
)

TIME_CHOICES = [
    ("D", "Days"),
    ("W", "Weeks"),
    ("M", "Months")
]


class WorkItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, blank=False, null=False, default="IP")

    created_at = models.DateField(editable=False, blank=False, null=False)
    updated_at = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now().date()
        return super(WorkItem, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.subject}"


class WorkItemPreferences(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    time_amount = models.IntegerField(blank=False, null=False, default=1)
    time_unit = models.CharField(max_length=1, choices=TIME_CHOICES, blank=False, null=False, default="W")

    def __str__(self):
        return f"{self.user} Preferences"
