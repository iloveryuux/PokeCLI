import os
import time
import random
import pickle
import requests
from collections import Counter
from colorama import Back, Style, init

CACHE_FILE = 'cache.pickle'
NUMBER_OF_POKEMONS = 151
POKEMON_API_URL = 'https://pokeapi.co/api/v2/pokemon/'
POKEMON_CACHE = {}

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

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

  pokemon_id = random.randint(1, NUMBER_OF_POKEMONS)

  if pokemon_id in POKEMON_CACHE:
    return POKEMON_CACHE[pokemon_id]

  try:
    response = requests.get(f'{POKEMON_API_URL}{pokemon_id}')
    response.raise_for_status()
    pokemon_data = response.json()
    pokemon_name = pokemon_data['name']
    
    POKEMON_CACHE[pokemon_id] = pokemon_name
    save_cache()
    
    return pokemon_name
  except requests.RequestException as e:
    return None

def color_bg(letter, color):
    colors = {'green': Back.GREEN, 'yellow': Back.YELLOW, 'red': Back.RED}
    return f'{colors.get(color, Back.RED)} {letter} {Style.RESET_ALL}'

def wordle_result(guess, target):
    result = []
    target_counter = Counter(target)
    guess_counter = Counter(guess)
    color_map = {
        (True, True): 'green',
        (True, False): 'yellow',
        (False, True): 'red',
        (False, False): 'red'
    }

    for guess_letter, target_letter in zip(guess, target):
        correct_guess = guess_letter == target_letter
        correct_position = target_counter[guess_letter] > 0
        
        color = color_map.get((correct_guess, correct_position), 'red')
        result.append(color_bg(guess_letter, color))
        
        if correct_guess:
            target_counter[target_letter] -= 1
        if correct_position:
            guess_counter[guess_letter] -= 1

    return ' '.join(result)

def main():
  attempts = 1
  guesses = []
  target = random_pokemon_name()
  pokemon_length = len(target)
  print('''
                                  ,' 
    _.----.        ____         ,'  _\   ___    ___     ____
_,-'       `.     |    |  /`.   \,-'    |   \  /   |   |    \  |`.
\      __    \    '-.  | /   `.  ___    |    \/    |   '-.   \ |  |
 \.    \ \   |  __  |  |/    ,','_  `.  |          | __  |    \|  |
   \    \/   /,' _`.|      ,' / / / /   |          ,' _`.|     |  |
    \     ,-'/  /   \    ,'   | \/ / ,`.|         /  /   \  |     |
     \    \ |   \_/  |   `-.  \    `'  /|  |    ||   \_/  | |\    |
      \    \ \      /       `-.`.___,-' |  |\  /| \      /  | |   |
       \    \ `.__,'|  |`-._    `|      |__| \/ |  `.__,'|  | |   |
        \_.-'       |__|    `-._ |              '-.|     '-.| |   |
                                `'                            '-._|
  ''')

  print(f'pokemon has {pokemon_length} letters')
  time.sleep(3)
  while attempts > 0:
    cls()

    for guess, result in guesses:
      print(result + '\n')
    
    guess = input(f'\nthe pokemon is ({attempts} Attempts): ').lower()

    if len(guess) != pokemon_length:
      print(f'\npokemon has {pokemon_length} letters')
      time.sleep(1)
      continue

    result = wordle_result(guess, target)
    guesses.append((guess, result))
    attempts -= 1

    if guess == target:
      cls()
      for guess, result in guesses:
        print(result)
      print(f'\ncongratulations the pokemon was {target}')
      break


    if attempts == 0:
      print(f'\nyou ran out of attempts the pokemon is: {target}')
      time.sleep(1)
      cls()
      for guess, result in guesses:
        print(result)

if __name__ == '__main__':
    main()