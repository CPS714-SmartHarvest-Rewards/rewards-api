from django.urls import path
from . import views

urlpatterns = [
    path('', views.loyalty_home, name='loyalty_home'),  # Default route for /loyalty/
    path('offers/', views.list_offers, name='list_offers'),
    path('rewards/', views.list_rewards, name='list_rewards'),  # New endpoint to list rewards
    path('create-reward/', views.create_reward, name='create_reward'),
    path('create-offer/', views.create_offer, name='create_offer'),
    path('total-points/', views.total_points_earned, name='total_points_earned'),    
    path('redeem/', views.create_redemption, name='create_redemption'),  # New endpoint to create redemption
]
