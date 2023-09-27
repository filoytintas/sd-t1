import grpc
import json
import time
import numpy as np
import cache_service_pb2
import cache_service_pb2_grpc
from find_car_by_id import find_car_by_id

class CacheClient:
    def __init__(self, host="master", port=50051):
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = cache_service_pb2_grpc.CacheServiceStub(self.channel)

    def get(self, key, simulated=False):
        start_time = time.time()  # Inicio del temporizador

        response = self.stub.Get(cache_service_pb2.Key(key=key))
        
        if response.value:
            elapsed_time = time.time() - start_time  # Calcula el tiempo transcurrido
            print(f"Time taken (cache): {elapsed_time:.5f} seconds")
            return response.value
        else:
            # Simulamos un retraso aletorio de 1 a 3 segundos, con una distribución normal en 2
            delay = np.random.normal(2, 0.5)
            print(f"Key not found in cache. Waiting {delay:.5f} seconds...")

            if not simulated:
                time.sleep(delay)

            # Si no está en el caché, buscar en el JSON
            value = find_car_by_id(int(key))
            value = str(value)
            if value:
                print("Key found in JSON. Adding to cache...")
                
                # Agregando la llave-valor al caché
                self.stub.Put(cache_service_pb2.CacheItem(key=key, value=value))
                
                elapsed_time = time.time() - start_time  # Calcula el tiempo transcurrido
                if simulated:
                    # add delay to time just sum
                    elapsed_time += delay
                print(f"Time taken (JSON + delay): {elapsed_time:.5f} seconds")
                
                return value
            else:
                elapsed_time = time.time() - start_time  # Calcula el tiempo transcurrido
                print(f"Time taken: {elapsed_time:.5f} seconds")
                print("Key not found.")
                return None
            
    def simulate_searches(self, n_searches=100):
        keys_to_search = [f"{i}" for i in np.random.randint(1, 101, n_searches)]
        total = 0

        # Métricas
        time_without_cache = 0
        time_with_cache = 0
        avoided_json_lookups = 0

        count = 0
        for key in keys_to_search:
            # clear console
            count += 1
            print("\033[H\033[J")
            print(f"Searching : {count}/{n_searches}")
            start_time = time.time()
            time_without_cache += 3 + 0.001  # Estimado de tiempo de búsqueda en JSON
            self.get(key)
            elapsed_time = time.time() - start_time
            time_with_cache += elapsed_time

            if elapsed_time < 1:
                avoided_json_lookups += 1

        time_saved = time_without_cache - time_with_cache
        time_total = time_without_cache + time_with_cache
        print(f"\t t3iempo total: {time_total:.2f} seconds")
        print(f"\nTime saved thanks to cache: {time_saved:.2f} seconds")
        print(f"Number of times JSON lookup was avoided: {avoided_json_lookups}")
    
    def simulate_distribucion_normal(self, n_simulations=100):
        media = 50
        desviacion_estandar = 10
        ids_aleatorios = [int(np.random.normal(media, desviacion_estandar)) for _ in range(n_simulations)]

        # Métricas
        time_without_cache = 0
        time_with_cache = 0
        avoided_json_lookups = 0

        count = 0
        for id_aleatorio in ids_aleatorios:
            # Limpiar la consola
            count += 1
            print("\033[H\033[J")
            print(f"Simulating Random ID : {count}/{n_simulations}")
            start_time = time.time()
            time_without_cache += 3 + 0.001  # Estimado de tiempo de búsqueda en JSON
            self.get(str(id_aleatorio))  
            elapsed_time = time.time() - start_time
            time_with_cache += elapsed_time

            if elapsed_time < 1:
                avoided_json_lookups += 1

        time_saved = time_without_cache - time_with_cache
        time_total = time_without_cache + time_with_cache
        print(f"\tTotal time: {time_total:.2f} seconds")
        print(f"\nTime saved thanks to cache: {time_saved:.2f} seconds")
        print(f"Number of times JSON lookup was avoided: {avoided_json_lookups}")

        

if __name__ == '__main__':
    client = CacheClient()

    while True:
        print("\nChoose an operation:")
        print("1. Get")
        print("2. Simulate Searches")
        print("3. Simulate Normal Distribution")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            key = input("Enter key: ")
            value = client.get(key)
            if value is not None:
                print(f"Value: {value}")
        elif choice == "2":
            n_searches = int(input("Enter the number of searches you want to simulate: "))
            client.simulate_searches(n_searches)
        elif choice == "3":
            n_simulations = int(input("Enter the number of simulations for normal distribution: "))
            client.simulate_distribucion_normal(n_simulations)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")