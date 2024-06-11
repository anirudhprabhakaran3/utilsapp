from django.urls import path
from logger import views

urlpatterns = [
    path("", views.home, name="logger_home"),
    path("all/", views.list_logs, name="logger_list_logs"),
    path("<int:pk>/", views.view_log, name="logger_view_log"),
    path("<int:pk>/edit", views.edit_log, name="logger_edit_log"),
    path("new/", views.new_log, name="logger_new")
]
