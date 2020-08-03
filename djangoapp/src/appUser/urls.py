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
    path('post/', views.post, name='post'),
    path('post/editPost/<int:Post_id>/', views.editPost, name="editPost"),
    path('post/delete/<int:Post_id>/', views.delete, name="delete"),
    path('editApartment/', views.editApartment, name='editApartment'),
]


