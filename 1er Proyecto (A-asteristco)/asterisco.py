import pygame
from queue import PriorityQueue
import time

ANCHO_VENTANA = 800
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Visualización de Nodos")

# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)
AZUL_CIELO = (135, 206, 250)

pygame.font.init()
FUENTE = pygame.font.Font(None, 18) 


class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        self.g = float("inf")  
        self.h = float("inf")  
        self.f = float("inf")  
        self.padre = None  
        self.contador = 0  

    def get_pos(self):
        return self.fila, self.col

    def actualizar_costos(self, g, h, padre, contador):
        self.g = g
        self.h = h
        self.f = g + h
        self.padre = padre
        self.contador = contador

    def hacer_cerrado(self):
        self.color = ROJO

    def hacer_abierto(self):
        self.color = AZUL_CIELO

    def hacer_inicio(self):
        self.color = NARANJA

    def hacer_fin(self):
        self.color = PURPURA

    def hacer_pared(self):
        self.color = NEGRO

    def hacer_camino(self):
        self.color = VERDE

    def restablecer(self):
        self.color = BLANCO

    def dibujar(self, ventana):
        # Dibuja el rectángulo
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))
        if self.g != float("inf") or self.h != float("inf"):
            texto_g = FUENTE.render(f"g:{self.g}", True, NEGRO)
            texto_h = FUENTE.render(f"h:{self.h}", True, NEGRO)
            texto_f = FUENTE.render(f"f:{self.f}", True, NEGRO)

            ventana.blit(texto_g, (self.x + 5, self.y + 5))  
            ventana.blit(texto_h, (self.x + 5, self.y + 20))
            ventana.blit(texto_f, (self.x + 5, self.y + 35))

        
        if self.contador > 0:
            texto_c = FUENTE.render(f"#{self.contador}", True, NEGRO)
            ventana.blit(texto_c, (self.x + self.ancho // 2 - 5, self.y + self.ancho // 2 - 10))


    def __lt__(self, otro):
        return self.f < otro.f


def heuristica(pos1, pos2):
    
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)


def vecinos(nodo, grid):
    filas = nodo.total_filas
    vecinos_list = []
    fila, col = nodo.fila, nodo.col

    movimientos = [
        (-1, 0, 1), (1, 0, 1), (0, -1, 1), (0, 1, 1),  
        (-1, -1, 1.4), (-1, 1, 1.4), (1, -1, 1.4), (1, 1, 1.4)  
    ]

    for df, dc, costo in movimientos:
        nueva_fila, nueva_col = fila + df, col + dc
        if 0 <= nueva_fila < filas and 0 <= nueva_col < filas:
            vecino = grid[nueva_fila][nueva_col]
            vecinos_list.append((vecino, costo))
    return vecinos_list


def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas)
            grid[i].append(nodo)
    return grid


def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))


def dibujar(ventana, grid, filas, ancho):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)
    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()


def reconstruir_camino(nodo_actual, ventana, grid, filas, ancho):
    while nodo_actual.padre:
        nodo_actual.hacer_camino()
        nodo_actual = nodo_actual.padre
        dibujar(ventana, grid, filas, ancho)


def algoritmo_heuristico(grid, inicio, fin, ventana, ancho):
    open_set = PriorityQueue()
    open_set.put((0, inicio))
    inicio.actualizar_costos(0, heuristica(inicio.get_pos(), fin.get_pos()), None, 1)
    visitados = {inicio}
    contador = 2

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        pygame.time.delay(700)

        nodo_actual = open_set.get()[1]

        if nodo_actual == fin:
            reconstruir_camino(fin, ventana, grid, len(grid), ancho)
            return True

        for vecino, costo in vecinos(nodo_actual, grid):
            if vecino.color == NEGRO:  
                continue

            nuevo_g = nodo_actual.g + costo
            if nuevo_g < vecino.g:  
                vecino.actualizar_costos(nuevo_g, heuristica(vecino.get_pos(), fin.get_pos()), nodo_actual, contador)
                contador += 1
                vecino.hacer_abierto()
                open_set.put((vecino.f, vecino))

        if nodo_actual != inicio:
            nodo_actual.hacer_cerrado()

        dibujar(ventana, grid, len(grid), ancho)

    return False


def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    y, x = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col


def main(ventana, ancho):
    FILAS = 9
    grid = crear_grid(FILAS, ancho)

    inicio = None
    fin = None

    corriendo = True
    while corriendo:
        dibujar(ventana, grid, FILAS, ancho)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            if pygame.mouse.get_pressed()[0]: 
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                if not inicio and nodo != fin:
                    inicio = nodo
                    inicio.hacer_inicio()
                elif not fin and nodo != inicio:
                    fin = nodo
                    fin.hacer_fin()
                elif nodo != fin and nodo != inicio:
                    nodo.hacer_pared()

            elif pygame.mouse.get_pressed()[2]: 
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                nodo.restablecer()
                if nodo == inicio:
                    inicio = None
                elif nodo == fin:
                    fin = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and inicio and fin:
                    algoritmo_heuristico(grid, inicio, fin, ventana, ancho)

    pygame.quit()


main(VENTANA, ANCHO_VENTANA)
