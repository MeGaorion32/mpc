from django.shortcuts import get_object_or_404, render, redirect
from .models import Project, ProjectFile
from account.models import Account
from .forms import ProjectForm, MyFileForm
import json
import os


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


def update_project(request, id):
    project = get_object_or_404(Project, id=id)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        print('form', form)
        if form.is_valid():
            project = form.save(commit=False)
            print('project1', project)
            project.save()
            print('project2', project)
            return redirect("admin_project_detail", id=project.id)
    else:
        form = ProjectForm(instance=project)
    
    return render(request, "projects/admin/update.html", {"form": form, "project": project})


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

def admin_project_detail(request, id):
    project = get_object_or_404(Project, id=id)
    is_image = project.file.name.endswith(('.jpg', '.jpeg', '.png'))
    is_pdf = project.file.name.endswith('.pdf')
    return render(request, "projects/admin/detail.html", {"project": project, 'is_image': is_image, 'is_pdf': is_pdf,})

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

def user_project_detail(request, id):
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
    type_label = project_files.first().get_type_display()
    print('type_label', type_label)

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




# def create_project_test(request):
#     if request.method == "POST":
#         form = ProjectWithFilesForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Сохраняем проект
#             project = form.save()

#             # Сохраняем дополнительные файлы
#             files = request.FILES.getlist('files')  # Получаем список загруженных файлов
#             for f in files:
#                 ProjectFile.objects.create(file_project=project, path=f)  # Создаем объект ProjectFile с каждым файлом

#             return redirect("admin_project_detail", id=project.id)  # Перенаправление на детальный просмотр проекта

#     else:
#         form = ProjectWithFilesForm()

#     return render(request, "projects/admin/create.html", {"form": form})



def create_project(request):    
    if request.method == 'POST':
        print('request post', request.POST)
        print('request file', request.FILES)        
        completed = False
        if request.POST.get('completed', False) == 'on':
            completed = True

        user = Account.objects.get(id=request.POST.get('user'))
        data = {
            'name': request.POST.get('name'),
            'info': request.POST.get('info'),
            'user': user,
            'completed': completed,
            'file': request.FILES.get('file'),
        }    
        print('data', data)    
        updatePage = False

        if request.POST.get('updatePage') == 'true':
            project = Project.objects.get(id=request.POST.get('projectId'))
            data = {k: v for k, v in data.items() if v is not None}
            updatePage = True

            # Обновляем проект
            for attr, value in data.items():
                setattr(project, attr, value)

            # Сохраняем изменения
            project.save()

        else:
            # Создаем новый проект
            project = Project.objects.create(**data)

        users = Account.objects.filter(is_superuser=False)     

        fields = [
            {'name': 'photo', 'field': ProjectFile.FileType.PHOTO},
            {'name': 'video', 'field': ProjectFile.FileType.VIDEO},
            {'name': 'graphics', 'field': ProjectFile.FileType.GRAPHICS},
            {'name': 'summaries', 'field': ProjectFile.FileType.SUMMARIES},
            {'name': 'techpark', 'field': ProjectFile.FileType.TECHPARK},
            {'name': 'personal', 'field': ProjectFile.FileType.PERSONAL},
            {'name': 'equipment', 'field': ProjectFile.FileType.EQUIPMENT},
            {'name': 'laboratories', 'field': ProjectFile.FileType.LABORATORIES},
            {'name': 'ot_pb_oos', 'field': ProjectFile.FileType.OT_PB_OOS},
            {'name': 'regulations', 'field': ProjectFile.FileType.REGULATIONS},
            {'name': 'reserv', 'field': ProjectFile.FileType.RESERV},

        ]

        photo_file = None

        for field in fields:
            # Получаем список загруженных фото
            files = request.FILES.getlist(field['name'])           
            print(field['name'], files)
            for f in files:
                ProjectFile.objects.create(path=f, file_project=project, type=field['field'])  # Указываем тип

        # project.save()
        print('project', project)    

        print('photo_file', photo_file)     

        projectFiles = ProjectFile.objects.filter(file_project=project)
        print('projectFiles', projectFiles.__dict__)
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
        # projectFiles_list = list(projectFiles.values('file_project', 'path', 'type', 'full_file_path()', 'id'))
        projectFiles_list = json.dumps(projectFiles_list)
        return render(request, "projects/admin/create.html", {
            "users": users, 
            "project": project, 
            "updatePage": updatePage, 
            "projectFiles": projectFiles_list
            })
        # return render(request, 'projects/admin/create.html', {'users': users})
    else:
        form = MyFileForm()
    
    return render(request, 'upload.html', {'users': users})

def delete_project(request, id):
        
        if request.method == 'DELETE':

            project = get_object_or_404(Project, id=id)
            project.delete()

            projects = Project.objects.filter(completed=False).order_by("-created_at")
            completed_projects = Project.objects.filter(completed=True).order_by("-created_at")
            context = {
                "projects": projects,
                "completed_projects": completed_projects,
                }
            return render(request, "projects/user/list.html", context)
        

def delete_project_file(request, id):
        
        if request.method == 'DELETE':

            projectFile = get_object_or_404(ProjectFile, id=id)
            projectFile.delete()
            project = Project.objects.get(id=projectFile.file_project.id)

            users = Account.objects.filter(is_superuser=False) 
            projectFiles = ProjectFile.objects.filter(file_project=project)
            print('projectFiles', projectFiles.__dict__)
            projectFiles_list = [
            {
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

