import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)


def test_connection():
    try:
        response = supabase.table('tasks').select("*").limit(1).execute()
        print("Conexión exitosa a Supabase")
        return True
    except Exception as e:
        print(f"Error de conexión: {e}")
        return False