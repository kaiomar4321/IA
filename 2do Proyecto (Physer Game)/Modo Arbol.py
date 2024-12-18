import pygame
import random
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
w, h = 800, 400
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego: Disparo de Bala, Salto, Nave y Menú")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Variables del jugador, bala, nave, fondo, etc.
jugador = None
bala = None
fondo = None
nave = None
menu = None
clf = None
# Variables de salto
salto = False
salto_altura = 15  # Velocidad inicial de salto
gravedad = 1
en_suelo = True
modo_auto_arbol = False
# Variables de pausa y menú
pausa = False
fuente = pygame.font.SysFont('Arial', 24)
menu_activo = True
modo_auto = False  # Indica si el modo de juego es automático

# Lista para guardar los datos de velocidad, distancia y salto (target)
datos_modelo = []

# Cargar las imágenes
jugador_frames = [
    pygame.image.load('assets/sprites/Son/resoluciones_cambiadas/Son (1).png'),
    pygame.image.load('assets/sprites/Son/resoluciones_cambiadas/Son (2).png'),
    pygame.image.load('assets/sprites/Son/resoluciones_cambiadas/Son (3).png'),
    pygame.image.load('assets/sprites/Son/resoluciones_cambiadas/Son (4).png'),
    pygame.image.load('assets/sprites/Son/resoluciones_cambiadas/Son (5).png'),
    pygame.image.load('assets/sprites/Son/resoluciones_cambiadas/Son (6).png'),
    pygame.image.load('assets/sprites/Son/resoluciones_cambiadas/Son (7).png'),
    pygame.image.load('assets/sprites/Son/resoluciones_cambiadas/Son (8).png'),
    pygame.image.load('assets/sprites/Son/resoluciones_cambiadas/Son (9).png'),
    pygame.image.load('assets/sprites/Son/resoluciones_cambiadas/Son (10).png'),
    pygame.image.load('assets/sprites/Son/resoluciones_cambiadas/Son (11).png'),
    pygame.image.load('assets/sprites/Son/resoluciones_cambiadas/Son (12).png'),
    pygame.image.load('assets/sprites/Son/resoluciones_cambiadas/Son (13).png'),
    pygame.image.load('assets/sprites/Son/resoluciones_cambiadas/Son (14).png'),
    pygame.image.load('assets/sprites/Son/resoluciones_cambiadas/Son (15).png'),
    pygame.image.load('assets/sprites/Son/resoluciones_cambiadas/Son (16).png'),

]

bala_img = pygame.image.load('assets/sprites/purple_ball.png')
fondo_img = pygame.image.load('assets/game/fondo4.jpg')
nave_img = pygame.image.load('assets/game/ufo.png')
menu_img = pygame.image.load('assets/game/menu.png')

# Escalar la imagen de fondo para que coincida con el tamaño de la pantalla
fondo_img = pygame.transform.scale(fondo_img, (w, h))

# Crear el rectángulo del jugador y de la bala
jugador = pygame.Rect(50, h - 100, 32, 48)
bala = pygame.Rect(w - 50, h - 90, 16, 16)
nave = pygame.Rect(w - 100, h - 100, 64, 64)
menu_rect = pygame.Rect(w // 2 - 135, h // 2 - 90, 270, 180)  # Tamaño del menú

# Variables para la animación del jugador
current_frame = 0
frame_speed = 1  # Cuántos frames antes de cambiar a la siguiente imagen
frame_count = 0

# Variables para la bala
velocidad_bala = -5  # Velocidad de la bala hacia la izquierda
bala_disparada = False

# Variables para el fondo en movimiento
fondo_x1 = 0
fondo_x2 = w

# Función para disparar la bala
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-8, -3)  # Velocidad aleatoria negativa para la bala
        bala_disparada = True

# Función para reiniciar la posición de la bala
def reset_bala():
    global bala, bala_disparada
    bala.x = w - 50  # Reiniciar la posición de la bala
    bala_disparada = False

# Función para manejar el salto
def manejar_salto():
    global jugador, salto, salto_altura, gravedad, en_suelo

    if salto:
        jugador.y -= salto_altura  # Mover al jugador hacia arriba
        salto_altura -= gravedad  # Aplicar gravedad (reduce la velocidad del salto)

        # Si el jugador llega al suelo, detener el salto
        if jugador.y >= h - 100:
            jugador.y = h - 100
            salto = False
            salto_altura = 15  # Restablecer la velocidad de salto
            en_suelo = True

# Función para actualizar el juego
def update():
    global bala, velocidad_bala, current_frame, frame_count, fondo_x1, fondo_x2

    # Mover el fondo
    fondo_x1 -= 1
    fondo_x2 -= 1

    # Si el primer fondo sale de la pantalla, lo movemos detrás del segundo
    if fondo_x1 <= -w:
        fondo_x1 = w

    # Si el segundo fondo sale de la pantalla, lo movemos detrás del primero
    if fondo_x2 <= -w:
        fondo_x2 = w

    # Dibujar los fondos
    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))

    # Animación del jugador
    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0

    # Dibujar el jugador con la animación
    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))

    # Dibujar la nave
    pantalla.blit(nave_img, (nave.x, nave.y))

    # Mover y dibujar la bala
    if bala_disparada:
        bala.x += velocidad_bala

    # Si la bala sale de la pantalla, reiniciar su posición
    if bala.x < 0:
        reset_bala()

    pantalla.blit(bala_img, (bala.x, bala.y))

    # Colisión entre la bala y el jugador
    if jugador.colliderect(bala):
        print("Colisión detectada!")
        reiniciar_juego()  # Terminar el juego y mostrar el menú

