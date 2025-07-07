# Nombre: Maylon Javier Polanco
# Matrícula: 15-EISN-2-004

import pygame
import random
from scripts.bullet import Bullet

class EnemyBoss:
    def __init__(self, x, y):
        self.width = 40
        self.height = 50
        self.color = (255, 0, 255)  # morado
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.spawn_point = (x, y)
        self.speed = 2
        self.gravity = 0.8
        self.vel_y = 0
        self.on_ground = False
        self.direction = 1
        self.state = "idle"  # idle, chase, attack
        self.shoot_cooldown = 0
        self.bullets = []
        self.alive = True

    def reset(self):
        self.rect.topleft = self.spawn_point
        self.vel_y = 0
        self.on_ground = False
        self.state = "idle"
        self.bullets.clear()
        self.alive = True

    def apply_gravity(self, walls):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y
        self.on_ground = False
        for wall in walls:
            if self.rect.colliderect(wall):
                if self.vel_y > 0:
                    self.rect.bottom = wall.top
                    self.on_ground = True
                    self.vel_y = 0

    def update(self, player, walls):
        if not self.alive:
            return

        self.apply_gravity(walls)

        distance = self.rect.centerx - player.rect.centerx

        # Árbol de comportamiento simple
        if abs(distance) > 300:
            self.state = "idle"
        elif abs(distance) > 100:
            self.state = "chase"
        else:
            self.state = "attack"

        if self.state == "chase":
            self.direction = -1 if distance > 0 else 1
            self.rect.x += self.speed * self.direction

        elif self.state == "attack":
            if self.shoot_cooldown == 0:
                bullet = Bullet(self.rect.centerx, self.rect.centery, -1 if distance > 0 else 1)
                self.bullets.append(bullet)
                self.shoot_cooldown = 60

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        for bullet in self.bullets[:]:
            if bullet.update(walls):
                pass
            else:
                self.bullets.remove(bullet)

    def draw(self, surface):
        if self.alive:
            pygame.draw.rect(surface, self.color, self.rect)
        for bullet in self.bullets:
            bullet.draw(surface)
