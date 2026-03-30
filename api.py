import os
import requests
from dotenv import load_dotenv

load_dotenv()

IGDB_CLIENT_ID = os.getenv('IGDB_CLIENT_ID')
IGDB_BEARER_TOKEN = os.getenv('IGDB_TOKEN')

def get_igdb_headers():
    return {
        'Client-ID': IGDB_CLIENT_ID,
        'Authorization': f'Bearer {IGDB_BEARER_TOKEN}'
    }

def search_game(query):
    url = "https://api.igdb.com/v4/games"
    # ADDED 'id' to the fields we are requesting
    body = f'search "{query}"; fields id, name, cover.url, summary; limit 10;'
    
    try:
        response = requests.post(url, headers=get_igdb_headers(), data=body)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"API Error: {e}")
        return None

def get_game_by_id(game_id):
    """Fetches a single game's details by its IGDB ID."""
    url = "https://api.igdb.com/v4/games"
    body = f'fields id, name, cover.url, summary, first_release_date; where id = {game_id};'
    
    try:
        response = requests.post(url, headers=get_igdb_headers(), data=body)
        response.raise_for_status()
        data = response.json()
        return data[0] if data else None
    except requests.exceptions.HTTPError as e:
        print(f"API Error: {e}")
        return None
        
def format_cover_url(raw_url):
    if not raw_url:
        return "https://via.placeholder.com/264x352?text=No+Cover"
    return "https:" + raw_url.replace('t_thumb', 't_cover_big')