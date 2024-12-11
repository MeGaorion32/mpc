from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm, UserLoginForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('register')  # Замените на ваше название URL входа
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})



def login_view(request):
     # Проверяем, аутентифицирован ли пользователь

    if request.user.is_authenticated:
        # Если пользователь уже авторизован, перенаправляем его на нужную страницу
        if request.user.is_superuser:
            return redirect('admin_all_projects')  # Замените на ваше целевое представление для админов
        return redirect('user_all_projects')  # Замените на ваше целевое представление для обычных пользователей
    print(request.POST)

    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        print('user', user.is_superuser)
        if user.is_superuser:
            return redirect('admin_all_projects')  
        return redirect('user_all_projects') 
    print("Form errors:", form.errors)
    return render(request, 'account/login.html', {'form': form})

