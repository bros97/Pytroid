# scripts/player.py
# Autor: Sharenny Reyes
# Matrícula: [Tu matrícula]

import pygame
from scripts.bullet import Bullet

class Player:
    def __init__(self, x=100, y=100):
        self.width = 30
        self.height = 40
        self.color = (255, 100, 100)
        self.speed = 4
        self.jump_force = 12
        self.gravity = 0.8
        self.vel_y = 0
        self.on_ground = False

        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.bullets = []
        self.shoot_cooldown = 0
        self.direction = "right"

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
            self.direction = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
            self.direction = "right"
        if (keys[pygame.K_k] or keys[pygame.K_SPACE]) and self.on_ground:
            self.vel_y = -self.jump_force
            self.on_ground = False

        return dx

    def move(self, dx, walls):
        # Movimiento horizontal
        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall):
                if dx > 0:
                    self.rect.right = wall.left
                elif dx < 0:
                    self.rect.left = wall.right

        # Movimiento vertical (gravedad)
        self.vel_y += self.gravity
        if self.vel_y > 10:
            self.vel_y = 10
        self.rect.y += self.vel_y

        # Colisiones verticales
        self.on_ground = False
        for wall in walls:
            if self.rect.colliderect(wall):
                if self.vel_y > 0:
                    self.rect.bottom = wall.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = wall.bottom
                    self.vel_y = 0

    def shoot(self):
        if self.shoot_cooldown == 0:
            if self.direction == "right":
                bullet_x = self.rect.right + 1
                bullet_y = self.rect.centery
            elif self.direction == "left":
                bullet_x = self.rect.left - 11
                bullet_y = self.rect.centery
            elif self.direction == "up":
                bullet_x = self.rect.centerx
                bullet_y = self.rect.top - 11
            elif self.direction == "down":
                bullet_x = self.rect.centerx
                bullet_y = self.rect.bottom + 1

            bullet = Bullet(bullet_x, bullet_y, self.direction)
            self.bullets.append(bullet)
            self.shoot_cooldown = 15

    def update(self, walls):
        dx = self.handle_input()
        self.move(dx, walls)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_j]:
            self.shoot()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        for bullet in self.bullets:
            bullet.draw(surface)
