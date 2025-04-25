from django.contrib import admin
from django.urls import path
from ads import views

urlpatterns = [
    path('', views.IndexHome.as_view(), name='home_page')
]