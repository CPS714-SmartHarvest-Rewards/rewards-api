from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .supabase_client import supabase
import json

# List all offers
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

# Calculate total points earned for a user
def total_points_earned(request):
    # Assuming user_id is provided as a query parameter
    user_id = request.GET.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'User ID is required'}, status=400)

    # Query all entries for the specified user and sum points_earned
    response = supabase.table('rewards').select('points_earned').eq('user_id', user_id).execute()
    if response.status_code != 200:
        return JsonResponse({'error': response.error_message}, status=response.status_code)

    # Calculate total points with a check for missing 'points_earned' fields
    total_points = sum(entry.get('points_earned', 0) for entry in response.data)

    return JsonResponse({'user_id': user_id, 'total_points_earned': total_points})
