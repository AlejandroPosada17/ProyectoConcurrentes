import streamlit as st
import numpy as np

# Lista de kernels disponibles
kernels = ["Square 3x3", "Square 5x5", "Sobel X", "Sobel Y", "Laplacian"] 

# Opciones de frameworks/librerías
options = ["C", "OpenMP", "Multiprocessing", "MPI", "PyCUDA"]

# Selección de framework/librería
option = st.selectbox("Seleccione framework/librería", options)

if option == "C":
    # Opciones específicas para C
    num_threads = st.slider("Número de hilos", 1, 8, 1) 

elif option == "OpenMP":
    num_threads = st.slider("Número de hilos", 1, 8, 1)

elif option == "Multiprocessing":
    num_processes = st.slider("Número de procesos", 1, 8, 1)

elif option == "MPI":
    num_processes = st.slider("Número de procesos", 1, 8, 1) 

elif option == "PyCUDA":
    num_blocks = st.slider("Número de bloques", 1, 64, 1)
    threads_per_block = st.slider("Hilos por bloque", 1, 1024, 1)

# Selección de kernel  
kernel = st.selectbox("Seleccione el kernel", kernels)

# Funciones
def load_images():   
    print("cargando las imagenes")

def apply_filter(kernel, option, num_threads):
    print("aplicando filtros")
# Botones
if st.button("Cargar imágenes"):
    load_images()

if st.button("Filtrar imágenes"):
    filtered_images = apply_filter(kernel, option, num_threads)
