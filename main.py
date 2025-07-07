# Nombre: Maylon Javier Polanco
# Matrícula: 15-EISN-2-004

import pygame
import sys
from scripts.player import Player
from scripts.enemy import Enemy
from scripts.enemy_boss import EnemyBoss
from scripts.bullet import Bullet
from scripts.level import draw_level, level_map, TILE_SIZE
from scripts.pathfinding import a_star

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pytroid")
clock = pygame.time.Clock()

# Estados del juego
STATE_INTRO = "intro"
STATE_PLAYING = "playing"
STATE_VICTORY = "victory"

# Inicializar entidades
player = Player(60, 60)

enemies = [
    Enemy(300, 100),
    Enemy(600, 100),
    Enemy(900, 100)
]

boss = EnemyBoss(1140, 100)

font = pygame.font.SysFont(None, 48)

def get_collision_rects():
    rects = []
    for row_idx, row in enumerate(level_map):
        for col_idx, tile in enumerate(row):
            if tile == 1:
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE
                rects.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
    return rects

def reset():
    player.reset()
    for e in enemies:
        e.reset()
    boss.reset()

def main():
    state = STATE_INTRO
    running = True

    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if state == STATE_INTRO:
            text = font.render("Presiona ENTER para comenzar", True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2))
            if keys[pygame.K_RETURN]:
                state = STATE_PLAYING
                reset()

        elif state == STATE_PLAYING:
            walls = get_collision_rects()

            player.update(walls)
            for enemy in enemies:
                enemy.update(player, walls)
            boss.update(player, walls)

            for bullet in player.bullets[:]:
                if bullet.update(walls):
                    for enemy in enemies + [boss]:
                        if enemy.alive and bullet.rect.colliderect(enemy.rect):
                            enemy.alive = False
                            player.bullets.remove(bullet)
                            if enemy == boss:
                                state = STATE_VICTORY
                            break
                else:
                    player.bullets.remove(bullet)

            draw_level(screen)
            player.draw(screen)
            for enemy in enemies:
                enemy.draw(screen)
            boss.draw(screen)

        elif state == STATE_VICTORY:
            text = font.render("Felicidades, has vencido al jefe final!", True, (0, 255, 0))
            screen.blit(text, (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2))
            text2 = font.render("Presiona R para reiniciar", True, (255, 255, 255))
            screen.blit(text2, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 50))
            if keys[pygame.K_r]:
                state = STATE_INTRO

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
