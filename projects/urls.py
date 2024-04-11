from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('project/<str:pk>/', views.project, name='project'),
    path('add-project/', views.add_project, name='add_project'),
    path('edit-project/<str:pk>/', views.edit_project, name='edit_project'),
    path('delete-project/<str:pk>/', views.delete_project, name='delete_project'),
]
