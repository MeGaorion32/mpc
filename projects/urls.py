from django.urls import path

from . import views

urlpatterns = [    
    # Админ
    # path("admin/create", views.create_project, name="project_create"),
    

    path("admin/<int:id>/", views.admin_project_detail, name="admin_project_detail"),

    path("create/", views.create_project, name="project_create"),
    path("update/<int:id>", views.update_project, name="project_update"),
    path("project/update/status/<int:id>", views.update_project_status, name="project_update_status"),
    path("project/delete/<int:id>", views.delete_project, name="project_delete"),
    path("projectFile/delete/<int:id>", views.delete_project_file, name="project_file_delete"),
   
    # path('upload/', views.upload_files, name='upload_files'),

   

    # Пользователь    
    
]