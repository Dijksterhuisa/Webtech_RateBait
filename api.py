import os
import requests
from dotenv import load_dotenv

# This looks for the .env file and loads the variables into the system environment
load_dotenv()

# Pull variables from the environment
IGDB_CLIENT_ID = os.getenv('IGDB_CLIENT_ID')
IGDB_BEARER_TOKEN = os.getenv('IGDB_TOKEN')

def get_igdb_headers():
    """Returns the headers required for every IGDB request."""
    return {
        'Client-ID': IGDB_CLIENT_ID,
        'Authorization': f'Bearer {IGDB_BEARER_TOKEN}'
    }

def search_game(query):
    url = "https://api.igdb.com/v4/games"
    
    # IGDB Query Language (APICalypse)
    # We ask for: name, the cover's image_id, and the summary
    body = f'search "{query}"; fields name, cover.url, summary; limit 10;'
    
    try:
        response = requests.post(url, headers=get_igdb_headers(), data=body)
        response.raise_for_status() # Check for 401 (Unauthorized) or 403 errors
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}")
        return None
    
def format_cover_url(raw_url):
    if not raw_url:
        return "https://via.placeholder.com/264x352?text=No+Cover"
    # Replace 't_thumb' with 't_cover_big' for better resolution
    return "https:" + raw_url.replace('t_thumb', 't_cover_big')

# Quick test (you can remove this later)
if __name__ == "__main__":
    results = search_game("Elden Ring")
    print(results)