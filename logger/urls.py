from django.urls import path
from logger import views

urlpatterns = [
    path("", views.home, name="logger_home")
]
