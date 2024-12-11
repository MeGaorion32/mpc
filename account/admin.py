from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):

    model = Account
    list_display = ( 'id', 'email', 'name', 'surname', 'patronymic', 'password', 'avatar', 
                    'is_active', 'is_superuser', 'token', 'created_at', 'updated_at')
    list_filter = ('is_active', 'is_staff',)
    ordering = ('email',)
    fieldsets = (

        (None, {'fields': ('email', 'name', 'surname', 'patronymic', 'avatar', 'is_active', 'is_superuser', 'token')}),
    )
    search_fields = ('email',) 

admin.site.register(Account, CustomUserAdmin)
