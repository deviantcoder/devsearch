from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>/', views.profile, name='profile'),

    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('account/', views.user_account, name='account'),
    path('edit-account/', views.edit_account, name='edit_account'),
    path('add-skill/', views.add_skill, name='add_skill'),
    path('edit-skill/<str:pk>/', views.edit_skill, name='edit_skill'),
    path('delete-skill/<str:pk>/', views.delete_skill, name='delete_skill'),
    path('inbox/', views.inbox, name='inbox'),
    path('message/<str:pk>/', views.view_message, name='message'),
    path('create-message/<str:pk>/', views.create_message, name='create_message')
]
