from django.db import models
from django.conf import settings

class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Project(Base):
    name = models.CharField(max_length=200, verbose_name='Называние проекта')
    file = models.FileField(upload_to='', verbose_name='Файл проекта')

    def __str__(self):
        return self.name
    
    def full_file_path(self):
        return settings.BASE_URL + self.file.url
    


    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'