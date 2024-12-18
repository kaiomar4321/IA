import cv2 as cv

# Leer la imagen
img = cv.imread('salida.jpg', 1)

# Convertir la imagen de BGR a RGB y luego a HSV
img2 = cv.cvtColor(img, cv.COLOR_BGR2RGB)
img3 = cv.cvtColor(img2, cv.COLOR_RGB2HSV)

# Definir los umbrales para los colores en HSV
umbralBajo = (0, 80, 80)
umbralAlto = (10, 255, 255)
umbralBajoB = (170, 80, 80)
umbralAltoB = (180, 255, 255)

umbralBajoY = (10, 80, 80)
umbralAltoY = (37, 255, 255)

umbralBajoBL = (90, 80, 80)
umbralAltoBL = (130, 255, 255)

umbralBajoG = (45, 80, 80)
umbralAltoG = (87, 255, 255)

# Crear máscaras para cada color
mascara1 = cv.inRange(img3, umbralBajo, umbralAlto)
mascara2 = cv.inRange(img3, umbralBajoB, umbralAltoB)
mascaraYellow = cv.inRange(img3, umbralBajoY, umbralAltoY)
mascaraBlue = cv.inRange(img3, umbralBajoBL, umbralAltoBL)
mascaraGreen = cv.inRange(img3, umbralBajoG, umbralAltoG)

# Sumar las dos máscaras del color rojo
mascaraRoja = mascara1 + mascara2

# Función para contar islas y dibujar los contornos
def contar_islas_y_dibujar(mascara, img_original, min_ancho, min_alto):
    # Encontrar los contornos en la máscara
    contornos, _ = cv.findContours(mascara, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    islas = 0
    for contorno in contornos:
        # Obtener el bounding box (rectángulo) alrededor del contorno
        x, y, ancho, alto = cv.boundingRect(contorno)
        # Filtrar solo las islas que cumplen con el tamaño mínimo
        if ancho >= min_ancho and alto >= min_alto:
            islas += 1
            # Dibujar el contorno en la imagen original (color rojo: (0, 0, 255))
            cv.drawContours(img_original, [contorno], -1, (0, 0, 255), 2)
    return islas

# Parámetros mínimos de ancho y alto para filtrar las islas
min_ancho = 20  # puedes ajustar según tus necesidades
min_alto = 20   # puedes ajustar según tus necesidades

# Contar cuántas islas hay de cada color y dibujar sus contornos
islas_rojas = contar_islas_y_dibujar(mascaraRoja, img, min_ancho, min_alto)
islas_amarillas = contar_islas_y_dibujar(mascaraYellow, img, min_ancho, min_alto)
islas_azules = contar_islas_y_dibujar(mascaraBlue, img, min_ancho, min_alto)
islas_verdes = contar_islas_y_dibujar(mascaraGreen, img, min_ancho, min_alto)

# Mostrar los resultados en la consola
print(f'Islas rojas (mín. {min_ancho}x{min_alto}): {islas_rojas}')
print(f'Islas amarillas (mín. {min_ancho}x{min_alto}): {islas_amarillas}')
print(f'Islas azules (mín. {min_ancho}x{min_alto}): {islas_azules}')
print(f'Islas verdes (mín. {min_ancho}x{min_alto}): {islas_verdes}')

# Mostrar la imagen con los contornos rojos de las islas detectadas
cv.imshow('Islas detectadas con contornos rojos', img)

cv.waitKey(0)
cv.destroyAllWindows()
