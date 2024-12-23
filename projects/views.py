from django.shortcuts import get_object_or_404, render, redirect
from .models import Project, ProjectFile
from account.models import Account
from .forms import ProjectForm, MyFileForm
import json
import os


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



def admin_project_detail(request, id):
    project = get_object_or_404(Project, id=id)
    is_image = project.file.name.endswith(('.jpg', '.jpeg', '.png'))
    is_pdf = project.file.name.endswith('.pdf')
    return render(request, "projects/admin/detail.html", {"project": project, 'is_image': is_image, 'is_pdf': is_pdf,})





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
            'file': request.FILES.get('projectFile'),
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

def update_project_status(request, id):

    if request.method == 'POST':
        completed = False
        if request.POST.get('completed', False) == 'true':
            completed = True
        project = get_object_or_404(Project, id=id)
        project.completed = completed
        project.save()

        projects = Project.objects.filter(completed=False).order_by("-created_at")
        completed_projects = Project.objects.filter(completed=True).order_by("-created_at")
        context = {
            "projects": projects,
            "completed_projects": completed_projects,
            }
        return render(request, "projects/admin/list.html", context)


def delete_project(request, id):
        
        if request.method == 'POST':

            project = get_object_or_404(Project, id=id)
            project.delete()

            projects = Project.objects.filter(completed=False).order_by("-created_at")
            completed_projects = Project.objects.filter(completed=True).order_by("-created_at")
            context = {
                "projects": projects,
                "completed_projects": completed_projects,
                }
            return render(request, "projects/admin/list.html", context)
        

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

