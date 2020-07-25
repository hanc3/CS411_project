from django.urls import path

from . import views

app_name = 'appUser'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]