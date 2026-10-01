"""
Supabase client — singleton para toda la app
"""
import os
from dotenv import load_dotenv

load_dotenv()

_client = None


def get_supabase():
    """Retorna el cliente Supabase (singleton)."""
    global _client
    if _client is None:
        from supabase import create_client
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        if not url or not key:
            raise RuntimeError("SUPABASE_URL y SUPABASE_KEY deben estar en .env")
        _client = create_client(url, key)
    return _client


def supabase_ok() -> bool:
    """Health check: verifica que la conexión funciona."""
    try:
        get_supabase()
        return True
    except Exception:
        return False
