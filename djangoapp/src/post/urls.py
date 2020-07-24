from django.urls import path

from . import views

app_name = 'post'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:Post_id>/', views.detail, name='detail'),
    path('insertion/', views.Insertrecord, name='insert'),
]