from django.urls import path

from . import views

urlpatterns = [    
    # Админ
    # path("admin/create", views.create_project, name="project_create"),
    path("admin/create/", views.create_project_page, name="project_create_page"),
    path("create/", views.create_project, name="project_create"),

    path("admin/update/<int:id>", views.update_project_page, name="project_update_page"),
    path("update/<int:id>", views.update_project, name="project_update"),
    path("admin/all", views.admin_all_projects, name="admin_all_projects"),
    path("admin/<int:id>/", views.admin_project_detail, name="admin_project_detail"),
    # path('upload/', views.upload_files, name='upload_files'),

    path("admin/project/delete/<int:id>", views.delete_project, name="admin_project_delete"),
    path("admin/projectFile/delete/<int:id>", views.delete_project_file, name="admin_project_file_delete"),

    # Пользователь    
    path("user/all", views.user_all_projects, name="user_all_projects"),
    path("user/<int:id>/", views.user_project_detail, name="user_project_detail"),
]