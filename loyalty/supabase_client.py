# loyalty/supabase_client.py
from supabase import create_client
import os

supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_API_KEY')

# Create the Supabase client
supabase = create_client(supabase_url, supabase_key)
