from django.urls import path

from . import views

urlpatterns = [
    path("list/", views.users_list_view),
    path("<int:user_id>/", views.user_detail_view),
    path("toggle-follow/", views.toggle_follow, name="toggle_follow"),
]