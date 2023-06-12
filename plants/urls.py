from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('scan/', views.plant_scan, name='scan'),
    path('save/', views.plant_save, name='plant_save'),
    path('contribution/', views.contribution_system, name='contribution'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('treemap/', views.tree_map, name='tree_map'),
    path('library/', views.plant_library, name='plant_library'),
]
