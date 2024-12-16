import os
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.shortcuts import get_object_or_404, redirect


def save_object(id, instance_object, path):
    
    # Получаем имя файла и путь
    original_path = instance_object.name
    object_id = id        

    # Новое имя файла
    new_path = os.path.join(path, str(object_id), os.path.basename(original_path))

    # Сохраняем файл в новом месте
    if not default_storage.exists(new_path):
        # Перемещаем файл, если необходимо
        content = instance_object.read()
        default_storage.save(new_path, ContentFile(content))

        # Удаляем старый файл, если он существует
        if default_storage.exists(original_path):
            default_storage.delete(original_path)

            # Удаляем пустую директорию, если она существует
            original_dir = os.path.dirname(original_path)
            if not default_storage.listdir(original_dir)[1]:  # Check if directory is empty
                print('original_dir', original_dir)
                print('default_storage', default_storage)
                print('new_path', new_path)
                print('default_storage.listdir(original_dir)[1]', default_storage.listdir(original_dir)[1])

                original_dir_contents = default_storage.listdir(original_dir)
                files = original_dir_contents[1]  # Файлы
                dirs = original_dir_contents[0]  # Папки                

                # Удаляем только если в директории больше нет файлов или папок
                if not files and not dirs:
                    default_storage.delete(original_dir)
                # default_storage.delete(original_dir)

    # Обновляем поле poster так, чтобы оно указывало на новый путь
    instance_object.name = new_path
    
