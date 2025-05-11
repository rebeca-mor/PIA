import requests
import json

listPokemonInfo = []

def requestPokemonGeneraDataJsonToApi(pokedex_number):
    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{pokedex_number}"
        data = requests.get(url).json()
        return data
    except Exception as e:
        print(f"Error: {e}")
        return None
    

def requestPokemonCustomizedDataJsonToApi(pokedex_number):
    try:
        url = f"https://pokeapi.co/api/v2/pokemon-species/{pokedex_number}"
        data = requests.get(url).json()
        return data
    except Exception as e:
        print(f"Error: {e}")
        return None

def getPokemonFakePagination(pokemon_list, page_size):       
    for pokemon_id in range(1, page_size + 1):
        pokemonData = requestPokemonGeneraDataJsonToApi(pokemon_id)
        color = requestPokemonCustomizedDataJsonToApi(pokemon_id)['color']['name']
        pokemon = {
            "id": pokemon_id,
            "Nombre": pokemonData['name'],
            "Tipo": " y ".join([t['type']['name'] for t in pokemonData['types']]),
            "Movimientos": [m['move']['name'] for m in pokemonData['moves'][:5]],
            "Base Experience:": pokemonData['base_experience'],
            "Estadisticas" : pokemonData['stats'],
            "Altura": pokemonData['height'],
            "Peso": pokemonData['weight'],
            "Color": color,
        }

        listPokemonInfo.append(pokemon)

