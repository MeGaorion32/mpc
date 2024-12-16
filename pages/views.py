from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from projects.models import Project, ProjectFile
from account.models import Account
from projects.forms import ProjectForm, MyFileForm
import json
import os


def index(request):
    return HttpResponse("Hello, world. You're at the mpc start page.")

def create_project_page(request):
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        print('form', form)
        if form.is_valid():
            project = form.save(commit=False)
            print('project1', project)
            project.save()
            print('project2', project)
            return redirect("admin_project_detail", id=project.id)
    else:
        form = ProjectForm()
    users = Account.objects.filter(is_superuser=False)
    updatePage = False
    return render(request, "projects/admin/create.html", {"users": users, "updatePage": updatePage})


def update_project_page(request, id):
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        print('form', form)
        if form.is_valid():
            project = form.save(commit=False)
            print('project1', project)
            project.save()
            print('project2', project)
            return redirect("admin_project_detail", id=project.id)
    else:
        form = ProjectForm()
    users = Account.objects.filter(is_superuser=False)
    project = Project.objects.get(id=id)
    projectFiles = ProjectFile.objects.filter(file_project=project)
    print('projectFiles', projectFiles.__dict__)
    # projectFiles_list = list(projectFiles.values('file_project', 'path', 'type', 'full_file_path()', 'id'))
    projectFiles_list = [
    {
        'id': pf.id,
        'file_project': pf.file_project.id,
        'path': pf.path.url,  # Или используйте full_file_path() для получения строки URL
        'type': pf.type,
        'full_file_path': pf.full_file_path()  # Здесь вы вызываете метод
    } 
    for pf in projectFiles
    ]
    projectFiles_list = json.dumps(projectFiles_list)
    updatePage = True
    return render(request, "projects/admin/create.html", {
        "users": users, 
        "project": project, 
        "updatePage": updatePage, 
        "projectFiles": projectFiles_list
        })


def admin_all_projects_page(request):
    projects = Project.objects.filter(completed=False).order_by("-created_at")
    completed_projects = Project.objects.filter(completed=True).order_by("-created_at")
    context = {
        "projects": projects,
        "completed_projects": completed_projects,
        }
    return render(request, "projects/admin/list.html", context)


def admin_all_users_page(request):
    users = Account.objects.all().order_by("-created_at")
    roles = [{'name': '', 'label': 'Выбрать роль'},
                 {'name': 'admin', 'label': 'Администратор'},
                 {'name': 'owner', 'label': 'Владелец'},
                 {'name': 'director', 'label': 'Руководитель проекта'},
                ]
    context = {
        "users": users,
        "roles": roles,
        }
    return render(request, "account/all_users.html", context)

def user_all_projects_page(request):
    current_user = request.user
    if current_user.role == 'owner':
        projects = Project.objects.filter(completed=False).order_by("-created_at")
        completed_projects = Project.objects.filter(completed=True).order_by("-created_at")

    if current_user.role == 'director':
        projects = Project.objects.filter(completed=False, user=current_user.id).order_by("-created_at")
        completed_projects = Project.objects.filter(completed=True, user=current_user.id).order_by("-created_at")
    context = {
        "projects": projects,
        "completed_projects": completed_projects,
        }
    return render(request, "projects/user/list.html", context)

def user_project_detail_page(request, id):
    project = get_object_or_404(Project, id=id)
    project_photos = ProjectFile.objects.filter(file_project = project.id, type = 'photo').order_by("created_at")
    is_image = project.file.name.endswith(('.jpg', '.jpeg', '.png'))
    is_pdf = project.file.name.endswith('.pdf')
    return render(request, "projects/user/detail.html", {
        "project": project, 
        "project_photos": project_photos, 
        'is_image': is_image, 
        'is_pdf': is_pdf,
        })


def project_photo_video_page(request, id):
    project = get_object_or_404(Project, id=id)
    project_photos = ProjectFile.objects.filter(file_project = project.id, type = 'photo').order_by("created_at")
    project_videos = ProjectFile.objects.filter(file_project = project.id, type = 'video').order_by("created_at")
    
    return render(request, "projects/user/photo_video.html", {
        "project": project, 
        "project_photos": project_photos, 
        "project_videos": project_videos, 
        })


def other_files_page(request, type, id):
    print('type', type)
    project = get_object_or_404(Project, id=id)
    project_files = ProjectFile.objects.filter(file_project = project.id, type = type).order_by("created_at")
    type_label = ProjectFile.FileType(type).label if type in dict(ProjectFile.FileType.choices) else None

    for file in project_files:
        file.file_name = os.path.basename(file.full_file_path())

    
    return render(request, "projects/user/other_files.html", {
        "project": project, 
        "project_files": project_files, 
        "type_label": type_label        
        })

def photo_video_detail_page(request):
    if request.method == "POST":
        id = request.POST.get('id')
        type = request.POST.get('type')
        back_url = request.POST.get('url')
        print('back_url', back_url)
        print('id', id)
        print('type', type)
        project_file = get_object_or_404(ProjectFile, id=id)
        project = get_object_or_404(Project, id=project_file.file_project.id)
        project_files = ProjectFile.objects.filter(file_project=project.id, type=type).order_by("created_at")
        type_label = project_file.get_type_display()
        print('type_label', type_label)

        for file in project_files:
            file.file_name = os.path.basename(file.full_file_path())
    
    return render(request, "projects/user/photo_detail.html", {
        "project": project, 
        'project_file': project_file,
        "project_files": project_files, 
        "type_label": type_label,     
        'back_url': back_url,   
        'file_type': type
        })

    # return render(request, "projects/user/photo_detail.html")
