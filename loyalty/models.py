from django.db import models

class Offer(models.Model):
    offer_name = models.CharField(max_length=255)
    offer_description = models.TextField()
    user_id = models.IntegerField()
    awardable_points = models.IntegerField()
    expiry_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.offer_name

class Reward(models.Model):
    reward_name = models.CharField(max_length=255)
    reward_description = models.TextField()
    points = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.reward_name

class Redemption(models.Model):
    user_id = models.IntegerField()
    target_id = models.IntegerField()  # References Offer or Reward by ID
    is_reward_redemption = models.BooleanField()
    points_redeemed = models.IntegerField()
    is_active = models.BooleanField(default=True)
    redeemed_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Redemption for User {self.user_id}'
