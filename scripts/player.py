import pygame
from scripts.bullet import Bullet

class Player:
    def __init__(self, x=100, y=100):
        self.width = 30
        self.height = 40
        self.color = (255, 100, 100)  # rojo claro
        self.speed = 4
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.bullets = []
        self.shoot_cooldown = 0
        self.direction = "right"

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
            self.direction = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
            self.direction = "right"
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.speed
            self.direction = "up"
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.speed
            self.direction = "down"

        return dx, dy

    def move(self, dx, dy, walls):
        # Movimiento horizontal
        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall):
                if dx > 0:
                    self.rect.right = wall.left
                elif dx < 0:
                    self.rect.left = wall.right

        # Movimiento vertical
        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall):
                if dy > 0:
                    self.rect.bottom = wall.top
                elif dy < 0:
                    self.rect.top = wall.bottom

    def shoot(self):
        if self.shoot_cooldown == 0:
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction)
            self.bullets.append(bullet)
            self.shoot_cooldown = 15  # frames entre disparos

    def update(self, walls):
        dx, dy = self.handle_input()
        self.move(dx, dy, walls)

        # Disparo con tecla J
        keys = pygame.key.get_pressed()
        if keys[pygame.K_j]:
            self.shoot()

        # Actualizar balas
        self.bullets = [b for b in self.bullets if b.update(walls)]

        # Enfriamiento
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        for bullet in self.bullets:
            bullet.draw(surface)
