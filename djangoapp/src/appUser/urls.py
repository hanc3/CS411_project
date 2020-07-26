from django.urls import path

from . import views
from django.contrib.auth import views as auth_views


app_name = 'appUser'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('update/', views.update, name='update'),
    path('login/',auth_views.LoginView.as_view(template_name='appUser/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='appUser/logout.html'),name='logout'),
]


