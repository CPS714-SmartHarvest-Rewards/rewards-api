# loyalty/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('offers/', views.list_offers, name='list_offers'),
    path('create-reward/', views.create_reward, name='create_reward'),
    path('total-points/', views.total_points_earned, name='total_points_earned'),
    path('bonus-points/', views.add_bonus_points, name='add_bonus_points'),  # Add bonus points for events
    path('admin/add-reward/', views.admin_add_reward, name='admin_add_reward'),  # Admin endpoint to add reward
]
