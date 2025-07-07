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

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pytroid")
clock = pygame.time.Clock()

font_big = pygame.font.SysFont("arial", 60, bold=True)
font_small = pygame.font.SysFont("arial", 30)

# Variables globales
game_won = False
game_started = False

# Crear jugador y enemigos
player = Player(1 * TILE_SIZE, 9 * TILE_SIZE)
enemies = [Enemy(28 * TILE_SIZE, 2 * TILE_SIZE)]

def get_collision_rects():
    rects = []
    for row_idx, row in enumerate(level_map):
        for col_idx, tile in enumerate(row):
            if tile == 1:
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE
                rects.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
    return rects

def show_menu():
    screen.fill((0, 0, 0))
    title = font_big.render("Pytroid", True, (255, 255, 255))
    prompt = font_small.render("Presiona ENTER para jugar", True, (200, 200, 200))
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))
    screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 300))
    pygame.display.flip()

def show_victory():
    victory = font_big.render("¡Has ganado!", True, (255, 255, 0))
    screen.blit(victory, (SCREEN_WIDTH // 2 - victory.get_width() // 2, SCREEN_HEIGHT // 2 - victory.get_height() // 2))

def main():
    global game_started, game_won
    running = True

    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if not game_started:
            show_menu()
            if keys[pygame.K_RETURN]:
                game_started = True
            continue

        walls = get_collision_rects()
        player.update(walls)

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

        if game_won:
            show_victory()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
