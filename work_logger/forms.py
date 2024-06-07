from django import forms
from work_logger.models import Planner, Retrospect

class PlannerForm(forms.ModelForm):
    class Meta:
        model = Planner
        fields = ("before_lunch", "after_lunch")

class RetrospectForm(forms.ModelForm):
    class Meta:
        model = Retrospect
        fields = ("before_lunch", "plans_before_lunch", "after_lunch", "plans_after_lunch")