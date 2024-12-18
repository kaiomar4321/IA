import cv2

# Cargar el clasificador Haar para detección de rostros
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Capturar el video desde la cámara (0 es la cámara predeterminada)
cap = cv2.VideoCapture(0)

while True:
    # Leer el frame de la cámara
    ret, frame = cap.read()

    if not ret:
        print("No se pudo acceder a la cámara.")
        break

    # Convertir el frame a escala de grises (necesario para la detección de rostros)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar los rostros en la imagen
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Dibujar rectángulos alrededor de los rostros detectados
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Mostrar el video con los rostros detectados
    cv2.imshow('Detección de Rostros', frame)

    # Salir si se presiona 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()
