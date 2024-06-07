from django.urls import path
from work_logger import views

urlpatterns = [
    path("", views.home, name="work_logger_home")
]