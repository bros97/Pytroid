# Nombre: Maylon Javier Polanco
# Matrícula: 15-EISN-2-004

import pygame
import sys
from scripts.player import Player
from scripts.enemy import Enemy
from scripts.level import draw_level, get_collision_rects

pygame.init()

# Constantes
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Inicialización
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pytroid")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

# Estado del juego
START_SCREEN = True
GAME_OVER = False
VICTORY = False

# Instancias
player = Player(60, 60)

enemies = [
    Enemy(300, 100),
    Enemy(500, 200),
    Enemy(700, 100)
]

final_boss = Enemy(700, 300, color=(255, 0, 0), is_boss=True)

def reset():
    global GAME_OVER, VICTORY, START_SCREEN
    player.reset()
    for e in enemies + [final_boss]:
        e.reset()
    GAME_OVER = False
    VICTORY = False
    START_SCREEN = True

def main():
    global START_SCREEN, GAME_OVER, VICTORY
    while True:
        screen.fill(BLACK)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if START_SCREEN:
            text = font.render("Presione ENTER para iniciar", True, WHITE)
            screen.blit(text, (180, 250))
            if keys[pygame.K_RETURN]:
                START_SCREEN = False
            pygame.display.flip()
            clock.tick(FPS)
            continue

        if GAME_OVER:
            text = font.render("Game Over - R para reiniciar", True, (255, 0, 0))
            screen.blit(text, (180, 250))
            if keys[pygame.K_r]:
                reset()
            pygame.display.flip()
            clock.tick(FPS)
            continue

        if VICTORY:
            text = font.render("Felicidades, has ganado! - R para reiniciar", True, (0, 255, 0))
            screen.blit(text, (80, 250))
            if keys[pygame.K_r]:
                reset()
            pygame.display.flip()
            clock.tick(FPS)
            continue

        walls = get_collision_rects()
        player.update(walls)

        for e in enemies:
            e.update(player, walls)
        final_boss.update(player, walls)

        # Verificar colisiones con enemigos
        for e in enemies:
            if e.alive and player.rect.colliderect(e.rect):
                GAME_OVER = True

        if final_boss.alive and player.rect.colliderect(final_boss.rect):
            GAME_OVER = True

        for bullet in player.bullets:
            for e in enemies:
                if e.alive and bullet.rect.colliderect(e.rect):
                    e.alive = False
            if final_boss.alive and bullet.rect.colliderect(final_boss.rect):
                final_boss.alive = False
                VICTORY = True

        draw_level(screen)
        player.draw(screen)

        for e in enemies:
            e.draw(screen)
        final_boss.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
