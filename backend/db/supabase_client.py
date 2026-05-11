import os
from supabase import create_client, Client
from dotenv import load_dotenv
import httpx

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# 禁用 SSL 验证（仅用于测试）
httpx.Client(verify=False)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)