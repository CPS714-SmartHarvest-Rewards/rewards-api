from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .supabase_client import supabase
import json

# Default view for the /loyalty/ path
def loyalty_home(request):
    return HttpResponse(
        "<h1>Welcome to the Loyalty Program</h1>"
        "<p>Available endpoints:</p>"
        "<ul>"
        "<li><a href='/loyalty/offers/'>/loyalty/offers/</a> - List all available rewards</li>"
        "<li>/loyalty/create-reward/ - Create a new reward (POST)</li>"
        "<li>/loyalty/total-points/ - Get total points and redemption history</li>"
        "<li>/loyalty/bonus-points/ - Add bonus points (POST) [REMOVED]</li>"
        "<li>/loyalty/admin/add-reward/ - Admin: Add a new reward (POST) [REMOVED]</li>"
        "</ul>"
    )

# List all available rewards (rewards catalog) with pagination
def list_offers(request):
    try:
        response = supabase.table('Offer').select('*').execute()
        # Check for errors in the response
        # if response.error:  #<--- .error doesn't exist as an attr ❌
        #     return JsonResponse({'error': response.error['message']}, status=400)
        return JsonResponse(response.data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Create a new reward
@csrf_exempt
def create_reward(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            #required_fields = ["reward_name", "points"]  # <----- FIX: REMOVE reward_name doesn't  even exist
            required_fields = ["points", "user_id"]
            for field in required_fields:
                if field not in data:
                    return JsonResponse({'error': f'Missing required field: {field}'}, status=500)

            reward_data = {               
                "points": int(data.get("points")),
                "reward_description": data.get("reward_description", ""),               
                "is_active": True,
                "user_id": int(data.get("user_id"))
            }
            response = supabase.table('04_rewards').insert(reward_data).execute()
            return JsonResponse(response.data, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)

# Total points earned and redemption history for user profile
def total_points_earned(request):
    user_id = request.GET.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'User ID is required'}, status=400)

    # Fetch points earned by the user
    points_response = supabase.table('04_rewards').select('points').eq('user_id', user_id).execute()
    
    # if points_response.status_code != 200: #<--- ".status_code" probably doesn't exist as an attr
    #     return JsonResponse({'error': points_response.error_message}, status=points_response.status_code)

    # Calculate total points
    total_points = sum(entry.get('points', 0) for entry in points_response.data)

    # Fetch redemption history for the user
    redemption_response = supabase.table('Redemptions').select('*').eq('user_id', user_id).execute()
    # if redemption_response.status_code != 200:  #<--- samething here, ".status_code" probably doesn't exist as an attr
    #     return JsonResponse({'error': redemption_response.error_message}, status=redemption_response.status_code)

    return JsonResponse({
        'user_id': user_id,
        'total_points_earned': total_points,
        'redemption_history': redemption_response.data
    })

# Add bonus points for specific events   #<----- FIX OR REMOVE: bonus_points TABLE DOES NOT EXIST
# @csrf_exempt
# def add_bonus_points(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             user_id = data.get("user_id")
#             event_id = data.get("event_id")
#             bonus_points = data.get("bonus_points", 0)

#             if not user_id or not event_id:
#                 return JsonResponse({'error': 'User ID and Event ID are required'}, status=400)

#             # Check if the user has already received points for this event
#             existing_bonus = supabase.table('bonus_points').select('*').eq('user_id', user_id).eq('event_id', event_id).execute()
#             if existing_bonus.data:
#                 return JsonResponse({'error': 'Bonus points already awarded for this event'}, status=400)

#             # Award bonus points
#             response = supabase.table('bonus_points').insert({
#                 "user_id": user_id,
#                 "event_id": event_id,
#                 "points": bonus_points
#             }).execute()

#             return JsonResponse(response.data, safe=False) if response.status_code == 201 else JsonResponse({'error': response.error_message}, status=response.status_code)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON data'}, status=400)

# Admin endpoint to add a new reward     #<----- FIX OR REMOVE: there's no point for this. it's the same as create_reward
# @csrf_exempt
# def admin_add_reward(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             reward_data = {
#                 "reward_name": data.get("reward_name"),
#                 "reward_description": data.get("reward_description"),
#                 "points": int(data.get("points", 0)),
#                 "is_active": True
#             }
#             response = supabase.table('04_rewards').insert(reward_data).execute()
#             return JsonResponse(response.data, safe=False) if response.status_code == 201 else JsonResponse({'error': response.error_message}, status=response.status_code)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON data'}, status=400)
