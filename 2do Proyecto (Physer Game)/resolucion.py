import os
from PIL import Image

def cambiar_resolucion(carpeta, nueva_resolucion):
    """
    Cambia la resolución de todas las imágenes en una carpeta específica,
    agregando bordes transparentes si es necesario para mantener la proporción original.

    Args:
        carpeta (str): Ruta de la carpeta donde se encuentran las imágenes.
        nueva_resolucion (tuple): Nueva resolución deseada en formato (ancho, alto).
    """
    # Verificar si la carpeta existe
    if not os.path.isdir(carpeta):
        print(f"La carpeta '{carpeta}' no existe.")
        return

    # Crear carpeta de salida
    carpeta_salida = os.path.join(carpeta, "resoluciones_cambiadas")
    os.makedirs(carpeta_salida, exist_ok=True)

    # Iterar sobre los archivos en la carpeta
    for archivo in os.listdir(carpeta):
        ruta_completa = os.path.join(carpeta, archivo)

        # Verificar si el archivo es una imagen
        try:
            with Image.open(ruta_completa) as img:
                # Obtener dimensiones de la imagen original
                ancho_original, alto_original = img.size

                # Crear una imagen con fondo transparente y la nueva resolución
                imagen_nueva = Image.new("RGBA", nueva_resolucion, (0, 0, 0, 0))

                # Calcular las proporciones para redimensionar la imagen sin deformarla
                ratio_original = ancho_original / alto_original
                ratio_nuevo = nueva_resolucion[0] / nueva_resolucion[1]

                if ratio_original > ratio_nuevo:
                    # Ajustar por ancho
                    nuevo_ancho = nueva_resolucion[0]
                    nuevo_alto = int(nueva_resolucion[0] / ratio_original)
                else:
                    # Ajustar por alto
                    nuevo_alto = nueva_resolucion[1]
                    nuevo_ancho = int(nueva_resolucion[1] * ratio_original)

                # Redimensionar la imagen manteniendo la proporción
                img_redimensionada = img.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)

                # Calcular posición para centrar la imagen
                posicion_x = (nueva_resolucion[0] - nuevo_ancho) // 2
                posicion_y = (nueva_resolucion[1] - nuevo_alto) // 2

                # Pegar la imagen redimensionada en el fondo transparente
                imagen_nueva.paste(img_redimensionada, (posicion_x, posicion_y))

                # Guardar la imagen modificada en la carpeta de salida
                nombre_salida = os.path.join(carpeta_salida, archivo)
                imagen_nueva.save(nombre_salida)

                print(f"Imagen procesada y guardada: {nombre_salida}")
        except Exception as e:
            print(f"No se pudo procesar el archivo '{archivo}': {e}")

# Ejemplo de uso
if __name__ == "__main__":
    carpeta_imagenes = "./assets/sprites/MM"  # Ruta de la carpeta con imágenes
    resolucion = (29, 47)  # Nueva resolución deseada

    cambiar_resolucion(carpeta_imagenes, resolucion)
