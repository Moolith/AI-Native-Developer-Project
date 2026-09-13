from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('join/', views.join, name='join'),
    path('chores/new/', views.create_chore, name='create_chore'),
]