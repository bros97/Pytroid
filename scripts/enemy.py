# Nombre: Maylon Javier Polanco
# Matrícula: 15-EISN-2-004

import pygame
from scripts.pathfinding import a_star
from scripts.level import level_map, TILE_SIZE

class Enemy:
    def __init__(self, x, y, color=(255, 0, 0), is_boss=False):
        self.rect = pygame.Rect(x, y, 30, 40)
        self.spawn_point = (x, y)
        self.velocity_y = 0
        self.gravity = 0.8
        self.speed = 2
        self.color = color
        self.path = []
        self.path_index = 0
        self.alive = True
        self.is_boss = is_boss
        self.respawn_timer = 0

    def reset(self):
        self.rect.topleft = self.spawn_point
        self.velocity_y = 0
        self.alive = True
        self.path.clear()
        self.path_index = 0
        self.respawn_timer = 0

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

    def move_to_player(self, player, walls):
        start = (self.rect.centerx // TILE_SIZE, self.rect.centery // TILE_SIZE)
        end = (player.rect.centerx // TILE_SIZE, player.rect.centery // TILE_SIZE)
        self.path = a_star(start, end, level_map)
        if self.path:
            self.path_index = 0

        if self.path and self.path_index < len(self.path):
            target = self.path[self.path_index]
            tx, ty = target[0] * TILE_SIZE, target[1] * TILE_SIZE
            if self.rect.centerx < tx:
                self.rect.x += self.speed
            elif self.rect.centerx > tx:
                self.rect.x -= self.speed

            if self.rect.collidepoint(tx, ty):
                self.path_index += 1

    def update(self, player, walls):
        if not self.alive:
            self.respawn_timer += 1
            if self.respawn_timer >= 600:
                self.reset()
            return

        self.move_to_player(player, walls)
        self.apply_gravity(walls)

    def draw(self, surface):
        if self.alive:
            pygame.draw.rect(surface, self.color, self.rect)
