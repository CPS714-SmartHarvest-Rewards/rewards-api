from django.urls import path
from . import views

urlpatterns = [
    path('', views.loyalty_home, name='loyalty_home'),  # Default route for /loyalty/
    path('offers/', views.list_offers, name='list_offers'),
    path('create-reward/', views.create_reward, name='create_reward'),
    path('total-points/', views.total_points_earned, name='total_points_earned'),
    path('bonus-points/', views.add_bonus_points, name='add_bonus_points'),
    path('admin/add-reward/', views.admin_add_reward, name='admin_add_reward'),
]
