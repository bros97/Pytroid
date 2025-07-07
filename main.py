# main.py


import pygame
import sys
from scripts.player import Player
from scripts.level import draw_level, level_map, TILE_SIZE
from scripts.enemy import Enemy

# Inicializar Pygame
pygame.init()

# Constantes
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
FPS = 60

# Crear ventana
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Metroid Clone")
clock = pygame.time.Clock()

# Crear jugador
player = Player(1 * TILE_SIZE, 9 * TILE_SIZE)


# Crear enemigos
enemies = [
    Enemy(8 * TILE_SIZE, 3 * TILE_SIZE),   # (col=6, fila=3) = (240, 120)
    Enemy(12 * TILE_SIZE, 3 * TILE_SIZE),
    Enemy(28 * TILE_SIZE, 2 * TILE_SIZE)

]


# Obtener colisiones desde el mapa
def get_collision_rects():
    rects = []
    for row_idx, row in enumerate(level_map):
        for col_idx, tile in enumerate(row):
            if tile == 1:
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE
                rects.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
    return rects

# Bucle principal
def main():
    running = True
    while running:
        screen.fill((0, 0, 0))  # fondo negro

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Obtener paredes
        walls = get_collision_rects()

        # Actualizar jugador
        player.update(walls)

        # Actualizar y manejar colisiones de balas
        for bullet in player.bullets[:]:  # Copia segura
            if not bullet.update(walls):
                player.bullets.remove(bullet)
                continue

            for enemy in enemies:
                if enemy.alive and bullet.rect.colliderect(enemy.rect):
                    enemy.alive = False
                    if bullet in player.bullets:
                        player.bullets.remove(bullet)
                    break

        # Dibujar elementos del juego
        draw_level(screen)
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
