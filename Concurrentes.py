import streamlit as st
from filtrados import Filtrados
from kernels import Kernels
from PIL import Image

# Funciones
def load_images():   
    print("cargando las imagenes")

def apply_filter(kernel, option, num_threads_or_processes):
    misKernels = Kernels()
    print("Aplicando filtros")
    
    objetoMultipro = None
    if kernel == "El primero de los Class 1":
        kernel_to_use = misKernels.class1
    elif kernel == "Square 3x3":
        kernel_to_use = misKernels.square33
    

    if option == "Multiprocessing":
        objetoMultipro = Filtrados(kernel_to_use, num_threads_or_processes)
        objetoMultipro.multiprocessing()
    elif option == "MPI":
        objetoMultipro = Filtrados(kernel_to_use, num_threads_or_processes)
        objetoMultipro.filtro4Py()
   

    if objetoMultipro:
        image = Image.open('imagen_filtrada.jpg')
        st.image(image, caption='Nombre de la imagen', use_column_width=True)


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
        
# Botones
if st.button("Cargar imágenes"):
    load_images()

if st.button("Filtrar imágenes"):
    filtered_images = apply_filter(kernel, option, num_threads_or_processes)
