import random
import requests
import pickle
import os

CACHE_FILE = 'cache.pickle'
NUMBER_OF_POKEMONES = 151
POKEMON_API_URL = 'https://pokeapi.co/api/v2/pokemon/'

POKEMON_CACHE = {}

def load_cache():
    global POKEMON_CACHE
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'rb') as f:
            POKEMON_CACHE = pickle.load(f)

def save_cache():
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump(POKEMON_CACHE, f)

def random_pokemon_name():
    load_cache()
    
    pokemon_id = random.randint(1, NUMBER_OF_POKEMONES)
    
    if pokemon_id in POKEMON_CACHE:
        return POKEMON_CACHE[pokemon_id]
    
    try:
        response = requests.get(POKEMON_API_URL + pokemon_id)
        response.raise_for_status()
        pokemon_data = response.json()
        pokemon_name = pokemon_data['name']
        
        POKEMON_CACHE[pokemon_id] = pokemon_name
        save_cache()
        
        return pokemon_name
    except requests.RequestException as e:
        return None
