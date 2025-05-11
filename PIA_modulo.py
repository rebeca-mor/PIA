import requests
import json
import os

# Devuelve una lista de enteros, cada valor entero es el promedio de las estadisticas de cada pokemon.
# Util para calcular la moda, mediana y varianza de los pokemones.
def getPromedyOfStatsList(listPokemons):
    stats_values = []
    for pokemon in listPokemons:
        stats_values.append(getPromedyOfStats(pokemon))
    return stats_values

#Devuelve el promedio entero de las estadisticas de un pokemon.
def getPromedyOfStats(pokemon):
    stats = pokemon['Estadisticas']
    stats_values = list(stats.values())
    return media(stats_values)

#Devuelve la moda de poder promedio de una lista de pokemones.
def getModeOfPokemonAverageStats(listPokemons):
    average_stats_values = getPromedyOfStatsList(listPokemons)
    return moda(average_stats_values)

#Devuelve la mediana de poder promedio de una lista de pokemones
def getMeanOfCollectionOfPokemons(listPokemons):
    stats_values = getPromedyOfStatsList(listPokemons)
    return mediana(stats_values)

#Devuelve la varianza de poder promedio de una lista de pokemones
def getVarianceOfCollectionOfPokemons(listPokemons):
    stats_values = getPromedyOfStatsList(listPokemons)
    return varianza(stats_values)

#Devuelve la desviacion estandar de poder promedio de una lista de pokemones
def getStandardDeviationOfCollectionOfPokemons(listPokemons):
    stats_values = getPromedyOfStatsList(listPokemons)
    return desviacion_estandar(stats_values)

#Calcula la media de una lista de numeros.
def media(list):
    return sum(list) / len(list)

#Calcula la mediana de una lista de numeros.
def mediana(lista):
	lista_ordenada = sorted(lista)
	n = len(lista_ordenada)
	if n % 2 == 1: 
		return lista_ordenada[n//2]
	else: 
		return (lista_ordenada[n//2 - 1] + lista_ordenada[n//2]) / 2

#Calcula la moda de una lista de numeros.
def moda(list):
    max_repeticiones = 0
    moda = None
    
    for i in range(len(list)):
        repeticiones = 0
        for j in range(len(list)):
            if list[i] == list[j]:
                repeticiones += 1
        
        if repeticiones > max_repeticiones:
            max_repeticiones = repeticiones
            moda = list[i]
    
    return moda

#Calcula la varianza de una lista de numeros.
def varianza(lista):
    varianza = 0
    media = sum(lista) / len(lista)
    suma_cuadrados = 0
    for valor in lista:
        suma_cuadrados += (valor - media) ** 2
    varianza = suma_cuadrados / (len(lista) -1)
    return varianza

#Calcula la desviacion estandar de una lista de numeros.
def desviacion_estandar(lista):
	return varianza(lista) ** 0.5

def foundPokemonByPokedexNumber():
    pokedex_number = str(input("Introduce el número de pokedex: "))
    return getPokemonByPokedexNumber(pokedex_number)

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

def getCollectionOfPokemons():
    try:
        with open("pokemon_list.json", "r") as file:
            pokemonList = json.load(file)
            if isinstance(pokemonList, dict): 
                return [pokemonList]
            return pokemonList
    except FileNotFoundError:
        print("Archivo no encontrado.")
        return None
    except json.JSONDecodeError:
        print("Error al decodificar el JSON.")
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
                if not isinstance(pokemonList, list):  
                    pokemonList = [pokemonList]
        except (FileNotFoundError, json.JSONDecodeError):
            pokemonList = []

        if not any(p['id'] == newPokemonInfo['id'] for p in pokemonList):
            pokemonList.append(newPokemonInfo)

        with open("pokemon_list.json", "w") as file:
            print(f"Agregando al pokemon {newPokemonInfo['Nombre']} a la lista")
            json.dump(pokemonList, file, indent=4)

    except Exception as e:
        print(f"Error al guardar el archivo: {e}")
        
def deletePokemonList():
    os.remove("pokemon_list.json")
    print("Archivo pokemon_list.json eliminado.")
    
    