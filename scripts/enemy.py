# scripts/enemy.py
# Autor: Sharenny Reyes
# Matrícula: [Tu matrícula]

import pygame

class Enemy:
    def __init__(self, x, y):
        self.width = 30
        self.height = 40
        self.color = (200, 0, 0)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.alive = True

    def update(self):
        pass  # Luego aquí puedes añadir comportamiento con IA

    def draw(self, surface):
        if self.alive:
            pygame.draw.rect(surface, self.color, self.rect)
