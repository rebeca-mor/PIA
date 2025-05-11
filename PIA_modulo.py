import requests
import json


def getPokemonByPokedexNumber(pokedex_number):
    pokemon = None
    pokemon = getPokemonFromFile(pokedex_number)
    if pokemon is None:
        pokemon = getPokemonFromAPI(pokedex_number)
    return pokemon

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


def getPokemonFromAPI(pokedex_number):
    pokemonData = requestPokemonGeneraDataJsonToApi(pokedex_number)
    color = requestPokemonCustomizedDataJsonToApi(pokedex_number)['color']['name']
    
    listStats = pokemonData['stats']
    stats_values = [stat['base_stat'] for stat in listStats]
    stats_names = [stat['stat']['name'] for stat in listStats]
    stats = dict(zip(stats_names, stats_values))
    pokemon = {
        "id": pokemonData['id'],
        "Nombre": pokemonData['name'],
        "Tipo": " y ".join([t['type']['name'] for t in pokemonData['types']]),
        "Movimientos": [m['move']['name'] for m in pokemonData['moves'][:5]],
        "Base Experience:": pokemonData['base_experience'],
        "Estadisticas" : stats,
        "Altura": pokemonData['height'],
        "Peso": pokemonData['weight'],
        "Color": color,
    }
    
    updateFilePokemonList(pokemon)
    return pokemon
    
def getPokemonFromFile(pokedex_number):
    try:
        with open("pokemon_list.json", "r") as file:
            pokemonList = json.load(file)
            if isinstance(pokemonList, dict): 
                if str(pokemonList.get("id")) == str(pokedex_number):
                    return pokemonList
                return None
            for pokemon in pokemonList:
                if str(pokemon.get("id")) == str(pokedex_number):
                    return pokemon
    except FileNotFoundError:
        print("Buscando en la api...")
    except json.JSONDecodeError:
        print("Error al decodificar el JSON.")
    return None

def updateFilePokemonList(newPokemonInfo):
    try:
        try:
            with open("pokemon_list.json", "r") as file:
                pokemonList = json.load(file)
                if not isinstance(pokemonList, list):  # Si por error es un dict
                    pokemonList = [pokemonList]
        except (FileNotFoundError, json.JSONDecodeError):
            pokemonList = []

        # Evitar duplicados por ID
        if not any(p['id'] == newPokemonInfo['id'] for p in pokemonList):
            pokemonList.append(newPokemonInfo)

        with open("pokemon_list.json", "w") as file:
            json.dump(pokemonList, file, indent=4)

    except Exception as e:
        print(f"Error al guardar el archivo: {e}")