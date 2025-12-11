# apps/users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # These are the REAL public pages (no login required)
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    
    # These are protected — redirect if already logged in
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
]