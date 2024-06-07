from django.urls import path
from work_logger import views

urlpatterns = [
    path("", views.home, name="work_logger_home"),
    path("planners/list", views.list_planners, name="work_logger_list_planners"),
    path("retrospects/list", views.list_retrospects, name="work_logger_list_retrospects"),
]