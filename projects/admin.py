from django.contrib import admin
from .models import Project, ProjectFile
from django.contrib.admin import ModelAdmin

class CustomProject(ModelAdmin):

    model = Project
    list_display = ('id', 'user', 'name', 'info', 'file', 'completed')
    list_filter = ('id', 'user', 'name', 'info', 'file', 'completed')
    ordering = ('name',)
    fieldsets = (

        (None, {'fields': ('user', 'name', 'info', 'file', 'completed')}),
    )
    search_fields = ('name',) 


class CustomProjectFile(ModelAdmin):

    model = ProjectFile
    list_display = ('id', 'file_project', 'path', 'type')
    list_filter = ('id', 'file_project', 'path', 'type')
    ordering = ('file_project',)
    fieldsets = (

        (None, {'fields': ('file_project', 'path', 'type')}),
    )
    search_fields = ('file_project',) 

admin.site.register(Project, CustomProject)
admin.site.register(ProjectFile, CustomProjectFile)

