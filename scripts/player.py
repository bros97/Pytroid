# Nombre: Maylon Javier Polanco
# Matrícula: 15-EISN-2-004

import pygame
from scripts.bullet import Bullet
import os

class Player:
    def __init__(self, x, y):
        self.width = 30
        self.height = 40
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.velocity_y = 0
        self.speed = 4
        self.gravity = 0.8
        self.jump_strength = -12
        self.on_ground = False
        self.spawn_point = (x, y)
        self.bullets = []
        self.cooldown = 0

        # Animaciones
        self.run_right_images = [
            pygame.image.load(os.path.join("assets", "images", "runr1.png")).convert_alpha(),
            pygame.image.load(os.path.join("assets", "images", "runr2.png")).convert_alpha(),
            pygame.image.load(os.path.join("assets", "images", "runr3.png")).convert_alpha()
        ]
        self.run_left_images = [
            pygame.image.load(os.path.join("assets", "images", "runl1.png")).convert_alpha(),
            pygame.image.load(os.path.join("assets", "images", "runl2.png")).convert_alpha(),
            pygame.image.load(os.path.join("assets", "images", "runl3.png")).convert_alpha()
        ]
        self.jump_right = pygame.image.load(os.path.join("assets", "images", "jumpR.png")).convert_alpha()
        self.jump_left = pygame.image.load(os.path.join("assets", "images", "jumpL.png")).convert_alpha()
        self.current_frame = 0
        self.frame_counter = 0
        self.facing_right = True

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
            self.facing_right = True
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
        bullet = Bullet(self.rect.centerx, self.rect.centery, 1 if self.facing_right else -1)
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

        # Animación correr
        if dx != 0 and self.on_ground:
            self.frame_counter += 1
            if self.frame_counter >= 6:
                self.current_frame = (self.current_frame + 1) % 3
                self.frame_counter = 0
        elif self.on_ground:
            self.current_frame = 0

    def draw(self, surface):
        if self.on_ground:
            if self.facing_right:
                image = self.run_right_images[self.current_frame]
            else:
                image = self.run_left_images[self.current_frame]
        else:
            image = self.jump_right if self.facing_right else self.jump_left

        surface.blit(image, self.rect.topleft)

        for bullet in self.bullets:
            bullet.draw(surface)

    def reset(self):
        self.rect.topleft = self.spawn_point
        self.velocity_y = 0
        self.bullets.clear()
        self.cooldown = 0
        self.current_frame = 0
        self.frame_counter = 0
