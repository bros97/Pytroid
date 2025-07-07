# main.py


import pygame
import sys
from scripts.player import Player
from scripts.level import draw_level, level_map, TILE_SIZE
from scripts.enemy import Enemy
from scripts.enemy_smart import EnemySmart
from scripts.enemy_bullet import EnemyBullet

# Inicialización
pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Metroid Lineal")
clock = pygame.time.Clock()

font_big = pygame.font.SysFont("arial", 60, bold=True)
font_small = pygame.font.SysFont("arial", 30)

# Variables globales
game_won = False
game_started = False
player_lost = False

# Instancias
def create_game():
    global player, enemies
    player = Player(1 * TILE_SIZE, 9 * TILE_SIZE)
    enemies = [
        EnemySmart(10 * TILE_SIZE, 9 * TILE_SIZE),
        EnemySmart(20 * TILE_SIZE, 3 * TILE_SIZE),
        EnemySmart(5 * TILE_SIZE, 6 * TILE_SIZE),
        Enemy(28 * TILE_SIZE, 2 * TILE_SIZE)  # Enemigo final
    ]

create_game()

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
    title = font_big.render("Metroid Lineal", True, (255, 255, 255))
    prompt = font_small.render("Presiona ENTER para jugar", True, (200, 200, 200))
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))
    screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 300))
    pygame.display.flip()

def show_victory():
    text = font_big.render("¡Has ganado!", True, (255, 255, 0))
    retry = font_small.render("Presiona R para reiniciar", True, (200, 200, 200))
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 160))
    screen.blit(retry, (SCREEN_WIDTH // 2 - retry.get_width() // 2, 260))

def show_game_over():
    text = font_big.render("¡Has perdido!", True, (255, 50, 50))
    retry = font_small.render("Presiona R para reiniciar", True, (200, 200, 200))
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 160))
    screen.blit(retry, (SCREEN_WIDTH // 2 - retry.get_width() // 2, 260))

def reset_game():
    global game_started, game_won, player_lost
    create_game()
    game_started = False
    game_won = False
    player_lost = False

# Bucle principal
def main():
    global game_started, game_won, player_lost
    running = True

    while running:
        screen.fill((0, 0, 0))
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_started:
            show_menu()
            if keys[pygame.K_RETURN]:
                game_started = True
            pygame.display.flip()
            continue

        walls = get_collision_rects()
        player.update(walls)

        if player.rect.top > SCREEN_HEIGHT:
            player_lost = True

        for enemy in enemies:
            if isinstance(enemy, EnemySmart):
                enemy.update(player, walls)
            elif isinstance(enemy, Enemy):
                enemy.update(walls)

            if hasattr(enemy, "bullets"):
                for bullet in enemy.bullets:
                    if bullet.rect.colliderect(player.rect):
                        player_lost = True

        # Colisión entre balas del jugador y enemigos
        for bullet in player.bullets[:]:
            for enemy in enemies:
                if enemy.alive and bullet.rect.colliderect(enemy.rect):
                    enemy.alive = False
                    if bullet in player.bullets:
                        player.bullets.remove(bullet)
                    break

        # Victoria si último enemigo muerto y el jugador está cerca
        final_enemy = enemies[-1]
        if not game_won and not final_enemy.alive:
            dx = abs(player.rect.centerx - final_enemy.rect.centerx)
            dy = abs(player.rect.centery - final_enemy.rect.centery)
            if dx < 60 and dy < 60:
                game_won = True

        # Dibujo
        draw_level(screen)
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)

        # Pantallas de fin
        if game_won:
            show_victory()
            if keys[pygame.K_r]:
                reset_game()
            pygame.display.flip()
            continue

        if player_lost:
            show_game_over()
            if keys[pygame.K_r]:
                reset_game()
            pygame.display.flip()
            continue

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
