from .supabase_client import supabase
from datetime import datetime

def save_essay(user_id, title, essay_text, score, strengths, model_used, type, rubric):
    data = {
        "user_id": user_id,
        "title": title,
        "essay_text": essay_text,
        "score": score,
        "strengths": strengths,
        "model_used": model_used,
        "created_at": datetime.utcnow().isoformat(),
        "rubric" : rubric,
        "essay_type": type
    }

    essay_response = supabase.table("essays").insert(data).execute()

     # Step 2: Upsert the title into essay_titles table
    title_data = {
        "title": title.strip(),
        "type": type,
        "rubric" : rubric
    }

    title_response = supabase.table("essay_titles").upsert(title_data, on_conflict=["title"]).execute()

    return {
        "essay_response": essay_response,
        "title_response": title_response,
    }

def get_essay_by_id(essay_id):
    res = supabase.table("essays").select("*").eq("id", essay_id).single().execute()
    return res.data

def get_essay_by_title(title):
    res = supabase.table("essays").select("*").eq("title", title).execute()
    return res.data
