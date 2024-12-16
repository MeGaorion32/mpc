from django.urls import path

from . import views
from account import views as account_views

urlpatterns = [
    path("", account_views.login_view, name="index"),

    path("welcome", views.index, name="index"),

    path("administrator/create/", views.create_project_page, name="project_create_page"),
    path("administrator/update/<int:id>", views.update_project_page, name="project_update_page"),
    path("administrator/projects/all", views.admin_all_projects_page, name="admin_all_projects_page"),
    path("administrator/users/all", views.admin_all_users_page, name="admin_all_users_page"),

    path("user/all", views.user_all_projects_page, name="user_all_projects_page"),    
    path("user/<int:id>/", views.user_project_detail_page, name="user_project_detail_page"),
    path("photo_video/<int:id>/", views.project_photo_video_page, name="project_photo_video_page"),
    path("other_files/<str:type>/<int:id>/", views.other_files_page, name="project_other_files_page"),
    path("file/detail/", views.photo_video_detail_page, name="project_detail_file_page"),
]