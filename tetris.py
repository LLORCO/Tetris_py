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
        self.siguiente_pieza = Pieza()
        self.puntuacion = 0
        self.nivel = 1
        self.lineas_completadas = 0
        self.juego_terminado = False
        self.velocidad_base = 0.5
        self.velocidad = self.velocidad_base
        self.tiempo_anterior = pygame.time.get_ticks()
        self.mostrar_tetris = False
        self.tiempo_tetris = 0

    def actualizar_nivel(self):
        # Subir de nivel cada 10 líneas
        nuevo_nivel = (self.lineas_completadas // 10) + 1
        if nuevo_nivel > self.nivel:
            self.nivel = nuevo_nivel
            # Aumentar la velocidad con cada nivel (máximo 0.1 segundos)
            self.velocidad = max(0.1, self.velocidad_base - (self.nivel - 1) * 0.05)

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
        area_x = ANCHO_TABLERO * ANCHO_BLOQUE + 10
        area_y = 170  # Movido más abajo para evitar superposición
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

    def dibujar_mensaje_tetris(self):
        if self.mostrar_tetris:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_tetris < 1000:  # Mostrar por 1 segundo
                fuente = pygame.font.Font(None, 72)
                texto = fuente.render("TETRIS!!", True, AMARILLO)
                # Posicionar en la misma línea que GAME OVER
                texto_rect = texto.get_rect(center=(ANCHO_TABLERO * ANCHO_BLOQUE + 110, 350))
                self.pantalla.blit(texto, texto_rect)
            else:
                self.mostrar_tetris = False

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
        
        if lineas_eliminadas > 0:
            # Puntos base por línea
            puntos_base = 100
            # Multiplicador por nivel
            multiplicador = self.nivel
            
            # Bonus por múltiples líneas
            if lineas_eliminadas == 4:
                bonus = 4  # Tetris
                self.mostrar_tetris = True
                self.tiempo_tetris = pygame.time.get_ticks()
            elif lineas_eliminadas == 3:
                bonus = 2.5  # Triple
            elif lineas_eliminadas == 2:
                bonus = 1.5  # Doble
            else:
                bonus = 1  # Línea simple
            
            self.puntuacion += int(puntos_base * lineas_eliminadas * multiplicador * bonus)
            self.lineas_completadas += lineas_eliminadas
            self.actualizar_nivel()

    def dibujar_puntuacion(self):
        fuente = pygame.font.Font(None, 36)
        # Mostrar puntuación
        texto_puntuacion = fuente.render(f"Puntuación: {self.puntuacion}", True, BLANCO)
        self.pantalla.blit(texto_puntuacion, (ANCHO_TABLERO * ANCHO_BLOQUE + 10, 10))
        
        # Mostrar nivel
        texto_nivel = fuente.render(f"Nivel: {self.nivel}", True, BLANCO)
        self.pantalla.blit(texto_nivel, (ANCHO_TABLERO * ANCHO_BLOQUE + 10, 50))
        
        # Mostrar líneas completadas
        texto_lineas = fuente.render(f"Líneas: {self.lineas_completadas}", True, BLANCO)
        self.pantalla.blit(texto_lineas, (ANCHO_TABLERO * ANCHO_BLOQUE + 10, 90))

    def caida_inmediata(self):
        # Mover la pieza hacia abajo hasta que colisione
        while not self.colision(dy=1):
            self.pieza_actual.y += 1
        self.fijar_pieza()

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
                    elif evento.key == pygame.K_SPACE:
                        self.caida_inmediata()

            self.pantalla.fill(NEGRO)
            self.dibujar_tablero()
            self.dibujar_pieza()
            self.dibujar_siguiente_pieza()
            self.dibujar_puntuacion()
            self.dibujar_mensaje_tetris()
            pygame.display.flip()
            self.reloj.tick(60)

        # Pantalla de Game Over
        fuente = pygame.font.Font(None, 48)
        texto = fuente.render("GAME OVER", True, ROJO)
        # Posicionar más a la derecha
        texto_rect = texto.get_rect(center=(ANCHO_TABLERO * ANCHO_BLOQUE + 110, 350))
        self.pantalla.blit(texto, texto_rect)
        pygame.display.flip()
        pygame.time.wait(2000)

if __name__ == "__main__":
    juego = Tetris()
    juego.ejecutar()
    pygame.quit() 