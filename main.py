import pokebase as pb
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import requests
import numpy as np
import matplotlib.pyplot as plt

root = None
def menu():
    while True:
        print("Menú de opciones:")
        print("1. Buscar pokémon por numero de pokedex:")
        print("2. Opción 2")
        print("3. Opción 3")
        print("4. Salir")
        option = str(input("Selecciona una opción: "))

        if option == "1":
            foundPokemonByPokedexNumber()
        elif option == "2":
            print("Opción 2 seleccionada")
        elif option == "3":
            print("Opción 3 seleccionada")
        elif option == "4":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida")
        
        
        
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
        
def foundPokemonByPokedexNumber():
    pokedex_number = int(input("Introduce el número de pokedex: "))
    
    showGraphicStats(pokedex_number)

    
def showGraphicStats(pokedex_number):
    pokemon_stats_json = requestPokemonGeneraDataJsonToApi(pokedex_number)
    pokemon_customized_json = requestPokemonCustomizedDataJsonToApi(pokedex_number)
    
    if pokemon_stats_json is None or pokemon_customized_json is None:
        print("No se pudo obtener la información del Pokémon.")
        return
    
    pokemon_name = pokemon_stats_json["name"]
    
    list_stats = pokemon_stats_json["stats"]
    stats_values = [stat["base_stat"] for stat in list_stats]
    stats_names = [stat["stat"]["name"] for stat in list_stats]
    stats_values += stats_values[:1]
    color = pokemon_customized_json["color"]["name"]
    
    angulos = np.linspace(0, 2 * np.pi, len(stats_names), endpoint=False).tolist()
    
    angulos += angulos[:1]
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    ax.plot(angulos, stats_values, color=color, linewidth=2)
    ax.fill(angulos, stats_values, color=color, alpha=0.3)
    
    ax.set_thetagrids(np.degrees(angulos[:-1]), stats_names)
    ax.set_title(f"Estadísticas de {pokemon_name}", size=15, pad=20)
    ax.grid(True)
    
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()
    
    plt.show()
    

        
if __name__ == "__main__":
    menu()  
