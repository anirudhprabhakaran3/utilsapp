from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomUser
from logger.models import WorkItemPreferences


@receiver(post_save, sender=CustomUser)
def create_work_item_preferences(sender, instance, created, **kwargs):
    if created:
        WorkItemPreferences.objects.create(user=instance)
