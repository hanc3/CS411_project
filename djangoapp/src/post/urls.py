from django.urls import path

from . import views

app_name = 'post'
urlpatterns = [
    # path to index page which lists post
    path('', views.index, name='index'),

    # path of detail of different post e.g. post/2
    path('<int:Post_id>/', views.detail, name='detail'),

    # path of insert a new post
    path('insertion/', views.Insertrecord, name='insert'),

    # path('search/', views.Search, name='search'),
]