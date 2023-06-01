from . import views
from .views import register
from django.urls import re_path, path

urlpatterns = [
    path('register/', views.register, name='user_register'),
    path('login/', views.login_view, name='user_login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<slug:username>/', views.profile_view, name='user_profile'),
    path('pass_refresh/', views.change_password, name='pass_refresh'),
    path('update_profile', views.update_profile, name='profile_update')
]
