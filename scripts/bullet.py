import pygame
import math

class Bullet:
    def __init__(self, x, y, direction):
        self.radius = 5
        self.speed = 10
        self.color = (255, 255, 0)  # amarillo
        self.direction = direction
        self.rect = pygame.Rect(x, y, self.radius * 2, self.radius * 2)
        self.rect.center = (x, y)
        self.frame = 0  # para animación tipo pulso

    def update(self, walls):
        if self.direction == "right":
            self.rect.x += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed

        # Colisión con pared
        for wall in walls:
            if self.rect.colliderect(wall):
                return False  # destruir bala

        self.frame += 1
        return True

    def draw(self, surface):
        pulse = 1 + 0.2 * math.sin(self.frame * 0.3)
        r = int(self.radius * pulse)
        pygame.draw.circle(surface, self.color, self.rect.center, r)
