# scripts/enemy_smart.py
# Enemigo inteligente con A* básico
import pygame
from scripts.pathfinding import a_star
from scripts.level import level_map, TILE_SIZE

class EnemySmart:
    def __init__(self, x, y):
        self.width = 30
        self.height = 40
        self.color = (0, 255, 100)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.speed = 2
        self.path = []
        self.path_index = 0
        self.gravity = 0.8
        self.velocity_y = 0
        self.on_ground = False
        self.jump_power = -10
        self.alive = True
        self.respawn_timer = 0
        self.spawn_point = (x, y)

    def get_grid_pos(self):
        col = self.rect.centerx // TILE_SIZE
        row = self.rect.centery // TILE_SIZE
        return (row, col)

    def apply_gravity(self, walls):
        self.velocity_y += self.gravity
        if self.velocity_y > 10:
            self.velocity_y = 10

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

    def follow_path(self, walls):
        if self.path and self.path_index < len(self.path):
            target_row, target_col = self.path[self.path_index]
            target_x = target_col * TILE_SIZE + TILE_SIZE // 2
            target_y = target_row * TILE_SIZE + TILE_SIZE // 2

            dx = target_x - self.rect.centerx
            dy = target_y - self.rect.centery

            if abs(dx) > 5:
                self.rect.x += self.speed if dx > 0 else -self.speed
            if dy < -10 and self.on_ground:
                self.velocity_y = self.jump_power
                self.on_ground = False

            # avanzar al siguiente nodo si ya se alcanzó el actual
            if abs(dx) < 5 and abs(dy) < 10:
                self.path_index += 1

            for wall in walls:
                if self.rect.colliderect(wall):
                    if dx > 0:
                        self.rect.right = wall.left
                    elif dx < 0:
                        self.rect.left = wall.right

    def update(self, player, walls):
        if not self.alive:
            self.respawn_timer += 1
            if self.respawn_timer > 180:  # 3 segundos
                self.rect.topleft = self.spawn_point
                self.alive = True
                self.respawn_timer = 0
            return

        self.apply_gravity(walls)

        start = self.get_grid_pos()
        end = (player.rect.centery // TILE_SIZE, player.rect.centerx // TILE_SIZE)

        if not self.path or self.path_index >= len(self.path):
            self.path = a_star(level_map, start, end)
            self.path_index = 0

        self.follow_path(walls)

    def draw(self, surface):
        if self.alive:
            pygame.draw.rect(surface, self.color, self.rect)


