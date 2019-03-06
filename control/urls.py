from django.urls import path
from . import views

urlpatterns = [
    path('map/', views.data_map, name='data_map'),
    path('networks/', views.networks, name='networks'),
    path('clients/', views.clients, name='clients'),
    path('data/', views.data, name='data'),
    path('', views.home, name='home'),
]