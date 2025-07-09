# Nombre: Maylon Javier Polanco
# Matrícula: 15-EISN-2-004

import pygame
import random
from scripts.bullet import Bullet
from scripts.behavior_tree import Selector, Sequence, Condition, Action

class EnemyBoss:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 60)
        self.spawn_point = (x, y)
        self.velocity_y = 0
        self.gravity = 0.8
        self.speed = 2
        self.direction = 1  # 1: derecha, -1: izquierda
        self.patrol_range = 200
        self.start_x = x
        self.shoot_timer = 0
        self.bullets = []
        self.alive = True
        self.current_walls = []
        self.tree = self.create_behavior_tree()

    def apply_gravity(self, walls):
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        for wall in walls:
            if self.rect.colliderect(wall):
                if self.velocity_y > 0:
                    self.rect.bottom = wall.top
                    self.velocity_y = 0
                elif self.velocity_y < 0:
                    self.rect.top = wall.bottom
                    self.velocity_y = 0

    def patrol(self, walls):
        self.rect.x += self.speed * self.direction
        if abs(self.rect.x - self.start_x) >= self.patrol_range:
            self.direction *= -1
        for wall in walls:
            if self.rect.colliderect(wall):
                self.rect.x -= self.speed * self.direction
                self.direction *= -1
                break

    def shoot(self):
        if self.shoot_timer <= 0:
            bullet = Bullet(self.rect.centerx, self.rect.centery, -1 if self.direction == -1 else 1)
            self.bullets.append(bullet)
            self.shoot_timer = 60
        else:
            self.shoot_timer -= 1

    def create_behavior_tree(self):
        def is_player_near(boss, player):
            return boss.rect.x - 200 < player.rect.x < boss.rect.x + 200

        def shoot_action(boss, player):
            boss.shoot()

        def patrol_action(boss, player):
            boss.patrol(boss.current_walls)

        return Selector([
            Sequence([
                Condition(is_player_near),
                Action(shoot_action)
            ]),
            Action(patrol_action)
        ])

    def update(self, player, walls):
        if not self.alive:
            return

        self.current_walls = walls
        self.apply_gravity(walls)
        self.tree.run(self, player)

        for bullet in self.bullets:
            bullet.update(walls)

        self.bullets = [b for b in self.bullets if b.active]

    def draw(self, surface):
        if self.alive:
            pygame.draw.rect(surface, (255, 100, 100), self.rect)
            for bullet in self.bullets:
                bullet.draw(surface)

    def reset(self):
        self.rect.topleft = self.spawn_point
        self.velocity_y = 0
        self.bullets.clear()
        self.shoot_timer = 0
        self.alive = True
