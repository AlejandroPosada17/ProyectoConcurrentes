import os
os.environ['PYOPENGL_PLATFORM'] = 'egl'
import cv2
from multiprocessing import Pool
import numpy as np

class Filtrados:
    def __init__(self, kernel,num_threads_or_processes):
        self.kernel = kernel
        self.num_threads_or_processes = num_threads_or_processes
        
        
    def multiprocessing(self):
        # Cargar la imagen
        image_path = 'messi.png'  # Reemplaza con la ruta de tu imagen
        img = cv2.imread(image_path)

        # Verificar si la imagen se cargó correctamente
        if img is not None:
            # Dividir la imagen en secciones para el multiprocesamiento
            sections = np.array_split(img, 4)  # Dividir en 4 secciones, puedes ajustar esto según el número de núcleos de tu CPU

            # Iniciar el pool de procesos
            with Pool(2) as pool:
                # Aplicar el filtro en paralelo a cada sección de la imagen
                 results = pool.map(self.apply_filter_kernel, sections)

            # Combinar los resultados en una sola imagen
            filtered_img = np.vstack(results)

            # Descarga imagen filtrada
            cv2.imwrite('imagen_filtrada.jpg', filtered_img)
            
            # Mostrar las dimensiones de la imagen filtrada
            print(f"Dimensiones de la imagen filtrada: {filtered_img.shape}")

            # Obtener valor mínimo, máximo, medio y desviación estándar de los píxeles
            min_val = np.min(filtered_img)
            max_val = np.max(filtered_img)
            mean_val = np.mean(filtered_img)
            std_dev = np.std(filtered_img)

            print(f"Valor mínimo de los píxeles: {min_val}")
            print(f"Valor máximo de los píxeles: {max_val}")
            print(f"Valor medio de los píxeles: {mean_val}")
            print(f"Desviación estándar de los píxeles: {std_dev}")
        
        else:
            print("No se pudo cargar la imagen. Verifica la ruta y el formato de la imagen.")
    
    def apply_filter_kernel(self, img_section):
        print(self.num_threads_or_processes)
        kernel = self.kernel
        
        filtered_section = cv2.filter2D(img_section, -1, kernel)
        return filtered_section