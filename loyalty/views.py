from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .supabase_client import supabase
import json

# List all available rewards (rewards catalog)
def list_offers(request):
    response = supabase.table('offers').select('*').execute()
    if response.status_code == 200:
        return JsonResponse(response.data, safe=False)
    else:
        return JsonResponse({'error': response.error_message}, status=response.status_code)

# Create a new reward
@csrf_exempt
def create_reward(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            reward_data = {
                "reward_name": data.get("reward_name"),
                "reward_description": data.get("reward_description"),
                "points": int(data.get("points", 0)),
                "is_active": True
            }
            response = supabase.table('rewards').insert(reward_data).execute()
            
            if response.status_code == 201:
                return JsonResponse(response.data, safe=False)
            else:
                return JsonResponse({'error': response.error_message}, status=response.status_code)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

# Total points earned and redemption history for user profile
def total_points_earned(request):
    user_id = request.GET.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'User ID is required'}, status=400)

    # Fetch points earned by the user
    points_response = supabase.table('rewards').select('points_earned').eq('user_id', user_id).execute()
    if points_response.status_code != 200:
        return JsonResponse({'error': points_response.error_message}, status=points_response.status_code)

    # Calculate total points
    total_points = sum(entry.get('points_earned', 0) for entry in points_response.data)

    # Fetch redemption history for the user
    redemption_response = supabase.table('redemptions').select('*').eq('user_id', user_id).execute()
    if redemption_response.status_code != 200:
        return JsonResponse({'error': redemption_response.error_message}, status=redemption_response.status_code)

    return JsonResponse({
        'user_id': user_id,
        'total_points_earned': total_points,
        'redemption_history': redemption_response.data
    })

# Add bonus points for specific events
@csrf_exempt
def add_bonus_points(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
            event_id = data.get("event_id")
            bonus_points = data.get("bonus_points", 0)

            if not user_id or not event_id:
                return JsonResponse({'error': 'User ID and Event ID are required'}, status=400)

            # Check if the user has already received points for this event
            existing_bonus = supabase.table('bonus_points').select('*').eq('user_id', user_id).eq('event_id', event_id).execute()
            if existing_bonus.data:
                return JsonResponse({'error': 'Bonus points already awarded for this event'}, status=400)

            # Award bonus points
            response = supabase.table('bonus_points').insert({
                "user_id": user_id,
                "event_id": event_id,
                "points": bonus_points
            }).execute()

            return JsonResponse(response.data, safe=False) if response.status_code == 201 else JsonResponse({'error': response.error_message}, status=response.status_code)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

# Admin endpoint to add a new reward
@csrf_exempt
def admin_add_reward(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            reward_data = {
                "reward_name": data.get("reward_name"),
                "reward_description": data.get("reward_description"),
                "points": int(data.get("points", 0)),
                "is_active": True
            }
            response = supabase.table('rewards').insert(reward_data).execute()
            return JsonResponse(response.data, safe=False) if response.status_code == 201 else JsonResponse({'error': response.error_message}, status=response.status_code)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
