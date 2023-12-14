import cv2
from multiprocessing import Pool
import numpy as np
from mpi4py import MPI
import os
import uuid


class Filtrados:
    def __init__(self, kernel,num_threads_or_processes, rutaImg):
        self.kernel = kernel
        self.num_threads_or_processes = num_threads_or_processes
        self.rutaImg = rutaImg
        
        
    def multiprocessing(self):
        # Cargar la imagen
        print(self.rutaImg)
        image_path = self.rutaImg  # Reemplaza con la ruta de tu imagen
        img = cv2.imread(image_path)

        # Verificar si la imagen se cargó correctamente
        if img is not None:
            # Dividir la imagen en secciones para el multiprocesamiento
            sections = np.array_split(img, self.num_threads_or_processes)  # Dividir secciones, puedes ajustar esto según el número de núcleos de tu CPU

            # Iniciar el pool de procesos
            with Pool(self.num_threads_or_processes) as pool:
                # Aplicar el filtro en paralelo a cada sección de la imagen
                 results = pool.map(self.apply_filter_kernel, sections)

            # Combinar los resultados en una sola imagen
            filtered_img = np.vstack(results)

            #Nombre al azar para la imagen fultada
            nombre_unico = str(uuid.uuid4()) + '.jpg'
            ruta_guardado = os.path.join('ImagenesFiltradas', nombre_unico)

            # Descarga imagen filtrada
            cv2.imwrite(ruta_guardado, filtered_img)
            
           
        
        else:
            print("No se pudo cargar la imagen. Verifica la ruta y el formato de la imagen.")
    
    def apply_filter_kernel(self, img_section):
        print(self.num_threads_or_processes)
        
        #matriz de convolución que se aplicará a la sección de la imagen
        kernel = self.kernel
        
        filtered_section = cv2.filter2D(img_section, -1, kernel)
        return filtered_section
    
    
    def filtro4Py(self):
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        size = comm.Get_size()

        # Cargar la imagen desde la web (reemplaza 'URL_de_tu_imagen.jpg' con la URL de tu imagen)
        image_url = self.rutaImg
        image = cv2.imread(image_url)

        # Dividir la imagen en partes iguales entre los procesos
        rows_per_process = image.shape[0] // size
        start_row = rank * rows_per_process
        end_row = (rank + 1) * rows_per_process if rank != size - 1 else image.shape[0]

        # Seleccionar la porción de la imagen para este proceso
        local_image = image[start_row:end_row, :]

        # Definir el kernel
        kernel = self.kernel

        # Convertir la porción de la imagen a escala de grises
        local_gray_image = cv2.cvtColor(local_image, cv2.COLOR_BGR2GRAY)

        # Aplicar el filtro convolucional localmente
        local_filtered_image = cv2.filter2D(local_gray_image, -1, kernel)

        # Recopilar todas las porciones filtradas
        filtered_images = comm.gather(local_filtered_image, root=0)

        # El proceso 0 muestra las imágenes
        if rank == 0:
            # Combinar las imágenes filtradas
            filtered_image = np.vstack(filtered_images)
            
                # Obtener dimensiones de la imagen filtrada
            filtered_height, filtered_width = filtered_image.shape

            # Calcular estadísticas de los píxeles
            min_pixel_value = np.min(filtered_image)
            max_pixel_value = np.max(filtered_image)
            mean_pixel_value = np.mean(filtered_image)
            std_dev_pixel_value = np.std(filtered_image)

            # Mostrar información
            print(f"Dimensiones de la imagen filtrada: {filtered_height} x {filtered_width}")
            print(f"Valor mínimo de píxel: {min_pixel_value}")
            print(f"Valor máximo de píxel: {max_pixel_value}")
            print(f"Valor medio de píxeles: {mean_pixel_value}")
            print(f"Desviación estándar de píxeles: {std_dev_pixel_value}")

            #Nombre al azar para la imagen fultada
            nombre_unico = str(uuid.uuid4()) + '.jpg'
            ruta_guardado = os.path.join('ImagenesFiltradas', nombre_unico)

            # Descarga imagen filtrada
            cv2.imwrite(ruta_guardado, filtered_image)