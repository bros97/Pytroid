
import pygame

class EnemyBullet:
    def __init__(self, x, y):
        self.radius = 5
        self.color = (255, 0, 0)  # rojo
        self.speed = 6
        self.rect = pygame.Rect(x, y, self.radius * 2, self.radius * 2)
        self.rect.center = (x, y)

    def update(self, walls):
        self.rect.x -= self.speed  # se mueve a la izquierda

        # Destruir si choca con una pared
        for wall in walls:
            if self.rect.colliderect(wall):
                return False

        return True

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.rect.center, self.radius)
