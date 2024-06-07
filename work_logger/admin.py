from django.contrib import admin
from work_logger import models

# Register your models here.
admin.site.register(models.Planner)
admin.site.register(models.Retrospect)