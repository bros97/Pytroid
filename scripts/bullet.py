# scripts/bullet.py


import pygame
import math 

class Bullet:
    def __init__(self, x, y, direction, speed=8):
        self.base_width = 10
        self.base_height = 4
        self.rect = pygame.Rect(x, y, self.base_width, self.base_height)
        self.direction = direction
        self.speed = speed
        self.frame = 0  # Para la animación

    def update(self, walls):
        # Movimiento
        if self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed
        elif self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed

        # Colisión con paredes
        for wall in walls:
            if self.rect.colliderect(wall):
                return False

        # Fuera de pantalla
        if (self.rect.right < 0 or self.rect.left > 1200 or
            self.rect.bottom < 0 or self.rect.top > 600):
            return False

        self.frame += 1
        return True

    def draw(self, surface):
        # Animación: color parpadeante y tamaño pulsante
        pulse = 1 + 0.2 * math.sin(self.frame * 0.3)

        width = int(self.base_width * pulse)
        height = int(self.base_height * pulse)

        # Cambia el color entre amarillo y blanco
        if self.frame % 6 < 3:
            color = (255, 255, 0)  # amarillo
        else:
            color = (255, 255, 255)  # blanco

        # Centrar el rectángulo animado
        draw_rect = pygame.Rect(0, 0, width, height)
        draw_rect.center = self.rect.center

        pygame.draw.rect(surface, color, draw_rect)
