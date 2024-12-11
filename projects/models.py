from django.db import models
from django.conf import settings


class Base(models.Model):
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Project(Base):

    user = models.ForeignKey('account.Account', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Руководитель проекта')
    name = models.CharField(max_length=200, verbose_name='Называние проекта')
    info = models.TextField(blank=True, null=True, verbose_name='Описание проекта')
    file = models.FileField(upload_to='project_uploads/', blank=True, null=True, verbose_name='Файл проекта')
    completed = models.BooleanField(default=False, verbose_name='Завершен')

    def __str__(self):
        return self.name
    
    def full_file_path(self):
        return settings.BASE_URL + self.file.url   

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class ProjectFile(Base):

    class FileType(models.TextChoices):
        GRAPHICS = 'graphics', 'Графики'
        SUMMARIES = 'summaries', 'Сводки'
        TECHPARK = 'techpark', 'Парк техники'
        PERSONAL = 'personal', 'Персонал, ВЗис'
        EQUIPMENT = 'equipment', 'Оснащение'
        LABORATORIES = 'laboratories', 'Лаборатории'
        OT_PB_OOS = 'ot_pb_oos', 'ОТ, ПБ, ООС'
        REGULATIONS = 'regulations', 'Предписания'
        RESERV = 'reserv', 'Резервная позиция'
        PHOTO = 'photo', 'Фото'
        VIDEO = 'video', 'Видео'

    file_project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Проект файла', related_name='project_files')
    path = models.FileField(upload_to='file_uploads/')
    type = models.CharField(max_length=100, choices=FileType.choices, default=FileType.PHOTO, verbose_name='Тип файла')

    # def __str__(self):
    #     return self.file_project.name
    
    def full_file_path(self):
        return settings.BASE_URL + self.path.url   

    class Meta:
        verbose_name = 'Файл проекта'
        verbose_name_plural = 'Файлы проектов'