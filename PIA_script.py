import pokebase as pb
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import PIA_modulo as repository
import requests
import numpy as np
import matplotlib.pyplot as plt

root = None
def menu():
    while True:
        print("\nMenú de opciones:")
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
            
def foundPokemonByPokedexNumber():
    pokedex_number = str(input("Introduce el número de pokedex: "))
    showGraphicStats(pokedex_number)

    
def showGraphicStats(pokedex_number):
    pokemon = repository.getPokemonByPokedexNumber(pokedex_number)
    
    if pokemon is None:
        print("Pokémon no encontrado.")
        return
    
    stats = pokemon['Estadisticas']
    statsName = list(stats.keys())
    statsValues = list(stats.values())
    statsValues += statsValues[:1]

    angulos = np.linspace(0, 2 * np.pi, len(statsName), endpoint=False).tolist()
    
    angulos += angulos[:1]
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    ax.plot(angulos, statsValues, color=pokemon['Color'], linewidth=2)
    ax.fill(angulos, statsValues, color=pokemon['Color'], alpha=0.3)
    
    ax.set_thetagrids(np.degrees(angulos[:-1]), statsName)
    ax.set_title(f"Estadísticas de {pokemon['Nombre']}", size=15, pad=20)
    ax.grid(True)
    
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()
    
    plt.show()
    

        
if __name__ == "__main__":
    menu()  
