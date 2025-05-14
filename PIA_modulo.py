import requests
import json
import os
import pandas as pd
import subprocess
import platform
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
    try :
        for valor in lista:
            suma_cuadrados += (valor - media) ** 2
        varianza = suma_cuadrados / (len(lista) -1)
    except ZeroDivisionError:
        return 0
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
        "Base Experience": pokemonData['base_experience'],
        "Estadisticas" : stats,
        "Altura": pokemonData['height'],
        "Peso": pokemonData['weight'],
        "Color": color,
    }
    
    updateFilePokemonList(pokemon)
    addPokemonToExcel(pokemon)
    return pokemon
    
def getPokemonFromFile(pokedex_number):
    try:
        with open(ruta_json, "r") as file:
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

ruta_json = "datos/pokemon_list.json"
def getCollectionOfPokemons():
    try:
        with open(ruta_json, "r") as file:
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
    
def updateFilePokemonList(newPokemonInfo):
    try:
        try:
            with open(ruta_json, "r") as file:
                pokemonList = json.load(file)
                if not isinstance(pokemonList, list):  
                    pokemonList = [pokemonList]
        except (FileNotFoundError, json.JSONDecodeError):
            pokemonList = []

        if not any(p['id'] == newPokemonInfo['id'] for p in pokemonList):
            pokemonList.append(newPokemonInfo)

        with open(ruta_json, "w") as file:
            print(f"Agregando al pokemon {newPokemonInfo['Nombre']} a la coleccion")
            json.dump(pokemonList, file, indent=4)

    except Exception as e:
        print(f"Error al guardar el archivo: {e}")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ruta_excel = os.path.join(BASE_DIR, "datos", "pokemon_list.xlsx")
def addPokemonToExcel(pokemon, ruta_excel=ruta_excel):
    try:
        # Crear archivo si no existe, con las columnas deseadas
        if not os.path.exists(ruta_excel):
            df = pd.DataFrame(columns=["id", "Nombre", "Tipo", "Movimientos", "Base Experience", "Estadisticas", "Altura", "Peso", "Color"])
            df.to_excel(ruta_excel, index=False)

        # Asegurar que 'pokemon' sea un DataFrame
        df_new = pd.DataFrame([pokemon])  # CORRECCIÓN: debes pasar [pokemon] (una lista con un dict), no el dict directo

        df_existing = pd.read_excel(ruta_excel)

        # Evitar duplicados
        if not df_existing.empty and 'id' in df_existing.columns and (df_existing['id'] == pokemon['id']).any():
            print(f"El Pokémon {pokemon['Nombre']} ya está en el archivo Excel.")
            return

        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_excel(ruta_excel, index=False)
        print(f"Pokémon {pokemon['Nombre']} agregado correctamente a {ruta_excel}.")

    except Exception as e:
        print(f"Error al manipular el archivo Excel: {e}")
        
        
def openExcelFile():
    if os.path.exists(ruta_excel):
        if platform.system() == "Windows":
            os.startfile(ruta_excel)
        elif platform.system() == "Darwin":  # macOS
            subprocess.call(["open", ruta_excel])
        else:  # Linux
            subprocess.call(["xdg-open", ruta_excel])
    else:
      print("El archivo Excel no existe.")
        
def deletePokemonList():
    if os.path.exists(ruta_excel):
        os.remove(ruta_excel)
        print("Archivo Excel eliminado correctamente.")
    if os.path.exists(ruta_json):
        os.remove(ruta_json)
        print("Archivo Json eliminado.")
    
    
def getCollectionSize() :
    if getCollectionOfPokemons() is None:
        return 0
    return len(getCollectionOfPokemons())
    
    