from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Button

from logger.models import Log

class LogForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True

    class Meta:
        model = Log
        fields = ["notes"]

class TaskFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = "post"
        self.layout = Layout("completed", "task")
        self.render_required_fields = False
        self.form_tag = False
        self.template = "bootstrap5/table_inline_formset.html"
        self.disable_csrf = True
