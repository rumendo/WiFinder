from django.urls import path
from . import views

urlpatterns = [
    path('map/', views.data_map, name='data_map'),
    path('location/', views.location, name='location'),
    path('networks/', views.networks, name='networks'),
    path('deauth_network/', views.deauth_network, name='deauth_network'),
    path('data/', views.data, name='data'),
    path('', views.home, name='home'),
]