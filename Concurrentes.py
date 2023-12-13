import streamlit as st
from filtrados import Filtrados
from kernels import Kernels
from DescargaImagenes import Guardado_Imagenes
from PIL import Image
import os
import random

tema_Busqueda = st.text_input("Ingrese el tema para descargar las imagenes") 

# Funciones
def load_images():   
    Guardado_Imagenes(tema_Busqueda)

# Boton para descragar imagenes
if st.button("Cargar imágenes"):
    load_images()

def apply_filter(kernel, option, num_threads_or_processes):
    misKernels = Kernels()
    directorio = './Imagenes'
        # Obtener la lista de archivos de imagen en el directorio
    archivos_imagen = [f for f in os.listdir(directorio) if f.endswith(('jpg', 'png'))]
        # Elegir 10 imágenes al azar si hay más de 10 disponibles
    imagenes_seleccionadas = random.sample(archivos_imagen, min(3, len(archivos_imagen)))
    
    objetoMultipro = None
    if kernel == "El primero de los Class 1":
        kernel_to_use = misKernels.class1
    elif kernel == "Square 3x3":
        kernel_to_use = misKernels.square33
    

    if option == "Multiprocessing":

        # Proceso para cada imagen seleccionada
        for imagen in imagenes_seleccionadas:
            ruta_imagen = os.path.join(directorio, imagen)
            
            # Procesar la imagen (ejemplo: mostrar el tamaño de cada imagen)
            img = Image.open(ruta_imagen)
            ancho, alto = img.size
            print(f"Imagen: {imagen} - Tamaño: {ancho}x{alto}")
            
            objetoMultipro = Filtrados(kernel_to_use, num_threads_or_processes,ruta_imagen)
            objetoMultipro.multiprocessing()
           
        
            # Cargar las imágenes
            imagen_normal = Image.open(ruta_imagen)
            imagen_filtrada = Image.open('imagen_filtrada.jpg')

            # Mostrar las imágenes una al lado de la otra
            col1, col2 = st.columns(2)
            with col1:
                st.image(imagen_normal, caption='Imagen Normal', use_column_width=True)

            with col2:
                st.image(imagen_filtrada, caption='Imagen Filtrada', use_column_width=True)

            # Cerrar la imagen abierta
            img.close()
    elif option == "MPI":
        objetoMultipro = Filtrados(kernel_to_use, num_threads_or_processes,)
        objetoMultipro.filtro4Py()
   




# Lista de kernels disponibles
kernels = ["El primero de los Class 1", "Square 3x3", "Square 5x5", "Sobel X", "Sobel Y", "Laplacian"] 

# Opciones de frameworks/librerías
options = ["C", "OpenMP", "Multiprocessing", "MPI", "PyCUDA"]

# Selección de framework/librería
option = st.selectbox("Seleccione framework/librería", options)

if option == "C":
    # Opciones específicas para C
    num_threads_or_processes = st.slider("Número de hilos", 1, 8, 1) 

elif option == "OpenMP":
    num_threads_or_processes = st.slider("Número de hilos", 1, 8, 1)

elif option == "Multiprocessing":
    num_threads_or_processes = st.slider("Número de procesos", 1, 8, 1)

elif option == "MPI":
    num_threads_or_processes = st.slider("Número de procesos", 1, 8, 1) 

elif option == "PyCUDA":
    num_blocks = st.slider("Número de bloques", 1, 64, 1)
    threads_per_block = st.slider("Hilos por bloque", 1, 1024, 1)

# Selección de kernel  
kernel = st.selectbox("Seleccione el kernel", kernels)
        
# Boton para filtrar imagenes
if st.button("Filtrar imágenes"):
    filtered_images = apply_filter(kernel, option, num_threads_or_processes)
