from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, UserPhotoForm
from .models import Profile, UserPhoto
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            birth_date = form.cleaned_data.get('birth_date')
            phone_number = form.cleaned_data.get('phone_number')
            profile = Profile(user=user, birth_date=birth_date, phone_number=phone_number)
            profile.save()
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'User/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm(request)
    return render(request, 'User/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'base/base.html')


def profile_view(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    is_own_profile = False
    if user.username == request.user.username:
        is_own_profile = True
        if request.method == 'POST':
            if 'image' in request.FILES:
                form = UserPhotoForm(request.POST, request.FILES)
                if form.is_valid():
                    images = request.FILES.getlist('image')
                    for image in images:
                        UserPhoto.objects.create(user=user, image=image)
                    return redirect('user_profile', username=username)
            else:
                form = UserPhotoForm()
        else:
            form = UserPhotoForm()
    else:
        form = None

    return render(request, 'User/personal_profile.html', {'form': form, 'user': user, 'profile': profile,
                                                          'is_own_profile': is_own_profile})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Обновление сессии после изменения пароля
            update_session_auth_hash(request, user)
            messages.success(request, 'Ваш пароль был успешно изменен!')
            return redirect('user_profile', request.user.username)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = PasswordChangeForm(user=request.user, label_suffix=': ')
    return render(request, 'User/change_password.html', {'form': form})


@login_required
def update_profile(request):
    if request.method == 'POST':
        # Получение отправленных данных
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        # Обновление данных пользователя
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.profile.phone_number = phone_number
        user.save()
        # Возвращение JSON ответа
        return JsonResponse({'success': True})

    # Возвращение ошибки, если запрос не является POST
    return JsonResponse({'success': False, 'error': 'Invalid request method'})