from django.urls import path

from . import views

app_name = 'apartment'
urlpatterns = [
    # path of detail of different apartment e.g. apartment/2
    path('<int:ApartmentID>/', views.detail, name='detail'),
]