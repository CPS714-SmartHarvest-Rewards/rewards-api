from django.db import models
from django.contrib.auth.models import User

class Offer(models.Model):
    offer_name = models.CharField(max_length=255)
    offer_description = models.TextField()
    awardable_points = models.BigIntegerField()    
    expiry_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.offer_name

class Reward(models.Model):
    reward_name = models.CharField(max_length=255)
    reward_description = models.TextField()
    points = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.reward_name
    
class Earning(models.Model):
    EARNING_TYPE_CHOICES = [
        (0, 'Purchase'),
        (1, 'Feedback Submission'),
        (2, 'Event Attendance'),
    ]

    user_id = models.BigIntegerField()
    earning_type = models.SmallIntegerField(choices=EARNING_TYPE_CHOICES, null=True, blank=True)
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True, blank=True)
    feedback_id = models.BigIntegerField(null=True, blank=True)
    event_id = models.BigIntegerField(null=True, blank=True)
    points_earned = models.BigIntegerField()
    earned_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Earning for User {self.user_id}'


class Redemption(models.Model):
    user_id = models.BigIntegerField()
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
    points_redeemed = models.BigIntegerField()
    redeemed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Redemption for User {self.user_id}'
