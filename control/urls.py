from django.urls import path

from . import views

urlpatterns = [
    path('start_hcx/', views.start_hcx, name='start_hcx'),
    path('', views.index, name='index'),
]