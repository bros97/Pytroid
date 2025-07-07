import pygame
from scripts.enemy_bullet import EnemyBullet

class Enemy:
    def __init__(self, x, y):
        self.width = 30
        self.height = 40
        self.color = (0, 200, 255)  # azul celeste
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.alive = True
        self.shoot_timer = 0
        self.bullets = []

    def update(self, walls):
        if not self.alive:
            return

        # Disparo automático cada 120 frames
        self.shoot_timer += 1
        if self.shoot_timer >= 120:
            bullet = EnemyBullet(self.rect.centerx, self.rect.centery)
            self.bullets.append(bullet)
            self.shoot_timer = 0

        # Actualizar balas
        for bullet in self.bullets[:]:
            if not bullet.update(walls):
                self.bullets.remove(bullet)

    def draw(self, surface):
        if self.alive:
            pygame.draw.rect(surface, self.color, self.rect)
            for bullet in self.bullets:
                bullet.draw(surface)
