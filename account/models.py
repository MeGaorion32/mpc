import os
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from projects.models import Base

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    

    def get_by_natural_key(self, email):
        return self.get(email=email)


class Account(Base, AbstractBaseUser, PermissionsMixin):

    class Role(models.TextChoices):
        ADMIN = 'admin', 'Администратор'
        OWNER = 'owner', 'Владелец'
        DIRECTOR = 'director', 'Руководитель проекта'

    def get_upload_path(instance, filename):
        # Получаем необходимые атрибуты из instance
        account_id = instance.pk  # Идентификатор экземпляра
        # Формируем путь на основе имени акции и её идентификатора
        return os.path.join('accounts', str(account_id), filename)

    email = models.EmailField(max_length=255, unique=True, verbose_name='Email')
    password = models.CharField(max_length=255, verbose_name='Пароль')
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Имя')
    surname = models.CharField(max_length=255, blank=True, null=True, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=255, blank=True, null=True, verbose_name='Отчество')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Номер телефона')
    avatar = models.FileField(upload_to='account/', blank=True, null=True, verbose_name='Аватар')  

     # Поле для роли
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.DIRECTOR, verbose_name='Роль')

    is_active = models.BooleanField(default=True, verbose_name='Активный')
    is_superuser = models.BooleanField(default=False, verbose_name='Админ')
    is_staff = models.BooleanField(default=False, verbose_name='Сотрудник')
    token = models.CharField(max_length=255, blank=True, null=True, verbose_name='Токен') 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Другие обязательные поля, если требуется

    objects = CustomUserManager()  # Подключите ваш кастомный менеджер

   
    def __str__(self):
        return self.email        


    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