# Función para guardar datos del modelo en modo manual
def guardar_datos():
    global jugador, bala, velocidad_bala, salto
    distancia = abs(jugador.x - bala.x)
    salto_hecho = 1 if salto else 0  # 1 si saltó, 0 si no saltó
    # Guardar velocidad de la bala, distancia al jugador y si saltó o no
    datos_modelo.append((velocidad_bala, distancia, salto_hecho))

# Función para pausar el juego y guardar los datos
def pausa_juego():
    global pausa, modo_auto_red, menu_activo

    pausa = not pausa
    if pausa:
        print("Juego pausado. Datos registrados hasta ahora:", datos_modelo)
        
        # Mostrar menú de pausa
        while pausa:
            pantalla.fill(NEGRO)
            texto_continuar = fuente.render("Presiona 'C' para continuar", True, BLANCO)
            texto_menu = fuente.render("Presiona 'M' para volver al menú principal", True, BLANCO)
            pantalla.blit(texto_continuar, (w // 4, h // 2 - 30))
            pantalla.blit(texto_menu, (w // 4, h // 2 + 10))
            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_c:  # Continuar
                        pausa = False
                    elif evento.key == pygame.K_m:  # Volver al menú principal


                        reiniciar_juego()
                        pausa = not pausa
                        return

def modo_juego_automatico_arbol():
    global clf, jugador, bala, velocidad_bala, salto, en_suelo

    if clf is not None:
        distancia = abs(jugador.x - bala.x)
        entrada = pd.DataFrame([[velocidad_bala, distancia]], columns=["velocidad_bala", "distancia"])

        # Predecir el salto
        prediccion = clf.predict(entrada)[0]
        print(f"Predicción del árbol de decisión: {prediccion}")

        if prediccion == 1 and en_suelo:
            print("¡Salta! Acción automatizada del árbol de decisión.")
            salto = True
            en_suelo = False
    else:
        print("El modelo de árbol de decisión no ha sido entrenado. Por favor, entrena el modelo primero.")


def entrenar_modelo_arbol():
    global clf, datos_modelo
    if len(datos_modelo) > 0 and not modo_auto_arbol:
        # Crear un DataFrame a partir de los datos recopilados
        df = pd.DataFrame(datos_modelo, columns=["velocidad_bala", "distancia", "salto"])
        X = df[["velocidad_bala", "distancia"]]
        y = df["salto"]

        # Dividir los datos en entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Entrenar el modelo de árbol de decisión
        clf = DecisionTreeClassifier()
        clf.fit(X_train, y_train)
        print("Modelo entrenado con éxito.")
    else:
        print("No hay datos suficientes o el modo automático está activado. No se puede entrenar el modelo.")
# Función para mostrar el menú y seleccionar el modo de juego
def mostrar_menu():
    global menu_activo, modo_auto_arbol
    pantalla.fill(NEGRO)
    texto = fuente.render("Presiona 'A' para Auto, 'M' para Manual, o 'Q' para Salir", True, BLANCO)
    pantalla.blit(texto, (w // 4, h // 2))
    pygame.display.flip()

    while menu_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:
                    entrenar_modelo_arbol()
                    modo_auto_arbol = True
                    menu_activo = False
                elif evento.key == pygame.K_m:
                    datos_modelo=[]
                    modo_auto_arbol = False
                    menu_activo = False
                elif evento.key == pygame.K_q:
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()

# Función para reiniciar el juego tras la colisión
def reiniciar_juego():
    global menu_activo, jugador, bala, nave, bala_disparada, salto, en_suelo
    menu_activo = True  # Activar de nuevo el menú
    jugador.x, jugador.y = 50, h - 100  # Reiniciar posición del jugador
    bala.x = w - 50  # Reiniciar posición de la bala
    nave.x, nave.y = w - 100, h - 100  # Reiniciar posición de la nave
    bala_disparada = False
    salto = False
    en_suelo = True
    # Mostrar los datos recopilados hasta el momento
    print("Datos recopilados para el modelo: ", datos_modelo)
    mostrar_menu()  # Mostrar el menú de nuevo para seleccionar modo

def main():
    global salto, en_suelo, bala_disparada

    reloj = pygame.time.Clock()
    mostrar_menu()
    correr = True

    while correr:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo and not pausa and not modo_auto_arbol:
                    salto = True
                    en_suelo = False
                if evento.key == pygame.K_p:
                    pausa_juego()
                if evento.key == pygame.K_q:
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()

        if not pausa:

            if modo_auto_arbol:
                modo_juego_automatico_arbol()
                if salto:
                    manejar_salto()
            else:
                guardar_datos()
                if salto:
                    manejar_salto()
            if not bala_disparada:
                disparar_bala()
            update()

        pygame.display.flip()
        reloj.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
