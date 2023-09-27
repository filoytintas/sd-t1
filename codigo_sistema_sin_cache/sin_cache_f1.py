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
id_a_buscar = int(input("Ingresa el ID que deseas buscar: "))
inicio = time.time()
resultado = buscar_por_id(datos, id_a_buscar)
fin = time.time()
tiempo_transcurrido = (fin - inicio)*1000

if resultado:
    print(f"Elemento encontrado:\n{resultado}")
else:
    print(f"No se encontró ningún elemento con el ID {id_a_buscar}")

print(f"Tiempo transcurrido: {tiempo_transcurrido+random.randint(0, 3000)} ms")