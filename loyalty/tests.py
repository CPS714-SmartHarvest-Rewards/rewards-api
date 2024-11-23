from django.test import TestCase
from loyalty.models import Offer, Reward, Redemption, Earning


# Create your tests here.
class OfferTest(TestCase):
    def setUp(self):
        Offer.objects.create(offer_name="Test Offer", offer_description="This is a test offer", awardable_points=100, expiry_date=None, is_active=True)
    
    def testOffer(self):
        offer = Offer.objects.get(offer_name="Test Offer")
        self.assertEqual(offer.offer_name, "Test Offer")
        self.assertEqual(offer.offer_description, "This is a test offer")
        self.assertEqual(offer.awardable_points, 100)
        self.assertEqual(offer.expiry_date, None)
        self.assertEqual(offer.is_active, True)


class RewardTest(TestCase):
    def setUp(self):
        Reward.objects.create(reward_name="Test Reward", reward_description="This is a test reward", points=100, is_active=True)
    
    def testReward(self):
        reward = Reward.objects.get(reward_name="Test Reward")
        self.assertEqual(reward.reward_name, "Test Reward")
        self.assertEqual(reward.reward_description, "This is a test reward")
        self.assertEqual(reward.points, 100)
        self.assertEqual(reward.is_active, True)

class RedemptionTest(TestCase):
    def setUp(self):
        Reward.objects.create(reward_name="Test Reward", reward_description="This is a test reward", points=100, is_active=True)
        Offer.objects.create(offer_name="Test Offer", offer_description="This is a test offer", awardable_points=100, expiry_date=None, is_active=True)
        Earning.objects.create(user_id=1, earning_type=0, offer=Offer.objects.get(offer_name="Test Offer"), points_earned=100)
    
    def testRedemption(self):
        response = self.client.post('/loyalty/redeem/', {"user_id": "1", "reward_id": str(Reward.objects.get(reward_name="Test Reward").id)})  
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Redemption.objects.count(), 1)
        