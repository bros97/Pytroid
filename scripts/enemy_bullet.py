# scripts/enemy_bullet.py

import pygame

class EnemyBullet:
    def __init__(self, x, y, direction, speed=5):
        self.rect = pygame.Rect(x, y, 10, 4)
        self.direction = direction
        self.speed = speed
        self.color = (255, 0, 0)

    def update(self, walls):
        if self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed

        # Colisión con paredes o fuera de pantalla
        for wall in walls:
            if self.rect.colliderect(wall):
                return False
        if self.rect.right < 0 or self.rect.left > 1200:
            return False
        return True

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
