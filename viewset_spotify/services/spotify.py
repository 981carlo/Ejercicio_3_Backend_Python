import base64
import requests
from django.conf import settings


# Guardamos el token en caché 
_SPOTIFY_TOKEN = None


# Solicitamos un token de acceso usando client_credentials
def _request_token():
    auth = f'{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}'
    auth_base64 = base64.b64encode(auth.encode()).decode()
    
    response = requests.post(
        'https://accounts.spotify.com/api/token',
        headers = {
            'Authorization': f'Basic {auth_base64}',
            'Content-type': 'application/x-www-form-urlencoded'
        },
        data = {'grant_type': 'client_credentials'},
        timeout=10,
        
    )
    
    response.raise_for_status()
    return response.json()['access_token']
    

#   - Realiza peticiones GET a la API de Spotify
#   - Gestiona token de acceso y renovación automática
def spotify_get(endpoint, params=None):
    global _SPOTIFY_TOKEN
    
    # Pedimos un token si no lo tenemos
    if not _SPOTIFY_TOKEN:
        _SPOTIFY_TOKEN = _request_token()
        
    response = requests.get(
        f'https://api.spotify.com/v1/{endpoint}',
        headers={'Authorization': f'Bearer {_SPOTIFY_TOKEN}'},
        params=params,
        timeout=10
    )
    
    # Pedimos un token nuevo si el actual ha caducado (lazy refresh)
    if response.status_code == 401:
        _SPOTIFY_TOKEN = _request_token()
        response = requests.get(
            f'https://api.spotify.com/v1/{endpoint}',
            headers={'Authorization': f'Bearer {_SPOTIFY_TOKEN}'},
            params=params,
            timeout=10
        )
    response.raise_for_status()
    return response.json()


# Funciones de búsqueda en Spotify

def buscar_artista(artista: str):
    
    data = spotify_get('search', params={'q': artista, 'type': 'artist', 'limit': 1})
    items = data.get('artists', {}).get('items', [])
    if not items:
        return None
    
    return items[0]['name'] # Devuelve el nombre del primer artista encontrado


def buscar_album(album: str):
    
    data = spotify_get('search', params={'q': album, 'type': 'album', 'limit': 1})
    items =data.get('albums', {}).get('items', [])
    if not items:
        return None
        
    album = items[0]['name'] # Devuelve el nombre del primer album encontrado
    artistname = items[0]['artists'][0]['name'] # Devuelve el nombre del artista del album
    
    return album, artistname

    
def buscar_cancion(cancion: str):
    
    data = spotify_get('search', params={'q': cancion, 'type': 'track', 'limit': 1})
    items = data.get('tracks', {}).get('items', [])
    if not items:
        return None
    
    cancion = items[0]['name'] #  Devuelve el nombre de la primera canción encontrada
    artistname = items[0]['artists'][0]['name'] # Devuelve el nombre del artista de la canción
    
    return cancion, artistname