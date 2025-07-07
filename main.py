# main.py


import pygame
import sys
from scripts.player import Player
from scripts.level import draw_level, level_map, TILE_SIZE
from scripts.enemy import Enemy

# Inicializar Pygame
pygame.init()

# Tamaño de pantalla para mostrar más mapa horizontal
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Metroid Lineal")
clock = pygame.time.Clock()

# Crear jugador al inicio del nivel
player = Player(1 * TILE_SIZE, 9 * TILE_SIZE)

# Enemigo final al final del nivel
enemies = [
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

def main():
    running = True
    while running:
        screen.fill((0, 0, 0))

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Lógica
        walls = get_collision_rects()
        player.update(walls)

        # Actualizar y manejar balas vs enemigos
        for bullet in player.bullets[:]:
            if not bullet.update(walls):
                player.bullets.remove(bullet)
                continue

            for enemy in enemies:
                if enemy.alive and bullet.rect.colliderect(enemy.rect):
                    enemy.alive = False
                    if bullet in player.bullets:
                        player.bullets.remove(bullet)
                    break

        # Dibujar
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
