from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.start_add, name='start_add'),
    path('count/', views.start_count, name='start_count'),
    path('tasks/<str:task_id>/', views.task_status, name='task_status'),
    path('decks/', views.decks, name='decks'),
]


