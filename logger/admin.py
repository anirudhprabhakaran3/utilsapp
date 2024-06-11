from django.contrib import admin
from logger import models

# Register your models here.
admin.site.register(models.Log)
admin.site.register(models.Task)
