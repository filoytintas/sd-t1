import json
import time
import random

def cargar_datos(archivo):
    with open(archivo, 'r') as f:
        datos = json.load(f)
    return datos

def buscar_por_id(datos, id_busqueda):
    for elemento in datos:
        if elemento.get('id') == id_busqueda:
            return elemento
    return None

archivo_json = 'cars.json'
datos = cargar_datos(archivo_json)
num_busquedas = int(input("Ingresa la cantidad de búsquedas aleatorias que deseas realizar: "))
tiempo_total = 0
i= 0

for _ in range(num_busquedas):
    id_a_buscar = random.choice([elemento['id'] for elemento in datos])
    inicio = time.time()
    resultado = buscar_por_id(datos, id_a_buscar)
    fin = time.time()
    tiempo_transcurrido = (fin - inicio)*1000 + random.randint(0, 3000)

    if resultado:
        i += 1
        print(f"Búsqueda nº{i}")
        print(f"Elemento encontrado para el ID {id_a_buscar}:\n{resultado}")
    else:
        print(f"No se encontró ningún elemento con el ID {id_a_buscar}")

    print(f"Tiempo transcurrido para la búsqueda del ID {id_a_buscar}: {tiempo_transcurrido} ms")
    print("="*50)
    tiempo_total+=tiempo_transcurrido

print(f"Tiempo total transcurrido: {tiempo_total} ms")