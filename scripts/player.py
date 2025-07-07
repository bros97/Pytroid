# Nombre: Maylon Javier Polanco
# Matrícula: 15-EISN-2-004

import pygame
from scripts.bullet import Bullet

class Player:
    def __init__(self, x, y):
        self.width = 30
        self.height = 40
        self.color = (0, 255, 0)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.velocity_y = 0
        self.speed = 4
        self.gravity = 0.8
        self.jump_strength = -12
        self.on_ground = False
        self.spawn_point = (x, y)
        self.bullets = []
        self.cooldown = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.velocity_y = self.jump_strength
        if keys[pygame.K_SPACE] and self.cooldown == 0:
            self.shoot()
            self.cooldown = 20
        return dx

    def apply_gravity(self, walls):
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        self.on_ground = False
        for wall in walls:
            if self.rect.colliderect(wall):
                if self.velocity_y > 0:
                    self.rect.bottom = wall.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:
                    self.rect.top = wall.bottom
                    self.velocity_y = 0

    def move(self, dx, walls):
        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall):
                if dx > 0:
                    self.rect.right = wall.left
                elif dx < 0:
                    self.rect.left = wall.right

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery, 1 if self.rect.centerx < 400 else -1)
        self.bullets.append(bullet)

    def update(self, walls):
        dx = self.handle_input()
        self.move(dx, walls)
        self.apply_gravity(walls)
        if self.cooldown > 0:
            self.cooldown -= 1
        for bullet in self.bullets:
            bullet.update(walls)
        self.bullets = [b for b in self.bullets if b.active]

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        for bullet in self.bullets:
            bullet.draw(surface)

    def reset(self):
        self.rect.topleft = self.spawn_point
        self.velocity_y = 0
        self.bullets.clear()
        self.cooldown = 0
