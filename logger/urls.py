from django.urls import path
from logger import views

urlpatterns = [
    path("", views.home, name="logger_home"),
    path("create", views.create_work_item, name="logger_create_work_item"),
    path("view/<int:item_id>", views.view_item, name="logger_view_item"),
    path("edit/<int:item_id>", views.edit_item, name="logger_edit_item"),
    path("view/status/<str:status>", views.view_all_status, name="logger_view_all_status"),
    path("update_preferences", views.update_preferences, name="logger_update_preferences"),
]
