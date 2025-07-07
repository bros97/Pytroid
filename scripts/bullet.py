# Nombre: Maylon Javier Polanco
# Matrícula: 15-EISN-2-004

import pygame

class Bullet:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 10, 5)
        self.speed = 8 * direction  # dirección puede ser 1 o -1
        self.color = (255, 255, 0)
        self.active = True

    def update(self, walls):
        self.rect.x += self.speed

        for wall in walls:
            if self.rect.colliderect(wall):
                self.active = False
                break

        return self.active

    def draw(self, surface):
        if self.active:
            pygame.draw.rect(surface, self.color, self.rect)
