from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, UserPhoto


class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(label='Дата рождения', widget=forms.DateInput(attrs={'type': 'date'}))
    phone_number = forms.CharField(label='Номер телефона')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'birth_date',
                  'phone_number']
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'username': 'Имя пользователя',
                  'email': 'Электронная почта', 'password1': 'Придумайте пароль', 'password2': 'Повторите пароль'}


class UserPhotoForm(forms.ModelForm):
    image = forms.ImageField(label='Добавить фото(можно несколько)',
                             widget=forms.ClearableFileInput(attrs={'id': 'id_image', 'multiple': True}),
                             required=False)

    class Meta:
        model = UserPhoto
        exclude = ['uploaded_at', 'user']
