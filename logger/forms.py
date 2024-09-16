from django.forms import ModelForm
from logger.models import WorkItem


class CreateWorkItemForm(ModelForm):
    class Meta:
        model = WorkItem
        fields = ("subject", "description", "status",)
