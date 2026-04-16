import os
from pathlib import Path
import requests
from dotenv import load_dotenv

env_path = Path(__file__).parent / ".hidden" / ".env"
load_dotenv(dotenv_path=env_path)

IGDB_CLIENT_ID = os.getenv('IGDB_CLIENT_ID')
IGDB_BEARER_TOKEN = os.getenv('IGDB_TOKEN')

def get_igdb_headers():
    """ Haalt de benodigde headers op voor het maken van een API request naar IGDB. Deze bevatten de Client-ID en de Authorization token.

    Returns:
        dict: Een dictionary met de benodigde headers voor IGDB API requests
    """
    return {
        'Client-ID': IGDB_CLIENT_ID,
        'Authorization': f'Bearer {IGDB_BEARER_TOKEN}'
    }

def search_game(query):
    """ Zoekt naar games op basis van een zoekterm.

    Args:
        query (str): De zoekterm voor het zoeken naar games

    Returns:
        list: Een lijst met game-gegevens die overeenkomen met de zoekterm
    """
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
    """ Haalt de details van een enkele game op basis van zijn IGDB ID.

    Args:
        game_id (int): Het IGDB ID van de game wiens details opgehaald moeten worden

    Returns:
        dict: Een dictionary met de details van de game
    """
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
    """ Haalt de cover URL op en formatteert deze zodat we een grotere versie van de cover kunnen tonen. Als er geen cover is, geeft het een placeholder afbeelding terug.

    Args:
        raw_url (str): De onbewerkte cover URL

    Returns:
        str: De geformatteerde cover URL
    """
    
    if not raw_url:
        return "https://via.placeholder.com/264x352?text=No+Cover"
    return "https:" + raw_url.replace('t_thumb', 't_cover_big')