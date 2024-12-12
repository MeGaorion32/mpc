from django.urls import path

from . import views

urlpatterns = [    
    # Админ
    # path("admin/create", views.create_project, name="project_create"),
    path("admin/create/", views.create_project_page, name="project_create_page"),
    path("admin/update/<int:id>", views.update_project_page, name="project_update_page"),
    path("admin/projects/all", views.admin_all_projects_page, name="admin_all_projects_page"),
    path("admin/users/all", views.admin_all_users_page, name="admin_all_users_page"),

    path("user/all", views.user_all_projects_page, name="user_all_projects_page"),    
    path("user/<int:id>/", views.user_project_detail, name="user_project_detail_page"),
    path("photo_video/<int:id>/", views.project_photo_video_page, name="project_photo_video_page"),
    path("other_files/<str:type>/<int:id>/", views.other_files_page, name="project_other_files_page"),

    path("admin/<int:id>/", views.admin_project_detail, name="admin_project_detail"),

    path("create/", views.create_project, name="project_create"),
    path("update/<int:id>", views.update_project, name="project_update"),
     path("admin/project/delete/<int:id>", views.delete_project, name="admin_project_delete"),
    path("admin/projectFile/delete/<int:id>", views.delete_project_file, name="admin_project_file_delete"),
   
    # path('upload/', views.upload_files, name='upload_files'),

   

    # Пользователь    
    
]