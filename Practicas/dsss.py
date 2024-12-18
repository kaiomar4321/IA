import cv2 as cv

# Inicializar la captura de video
cap = cv.VideoCapture(0)
i = 0

while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Convertir a escala de grises
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    # Aplicar desenfoque para reducir ruido
    blurred = cv.GaussianBlur(gray, (5, 5), 0)
    
    # Aplicar detección de bordes con Canny
    edges = cv.Canny(blurred, 50, 150)
    
    # Encontrar contornos en la imagen de bordes
    contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    # Dibujar los contornos en el frame original
    cv.drawContours(frame, contours, -1, (0, 255, 0), 2)
    
    # Mostrar el resultado con los contornos dibujados
    cv.imshow('Detección de Objetos', frame)
    
    # Guardar las imágenes con contornos si se detectan objetos
    if len(contours) > 0:
        cv.imwrite(f'/home/omar/objeto_{i}.jpg', frame)
        i += 1

    # Salir si se presiona la tecla 'Esc'
    k = cv.waitKey(1)
    if k == 27:
        break

# Liberar los recursos
cap.release()
cv.destroyAllWindows()

