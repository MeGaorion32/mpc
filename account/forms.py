from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Account

class UserRegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        # Добавим опцию "Выбрать роль" в начало списка
        self.fields['role'].choices = [('', 'Выбрать роль')] + list(self.fields['role'].choices)

         # Установим значение по умолчанию для поля role
        self.fields['role'].initial = ''
   
    password1 = forms.CharField(
        label='Пароль пользователя', 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control register-field', 
            'placeholder': 'Пароль'
        })

    )
    password2 = forms.CharField(
        label='Пароль пользователя', 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control register-field', 
            'placeholder': 'Подтверждение пароля'
        })

    )
    class Meta:
        model = Account
        fields = ('email', 'phone', 'role', 'password1', 'password2', 'name', 'surname', 'patronymic', 'avatar')

        widgets = {
                'email': forms.TextInput(attrs={'class': 'form-control register-field', 'placeholder': 'Введите email'}),
                'phone': forms.TextInput(attrs={'class': 'form-control register-field', 'placeholder': 'Введите телефон'}), 
                'name': forms.TextInput(attrs={'class': 'form-control register-field', 'placeholder': 'Имя'}), 
                'avatar': forms.FileInput(attrs={'class': 'register-avatar register-field', 'id': 'register-avatar',}), 
                'role': forms.Select(attrs={'class': 'form-select register-field', 'placeholder': 'Выбрать роль'}), 
                'surname': forms.TextInput(attrs={'class': 'form-control register-field', 'placeholder': 'Фамилия'}), 
                'patronymic': forms.TextInput(attrs={'class': 'form-control register-field', 'placeholder': 'Отчество'}),  
                # 'password1': forms.TextInput(attrs={'class': 'form-control register-field', 'placeholder': 'Пароль'}), 
                # 'password2': forms.TextInput(attrs={'class': 'form-control register-field', 'placeholder': 'Подтверждение пароля'}),                             
            }

        labels = {            
            'email': 'Email пользователя',
            'phone': 'Телефон пользователя',           

        }




class UserLoginForm(forms.Form):
    email = forms.CharField(max_length=150,                                
                            widget=forms.TextInput(attrs={'class': 'form-control custom-name-class', 'placeholder': 'Email'}))
    password = forms.CharField(         
        widget=forms.PasswordInput(attrs={
            'class': 'form-control custom-name-class', 
            'placeholder': 'Пароль'
        })

    )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')        

        if email is None or password is None:
            raise forms.ValidationError("Email и пароль не могут быть пустыми.")       

        try:
            user = Account.objects.get(email=email)
            if not user.check_password(password):
                raise forms.ValidationError("Пароль неверен.")
        except Account.DoesNotExist:
            raise forms.ValidationError("Пользователь с данным email не найден.")        

        self.user_cache = user
        return self.cleaned_data


    def get_user(self):
        return self.user_cache


    # class Meta:
    #     model = Account  # Добавленный атрибут необходим для создания экземляра
    #     fields = ('username', 'password')
       
    #     widgets = {
    #             'username': forms.TextInput(attrs={'class': 'form-control custom-name-class', 'placeholder': 'Введите логина'}),
    #             'password': forms.PasswordInput(attrs={'class': 'form-control custom-name-class', 'placeholder': 'Введите пароля'}),                
    #         }

    #     labels = {
    #         'username': 'Логин пользователя',
    #         'password': 'Пароль пользователя',
    #     }

# class UserLoginForm(AuthenticationForm):

#     class Meta:
#         model = Account
#         fields = ('username', 'password')
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control custom-name-class', 'placeholder': 'Введите логин'}),
#             'password': forms.PasswordInput(attrs={'class': 'form-control custom-name-class', 'placeholder': 'Введите пароль'}),
#         }
#         labels = {
#             'username': 'Логин пользователя',
#             'password': 'Пароль пользователя',
#         }

