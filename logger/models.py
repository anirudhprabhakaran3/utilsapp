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


class WorkItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, blank=False, null=False, default="IP")

    created_at = models.DateField(editable=False, blank=False, null=False)
    updated_at = models.DateField(blank=True, null=True)
    completed_at = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now().date()
        self.modified_at = timezone.now().date()
        return super(WorkItem, self).save(*args, **kwargs)
