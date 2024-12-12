from django.urls import path
from .views import register, login_view, update_user, delete_user_avatar
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', register, name='register'),
    path('update/<int:user_id>/', update_user, name='update_user'),
    
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('delete/avatar/<int:id>/', delete_user_avatar, name='delete_user_avatar'),
]
