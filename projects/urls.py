from django.urls import path

from . import views

urlpatterns = [    
    # Админ
    path("admin/create", views.create_project, name="project_create"),
    path("admin/update/<int:id>", views.update_project, name="project_update"),
    path("admin/all", views.admin_all_projects, name="admin_all_projects"),
    path("admin/<int:id>/", views.admin_project_detail, name="admin_project_detail"),

    # Пользователь    
    path("user/all", views.user_all_projects, name="user_all_projects"),
    path("user/<int:id>/", views.user_project_detail, name="user_project_detail"),
]