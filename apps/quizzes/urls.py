from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_quiz, name='create_quiz'),
]