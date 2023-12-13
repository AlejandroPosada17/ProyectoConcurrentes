from google_images_search import GoogleImagesSearch
import threading
import os

# Configuración
API_KEY = 'AIzaSyCYHMA8aRyxidEBnb_2-IiIddcx8Eom5LI'
CX = '65b4c74322300402a'
TOTAL_IMAGES = 20
THREAD_COUNT = 10

# Semáforo para controlar la concurrencia
semaphore = threading.Semaphore()

def download_images(thread_id, results):
    count_per_thread = len(results) // THREAD_COUNT
    start_index = thread_id * count_per_thread
    end_index = start_index + count_per_thread

    gis = GoogleImagesSearch(API_KEY, CX)

    for image in results[start_index:end_index]:
        try:
            # Adquirir el semáforo antes de descargar
            semaphore.acquire()

            print(f"Thread-{thread_id}: Descargando {image.url}")
            image.download(f'./Imagenes/')
        except OSError as error:
            print(f"Thread-{thread_id}: Error descargando {image}: {error}")
        finally:
            # Liberar el semáforo después de la descarga
            semaphore.release()

def Guardado_Imagenes(tema_Busqueda):
    gis = GoogleImagesSearch(API_KEY, CX)

    search_params = {
        'q': tema_Busqueda,
        'num': TOTAL_IMAGES,
        "type": "photo"
    }

    gis.search(search_params)
    results = list(gis.results())

    # Crear directorios para descargas
    for i in range(THREAD_COUNT):
        path = f'./Imagenes/'
        os.makedirs(path, exist_ok=True)

    threads = []

    for i in range(THREAD_COUNT):
        thread = threading.Thread(target=download_images, args=(i, results))
        threads.append(thread)

    # Iniciar los hilos
    for thread in threads:
        thread.start()

    # Esperar a que todos los hilos terminen
    for thread in threads:
        thread.join()

    print('Descarga finalizada')
