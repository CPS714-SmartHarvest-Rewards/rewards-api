from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

# from loyalty.models import Redemption
from .supabase_client import supabase
import json

# Default view for the /loyalty/ path
def loyalty_home(request):
    return HttpResponse(
        """
        <h1>Welcome to the Loyalty Program Backend</h1>
        <p>Available endpoints:</p>
        <ul>
            <li><a href='/loyalty/offers/'>/loyalty/offers/</a> - List all available offers</li>
            <li><a href='/loyalty/rewards/'>/loyalty/rewards/</a> - List all available rewards</li>
            <li>/loyalty/total-points/?user_id=USER_ID - Get user's current points count and total redemption history</li>
            <li>/loyalty/create-offer/ - Create a new offer (POST)
                <ul>
                    <li><strong>Expected JSON Format:</strong>
                        <pre>
                            {
                                "offer_name": "Eco-Friendly Fertilizer Bundle",
                                "offer_description": "Purchase our eco-friendly fertilizer bundle and earn points",
                                "awardable_points": 50,
                                "expiry_date": "2024-03-31T23:59:59Z",  # optional
                                "is_active": true
                            }
                        </pre>
                    </li>
                </ul>
            </li>
            <li>/loyalty/create-reward/ - Create a new reward (POST)
                <ul>
                    <li><strong>Expected JSON Format:</strong>
                        <pre>
                            {
                                "reward_name": "Free Maintenance Service",
                                "reward_description": "Get a free maintenance service for your equipment",
                                "points": 200,
                                "is_active": true
                            }
                        </pre>
                    </li>
                </ul>
            </li>
            <li>/loyalty/redeem/ - Redeem a reward (POST)
                <ul>
                    <li><strong>Expected JSON Format:</strong>
                        <pre>
                            {
                                "user_id": 123,
                                "reward_id": 1
                            }
                        </pre>
                    </li>
                </ul>
            </li>
        </ul>
        """
    )

# List all available rewards (rewards catalog) with pagination
def list_offers(request):
    try:
        response = supabase.table('Offer').select('*').execute()        
        return JsonResponse(response.data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
# List all available rewards
def list_rewards(request):
    try:
        response = supabase.table("041_rewards").select('*').execute()
        return JsonResponse(response.data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Total points earned and redemption history for user profile
def total_points_earned(request):
    user_id = request.GET.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'User ID is required'}, status=400)

    try:
        # Fetch points earned by the user from 'earnings' table
        earnings_response = supabase.table('earnings').select('points_earned').eq('user_id', user_id).execute()
        total_earned_points = sum(entry.get('points_earned', 0) for entry in earnings_response.data)

        # Fetch redemption history for the user
        redemption_response = supabase.table('redemptions').select('*').eq('user_id', user_id).execute()
        total_redeemed_points = sum(entry.get('points_redeemed', 0) for entry in redemption_response.data)

        available_points = total_earned_points - total_redeemed_points

        return JsonResponse({
            'user_id': user_id,
            'total_points_earned': total_earned_points,
            'total_points_redeemed': total_redeemed_points,
            'available_points': available_points,
            'redemption_history': redemption_response.data
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

# Create a new reward
@csrf_exempt
def create_reward(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)            
            required_fields = ["reward_name", "points"]
            for field in required_fields:
                if field not in data:
                    return JsonResponse({'error': f'Missing required field: {field}'}, status=500)

            reward_data = {
                "reward_name": data.get("reward_name"),
                "reward_description": data.get("reward_description", ""),
                "points": int(data.get("points")),
                "is_active": data.get("is_active", True),
            }
            response = supabase.table('041_rewards').insert(reward_data).execute()
            return JsonResponse(response.data, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)

# Create a new offer
@csrf_exempt
def create_offer(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            required_fields = ["offer_name", "awardable_points"]
            for field in required_fields:
                if field not in data:
                    return JsonResponse({'error': f'Missing required field: {field}'}, status=400)

            offer_data = {
                "offer_name": data.get("offer_name"),
                "offer_description": data.get("offer_description", ""),
                "awardable_points": int(data.get("awardable_points")),
                "expiry_date": data.get("expiry_date"),  # Optional
                "is_active": data.get("is_active", True),
            }
            response = supabase.table('offers').insert(offer_data).execute()
            return JsonResponse(response.data, safe=False, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)

# Redeem a reward
@csrf_exempt
def create_redemption(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            required_fields = ["user_id", "reward_id"]
            for field in required_fields:
                if field not in data:
                    return JsonResponse({'error': f'Missing required field: {field}'}, status=400)

            user_id = int(data.get("user_id"))
            reward_id = int(data.get("reward_id"))
            # Fetch reward details
            reward_response = supabase.table("041_rewards").select('points').eq('reward_id', reward_id).execute()
            if not reward_response.data:
                return JsonResponse({'error': 'Invalid reward_id'}, status=400)
            reward_points = reward_response.data[0]['points']

            # Calculate user's available points
            earnings_response = supabase.table('earnings').select('points_earned').eq('user_id', user_id).execute()
            total_earned_points = sum(entry.get('points_earned', 0) for entry in earnings_response.data)
            redemptions_response = supabase.table('redemptions').select('points_redeemed').eq('user_id', user_id).execute()
            total_redeemed_points = sum(entry.get('points_redeemed', 0) for entry in redemptions_response.data)
            available_points = total_earned_points - total_redeemed_points

            # This object needs to be created for testing purposes, can be commented out in production    
            #Redemption.objects.create(user_id=user_id, reward_id=reward_id, points_redeemed=reward_points)

            if available_points < reward_points:
                return JsonResponse({'error': 'Insufficient points to redeem this reward'}, status=200)

            redemption_data = {
                "user_id": user_id,
                "reward_id": reward_id,
                "points_redeemed": reward_points,
                # "redeemed_date": 'NOW()'  # Omit if database default is set
            }

            response = supabase.table('redemptions').insert(redemption_data).execute()
            return JsonResponse(response.data, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)