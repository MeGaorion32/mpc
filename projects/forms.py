from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['name', 'file']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control custom-name-class', 'placeholder': 'Введите называнию'}),
            'file': forms.ClearableFileInput(attrs={
                'class': 'form-control-file', 
                'accept': 'application/pdf,image/jpeg,image/png'
                }),                
        }

        labels = {
            'name': 'Полное название проекта',
            'file': 'Файл проекта',
        }

    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Проверяем расширение
            if not (file.name.endswith('.pdf') or file.name.endswith('.jpg') or file.name.endswith('.jpeg') or file.name.endswith('.png')):
                raise forms.ValidationError("Разрешены только файлы PDF, JPG, JPEG и PNG.")
        return file