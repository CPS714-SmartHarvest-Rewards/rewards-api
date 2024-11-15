# loyalty/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('offers/', views.list_offers, name='list_offers'),
    path('create-reward/', views.create_reward, name='create_reward'),
    path('total-points/', views.total_points_earned, name='total_points_earned'),
]
