from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()
def get_supabase_client():
    supabase_url: str  = os.getenv("SUPABASE_URL")
    supabase_key: str  = os.getenv("SUPABASE_SERVICE_KEY")
    supabase: Client = create_client(supabase_url, supabase_key)
    return supabase