import pygame
import random

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (128, 128, 128)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
NARANJA = (255, 165, 0)

# Configuración del juego
ANCHO_BLOQUE = 30
ALTO_BLOQUE = 30
ANCHO_TABLERO = 10
ALTO_TABLERO = 20
ANCHO_VENTANA = ANCHO_BLOQUE * (ANCHO_TABLERO + 8)
ALTO_VENTANA = ALTO_BLOQUE * ALTO_TABLERO

# Formas de las piezas
PIEZAS = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

COLORES = [CYAN, AMARILLO, MAGENTA, NARANJA, AZUL, VERDE, ROJO]

class Pieza:
    def __init__(self): #inicializa la pieza
        self.forma = random.choice(PIEZAS)
        self.color = COLORES[PIEZAS.index(self.forma)] 
        self.x = ANCHO_TABLERO // 2 - len(self.forma[0]) // 2 
        self.y = 0

    def rotar(self):
        self.forma = list(zip(*self.forma[::-1]))

class Tetris:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption("Tetris")
        self.reloj = pygame.time.Clock() 
        self.tablero = [[0 for _ in range(ANCHO_TABLERO)] for _ in range(ALTO_TABLERO)]
        self.pieza_actual = Pieza()
        self.siguiente_pieza = Pieza()  # Nueva pieza para mostrar
        self.puntuacion = 0
        self.juego_terminado = False
        self.velocidad = 0.5
        self.tiempo_anterior = pygame.time.get_ticks()

    def dibujar_tablero(self):
        for y in range(ALTO_TABLERO):
            for x in range(ANCHO_TABLERO):
                pygame.draw.rect(self.pantalla, GRIS,
                               [x * ANCHO_BLOQUE, y * ALTO_BLOQUE, ANCHO_BLOQUE, ALTO_BLOQUE], 1)
                if self.tablero[y][x]:
                    pygame.draw.rect(self.pantalla, self.tablero[y][x],
                                   [x * ANCHO_BLOQUE + 1, y * ALTO_BLOQUE + 1, ANCHO_BLOQUE - 2, ALTO_BLOQUE - 2])

    def dibujar_pieza(self):
        for y, fila in enumerate(self.pieza_actual.forma):
            for x, celda in enumerate(fila):
                if celda:
                    pygame.draw.rect(self.pantalla, self.pieza_actual.color,
                                   [(self.pieza_actual.x + x) * ANCHO_BLOQUE + 1,
                                    (self.pieza_actual.y + y) * ALTO_BLOQUE + 1,
                                    ANCHO_BLOQUE - 2, ALTO_BLOQUE - 2])

    def dibujar_siguiente_pieza(self):
        # Dibujar el área de la siguiente pieza
        area_x = ANCHO_TABLERO * ANCHO_BLOQUE + 20
        area_y = 100
        pygame.draw.rect(self.pantalla, GRIS, [area_x, area_y, 5 * ANCHO_BLOQUE, 5 * ALTO_BLOQUE], 1)
        
        # Dibujar el texto "Siguiente"
        fuente = pygame.font.Font(None, 36)
        texto = fuente.render("Siguiente:", True, BLANCO)
        self.pantalla.blit(texto, (area_x, area_y - 40))

        # Dibujar la siguiente pieza
        for y, fila in enumerate(self.siguiente_pieza.forma):
            for x, celda in enumerate(fila):
                if celda:
                    pygame.draw.rect(self.pantalla, self.siguiente_pieza.color,
                                   [area_x + (x + 1) * ANCHO_BLOQUE + 1,
                                    area_y + (y + 1) * ALTO_BLOQUE + 1,
                                    ANCHO_BLOQUE - 2, ALTO_BLOQUE - 2])

    def colision(self, dx=0, dy=0):
        for y, fila in enumerate(self.pieza_actual.forma):
            for x, celda in enumerate(fila):
                if celda:
                    nueva_x = self.pieza_actual.x + x + dx
                    nueva_y = self.pieza_actual.y + y + dy
                    if (nueva_x < 0 or nueva_x >= ANCHO_TABLERO or
                        nueva_y >= ALTO_TABLERO or
                        (nueva_y >= 0 and self.tablero[nueva_y][nueva_x])):
                        return True
        return False

    def fijar_pieza(self):
        for y, fila in enumerate(self.pieza_actual.forma):
            for x, celda in enumerate(fila):
                if celda:
                    self.tablero[self.pieza_actual.y + y][self.pieza_actual.x + x] = self.pieza_actual.color
        self.eliminar_lineas()
        self.pieza_actual = self.siguiente_pieza  # Usar la siguiente pieza
        self.siguiente_pieza = Pieza()  # Generar nueva siguiente pieza
        if self.colision():
            self.juego_terminado = True

    def eliminar_lineas(self):
        lineas_eliminadas = 0
        y = ALTO_TABLERO - 1
        while y >= 0:
            if all(self.tablero[y]):
                lineas_eliminadas += 1
                for y2 in range(y, 0, -1):
                    self.tablero[y2] = self.tablero[y2-1][:]
                self.tablero[0] = [0] * ANCHO_TABLERO
            else:
                y -= 1
        self.puntuacion += lineas_eliminadas * 100

    def dibujar_puntuacion(self):
        fuente = pygame.font.Font(None, 36)
        texto = fuente.render(f"Puntuación: {self.puntuacion}", True, BLANCO)
        self.pantalla.blit(texto, (ANCHO_TABLERO * ANCHO_BLOQUE + 10, 10))

    def ejecutar(self):
        while not self.juego_terminado:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_anterior > self.velocidad * 1000:
                if not self.colision(dy=1):
                    self.pieza_actual.y += 1
                else:
                    self.fijar_pieza()
                self.tiempo_anterior = tiempo_actual

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_LEFT and not self.colision(dx=-1):
                        self.pieza_actual.x -= 1
                    elif evento.key == pygame.K_RIGHT and not self.colision(dx=1):
                        self.pieza_actual.x += 1
                    elif evento.key == pygame.K_DOWN and not self.colision(dy=1):
                        self.pieza_actual.y += 1
                    elif evento.key == pygame.K_UP:
                        pieza_anterior = self.pieza_actual.forma
                        self.pieza_actual.rotar()
                        if self.colision():
                            self.pieza_actual.forma = pieza_anterior

            self.pantalla.fill(NEGRO)
            self.dibujar_tablero()
            self.dibujar_pieza()
            self.dibujar_siguiente_pieza()  # Dibujar la siguiente pieza
            self.dibujar_puntuacion()
            pygame.display.flip()
            self.reloj.tick(60)

        # Pantalla de Game Over
        fuente = pygame.font.Font(None, 48)
        texto = fuente.render("¡GAME OVER!", True, ROJO)
        texto_rect = texto.get_rect(center=(ANCHO_VENTANA/2, ALTO_VENTANA/2))
        self.pantalla.blit(texto, texto_rect)
        pygame.display.flip()
        pygame.time.wait(2000)

if __name__ == "__main__":
    juego = Tetris()
    juego.ejecutar()
    pygame.quit() 