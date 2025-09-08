import os
from supabase import create_client, Client

from app.core.config import Settings


class Database:
    def __init__(self):
        self.url: str = Settings.SUPABASE_URL
        self.key: str = Settings.SUPABASE_KEY
        self.client: Client = create_client(self.url, self.key)

    def get_client(self) -> Client:
        return self.client


db = Database()
