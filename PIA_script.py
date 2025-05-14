import pokebase as pb
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PIA_modulo as repository
import numpy as np
import matplotlib.pyplot as plt

root = None
def menu():
    while True:
        print("\nMenú de opciones:")
        print("1. Añadir pokemon a la colección:")
        print("2. Ver estadisticas matematicas de la coleccion de pokemones:")
        print("3. Ver estadisticas de un pokemon por numero de pokedex (Media y grafico):")
        print("4. Abrir coleccion de pokemones en excel:")
        print("5. Eliminar colección de pokémon")
        print("6. Salir")
        option = str(input("Selecciona una opción: "))

        if option == "1":
            pokemon = repository.foundPokemonByPokedexNumber()
            if pokemon is None:
                print("Pokémon no encontrado.")
                continue
            repository.updateFilePokemonList(pokemon)
        elif option == "2":
            pokemonList = repository.getCollectionOfPokemons()
            if pokemonList is None:
                print("No hay pokémons en la colección.")
                continue
            showPokemonCollectionStats(pokemonList)
        elif option == "3":
            pokemon = repository.foundPokemonByPokedexNumber()
            if pokemon is None:
                print("Pokémon no encontrado.")
                continue
            showPokemonGraphicStats(pokemon)
        elif option == "4":
            repository.openExcelFile()
            print("Abriendo archivo de Excel...")
        elif option == "5":
            safeOption = str(input("¿Estás seguro de que quieres eliminar la colección de pokémon? (s/n): "))
            if safeOption.lower() != "s":
                print("Operación cancelada.")
                continue
            print("Eliminando colección de pokémon...")
            repository.deletePokemonList()
        elif option == "6":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida")
            
def showPokemonCollectionStats(listPokemon):
    names = []
    colors = []
    promeedyStats = repository.getPromedyOfStatsList(listPokemon)

    for pokemon in listPokemon:
        names.append(pokemon['Nombre'])
        colors.append(pokemon['Color'])

    fig, ax = plt.subplots(figsize=(8, 6))

    bars = ax.bar(names, promeedyStats, color=colors)

    mode = repository.getModeOfPokemonAverageStats(listPokemon)
    median = repository.getMeanOfCollectionOfPokemons(listPokemon)
    variance = repository.getVarianceOfCollectionOfPokemons(listPokemon)
    std_deviation = repository.getStandardDeviationOfCollectionOfPokemons(listPokemon)

    
    ax.set_title("Estadísticas de la colección de Pokémon", size=15, pad=20)
    ax.set_xlabel("Pokemones", size=12)
    ax.set_ylabel("Media de poder", size=12)

    plt.subplots_adjust(bottom=0.25) 

    fig.text(0.1, 0.10, f'Moda: {mode:.2f}', fontsize=11)
    fig.text(0.1, 0.06, f'Mediana: {median:.2f}', fontsize=11)
    fig.text(0.5, 0.10, f'Varianza: {variance:.2f}', fontsize=11)
    fig.text(0.5, 0.06, f'Desviación estándar: {std_deviation:.2f}', fontsize=11)
        
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

    plt.show()
    
def showPokemonGraphicStats(pokemon):
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
    ax.set_xlabel(f"Media de estadísticas, {repository.getPromedyOfStats(pokemon)}", size=16, color='black')
    ax.grid(True)
    
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()
    
    plt.show()
    
    

        
if __name__ == "__main__":
    menu()  
