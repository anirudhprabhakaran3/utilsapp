from django.urls import path
from logger import views

urlpatterns = [
    path("", views.home, name="logger_home"),
    path("create", views.create_work_item, name="logger_create_work_item")
]
