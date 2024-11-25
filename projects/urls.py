from django.urls import path

from . import views

urlpatterns = [    
    path("create", views.create_project, name="project_create"),
    path("update/<int:id>", views.update_project, name="project_update"),
    path("all", views.all_projects, name="all_projects"),
    path("<int:id>/", views.project_detail, name="project_detail"),
]