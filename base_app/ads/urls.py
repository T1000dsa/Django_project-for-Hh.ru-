from django.contrib import admin
from django.urls import path
from ads import views

urlpatterns = [
    path('', views.IndexHome.as_view(), name='home_page'),
    path('create_ad/', views.CreateAd.as_view(), name='create_ad'),
    path('show_ads/', views.ShowAds.as_view(), name='show_ads'),
    path('show_ads/<int:pk>/', views.ShowAd.as_view(), name='show_ad'),

    path('edit_ad/<int:pk>', views.EditAd.as_view(), name='edit_ad'),
    path('delete_ad/<int:pk>', views.DeleteAd.as_view(), name='delete_ad'),

    path('exchange/<int:pk>/', views.CreateExchange.as_view(), name='exchange'),
    path('exchange/<int:ad_sender_id>/to/<int:ad_receiver_id>/', 
         views.CreateExchange.as_view(), 
         name='create_exchange'),

]