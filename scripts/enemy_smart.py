# scripts/enemy_smart.py
# Enemigo inteligente con A* básico


import pygame
from scripts.pathfinding import a_star
from scripts.level import level_map, TILE_SIZE

class EnemySmart:
    def __init__(self, x, y):
        self.width = 30
        self.height = 40
        self.color = (255, 100, 0)  # naranja
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.alive = True
        self.speed = 2
        self.path = []
        self.path_index = 0
        self.recalc_timer = 0

    def get_tile_pos(self, rect):
        return (rect.centerx // TILE_SIZE, rect.centery // TILE_SIZE)

    def update(self, player, walls):
        if not self.alive:
            return

        # Calcular camino cada 60 frames
        self.recalc_timer -= 1
        if self.recalc_timer <= 0:
            start = self.get_tile_pos(self.rect)
            goal = self.get_tile_pos(player.rect)
            self.path = a_star(start, goal, level_map)
            self.path_index = 0
            self.recalc_timer = 60

        # Mover al siguiente tile en el camino
        if self.path and self.path_index < len(self.path):
            target_tile = self.path[self.path_index]
            target_pos = (target_tile[0] * TILE_SIZE + TILE_SIZE // 2,
                          target_tile[1] * TILE_SIZE + TILE_SIZE // 2)

            dx = target_pos[0] - self.rect.centerx
            dy = target_pos[1] - self.rect.centery
            dist = (dx**2 + dy**2) ** 0.5

            if dist < 3:
                self.path_index += 1
            else:
                move_x = self.speed * dx / dist
                move_y = self.speed * dy / dist
                self.rect.x += int(move_x)
                self.rect.y += int(move_y)

    def draw(self, surface):
        if self.alive:
            pygame.draw.rect(surface, self.color, self.rect)
