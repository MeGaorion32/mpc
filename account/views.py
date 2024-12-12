from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from .forms import UserRegistrationForm, UserLoginForm
from .models import Account

def register(request, user_id=None):
  
    update_user=False
    if user_id:
        user = get_object_or_404(Account, pk=user_id)
        form = UserRegistrationForm(request.POST or None, request.FILES or None, instance=user)
        update_user=True
    else:
        form = UserRegistrationForm(request.POST or None, request.FILES or None)

    # if request.method == 'POST' and form.is_valid():
    #     form.save()
    #     return redirect('register')  # Замените на ваше название URL входа

    # return render(request, 'account/register.html', {'form': form, 'project_user': user if user_id else None, 'update_user': update_user})

    if request.method == 'POST':
        if form.is_valid():
            user_instance = form.save(commit=False)  # Сохраняем данные пользователя без пароля

            # # Если пароли введены, то обновляем пароль
            # if form.cleaned_data['password1']:
            #     user_instance.set_password(form.cleaned_data['password1'])

            # Установка пароля только если он был введен
            password1 = form.cleaned_data['password1']
            if password1:
                user_instance.set_password(password1)

            user_instance.save()  # Отправляем обновленный экземпляр в базу данных
            return redirect('register')  # Замените на ваше название URL входа

    return render(request, 'account/register.html', {
        'form': form,
        'project_user': user if user_id else None,
        'update_user': update_user
    })



def login_view(request):
     # Проверяем, аутентифицирован ли пользователь

    if request.user.is_authenticated:
        # Если пользователь уже авторизован, перенаправляем его на нужную страницу
        if request.user.is_superuser:
            return redirect('admin_all_projects_page')  # Замените на ваше целевое представление для админов
        return redirect('user_all_projects')  # Замените на ваше целевое представление для обычных пользователей
    print(request.POST)

    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        print('user', user.is_superuser)
        if user.is_superuser:
            return redirect('admin_all_projects_page')  
        return redirect('user_all_projects') 
    print("Form errors:", form.errors)
    return render(request, 'account/login.html', {'form': form})


def update_user(request, user_id):

    if request.method == 'POST':

        user = Account.objects.get(id=user_id)
        data = {
            'name': request.POST.get('name'),
            'surname': request.POST.get('surname'),
            'patronymic': request.POST.get('patronymic'), 
            'email': request.POST.get('email'),  
            'role': request.POST.get('role'),           
            'file': request.FILES.get('avatar'),
        }    
        print('data', data)                   
        
        data = {k: v for k, v in data.items() if v is not None}        

        # Обновляем проект
        for attr, value in data.items():
            setattr(user, attr, value)

        if request.POST.get('password'):
            user.set_password(request.POST.get('password'))

        # Сохраняем изменения
        user.save()
      
        return render(request, 'account/user_edit.html', {
            'project_user': user            
        }) 
    
    else:
        user = get_object_or_404(Account, id=user_id)
        roles = [{'name': '', 'label': 'Выбрать роль'},
                 {'name': 'admin', 'label': 'Администратор'},
                 {'name': 'owner', 'label': 'Владелец'},
                 {'name': 'director', 'label': 'Руководитель проекта'},
                ]

        return render(request, 'account/user_edit.html', {
            'project_user': user,
            'user_roles': roles,            
        })



def delete_user_avatar(request, id):
        
    if request.method == 'DELETE':

        user = get_object_or_404(Account, id=id)
        user.avatar = None
        user.save()

        form = UserRegistrationForm(request.POST or None, request.FILES or None, instance=user)
        update_user = True
        
        return render(request, "account/register.html", {
            "form": form,
            "project_user": user, 
            "update_user": update_user, 
            })



