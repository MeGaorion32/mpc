from django.shortcuts import get_object_or_404, render, redirect
from .models import Project
from .forms import ProjectForm


def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        print('form', form)
        if form.is_valid():
            project = form.save(commit=False)
            print('project1', project)
            project.save()
            print('project2', project)
            return redirect("project_detail", id=project.id)
    else:
        form = ProjectForm()
    return render(request, "projects/create.html", {"form": form})

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
            return redirect("project_detail", id=project.id)
    else:
        form = ProjectForm(instance=project)
    
    return render(request, "projects/update.html", {"form": form, "project": project})


def all_projects(request):
    projects = Project.objects.order_by("-created_at")
    context = {"projects": projects}
    return render(request, "projects/list.html", context)

def project_detail(request, id):
    project = get_object_or_404(Project, id=id)
    is_image = project.file.name.endswith(('.jpg', '.jpeg', '.png'))
    is_pdf = project.file.name.endswith('.pdf')
    return render(request, "projects/detail.html", {"project": project, 'is_image': is_image, 'is_pdf': is_pdf,})
