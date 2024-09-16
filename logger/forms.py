from django.forms import ModelForm
from logger.models import WorkItem, WorkItemPreferences


class CreateWorkItemForm(ModelForm):
    class Meta:
        model = WorkItem
        fields = ("subject", "description", "status",)


class WorkItemPreferencesForm(ModelForm):
    class Meta:
        model = WorkItemPreferences
        fields = ("time_amount", "time_unit",)
