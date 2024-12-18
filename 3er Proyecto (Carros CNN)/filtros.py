import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from tensorflow.keras.utils import img_to_array, array_to_img
import cv2
import random

# Directorio de las imágenes originales
dirname = os.path.join(os.getcwd(),'carros2/')
imgpath = dirname + os.sep 

# Configuración de los parámetros del generador de imágenes
datagen = ImageDataGenerator(
    rotation_range=30,        # Rango de rotación aleatoria

    shear_range=0.1,          # Desplazamiento por corte
    zoom_range=[0.8, 1.0],    # Zoom aleatorio entre 50% y 150%
    horizontal_flip=True,     # Volteo horizontal aleatorio
    fill_mode='nearest',     # Relleno constante (rellenará con negro)
    cval=0,                   # El valor constante usado para el relleno negro (0 para negro)
    brightness_range=[0.5, 1.5]  # Rango de brillo entre 50% y 150%
)

# Función para aplicar el filtro de brillo y oscuridad manualmente
def adjust_brightness(img, factor):
    # factor > 1 aumenta el brillo, factor < 1 oscurece
    img = np.array(img, dtype=np.float32)
    img = img * factor
    img = np.clip(img, 0, 255)  # Asegurar que los valores estén entre 0 y 255
    return np.uint8(img)

# Función para cargar las imágenes, transformarlas y guardarlas en la misma carpeta
def generate_and_save_images():
    for root, dirnames, filenames in os.walk(imgpath):
        for dirname in dirnames:
            dir_path = os.path.join(root, dirname)  # Ruta completa de la carpeta de las imágenes

            # Procesar todas las imágenes de la carpeta
            for filename in os.listdir(dir_path):
                if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
                    file_path = os.path.join(dir_path, filename)
                    img = image.load_img(file_path)  # Cargar imagen
                    img_array = img_to_array(img)   # Convertir la imagen a un array numpy

                    # Redimensionar la imagen al tamaño deseado (si es necesario)
                    img_array = cv2.resize(img_array, (60, 45))

                    # Ajustar brillo de manera manual (en un factor aleatorio)
                    brightness_factor = random.uniform(0.5, 1.5)  # Ajuste aleatorio entre 50% y 150%
                    img_array = adjust_brightness(img_array, brightness_factor)

                    # Reshaping de la imagen para adaptarla a ImageDataGenerator
                    img_array = np.expand_dims(img_array, axis=0)
                    
                    # Generar imágenes transformadas y guardarlas en la misma carpeta
                    i = 0
                    for batch in datagen.flow(img_array, batch_size=1, save_to_dir=dir_path, save_prefix="aug", save_format='jpeg'):
                        i += 1
                        if i > 8:  # Limitar el número de imágenes generadas por cada imagen original
                            break

            print(f"Imágenes generadas para el directorio: {dirname}")
    
# Llamar a la función para generar las imágenes modificadaspassat varianttsuru
generate_and_save_images()
