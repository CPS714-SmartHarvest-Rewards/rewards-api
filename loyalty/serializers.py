from rest_framework import serializers
from .models import Offer, Reward, Redemption

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'

class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = '__all__'

class RedemptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Redemption
        fields = '__all__'
