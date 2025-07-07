# main.py
# Autor: Sharenny Reyes
# Matrícula: [Tu matrícula]

import pygame
import sys
from scripts.player import Player
from scripts.level import draw_level, level_map, TILE_SIZE
from scripts.enemy import Enemy

# Inicializar Pygame
pygame.init()

# Tamaño de ventana
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Metroid Lineal")
clock = pygame.time.Clock()

# Crear jugador
player = Player(1 * TILE_SIZE, 9 * TILE_SIZE)

# Enemigo final
enemies = [
    Enemy(28 * TILE_SIZE, 2 * TILE_SIZE)
]

# Variable de victoria
game_won = False

# Obtener colisiones del mapa
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
    global game_won
    running = True
    while running:
        screen.fill((0, 0, 0))

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Obtener paredes
        walls = get_collision_rects()

        # Actualizar jugador
        player.update(walls)

        # Balas y enemigos
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

        # Verificar victoria
        if not game_won:
            final_enemy = enemies[0]
            if not final_enemy.alive:
                distance = abs(player.rect.centerx - final_enemy.rect.centerx)
                vertical = abs(player.rect.centery - final_enemy.rect.centery)
                if distance < 60 and vertical < 60:
                    game_won = True

        # Dibujar elementos
        draw_level(screen)
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)

        # Mostrar texto de victoria
        if game_won:
            font = pygame.font.SysFont("arial", 60, bold=True)
            text = font.render("¡Has ganado!", True, (255, 255, 0))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

        # Actualizar pantalla
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
