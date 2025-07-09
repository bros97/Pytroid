# Nombre: Maylon Javier Polanco
# Matrícula: 15-EISN-2-004

import pygame
import os
from scripts.pathfinding import a_star
from scripts.level import level_map, TILE_SIZE

class Enemy:
    def __init__(self, x, y, color=(255, 0, 0), is_boss=False):
        self.rect = pygame.Rect(x, y, 30, 40)
        self.spawn_point = (x, y)
        self.velocity_y = 0
        self.gravity = 0.8
        self.jump_strength = -12
        self.speed = 2
        self.color = color

        self.images_right = [
            pygame.image.load(os.path.join("assets", "images", "zedr1.png")).convert_alpha(),
            pygame.image.load(os.path.join("assets", "images", "zedr2.png")).convert_alpha()
        ]
        self.images_left = [
            pygame.image.load(os.path.join("assets", "images", "zedl1.png")).convert_alpha(),
            pygame.image.load(os.path.join("assets", "images", "zedl2.png")).convert_alpha()
        ]
        self.current_frame = 0
        self.frame_counter = 0
        self.facing_right = True
        self.path = []
        self.path_index = 0
        self.alive = True
        self.is_boss = is_boss
        self.respawn_timer = 0
        self.on_ground = False
        self.last_player_pos = None

    def reset(self):
        self.rect.topleft = self.spawn_point
        self.velocity_y = 0
        self.alive = True
        self.path.clear()
        self.path_index = 0
        self.respawn_timer = 0
        self.last_player_pos = None

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

    def move_to_player(self, player, walls):
        start = (self.rect.centerx // TILE_SIZE, self.rect.centery // TILE_SIZE)
        end = (player.rect.centerx // TILE_SIZE, player.rect.centery // TILE_SIZE)

        # Solo recalcular si el jugador se ha movido o no hay camino
        if self.last_player_pos != end or not self.path:
            self.path = a_star(start, end, level_map)
            self.path_index = 0
            self.last_player_pos = end

        if self.path and self.path_index < len(self.path):
            target = self.path[self.path_index]
            tx, ty = target[0] * TILE_SIZE + TILE_SIZE // 2, target[1] * TILE_SIZE + TILE_SIZE // 2

            dx = tx - self.rect.centerx
            dy = ty - self.rect.centery

            if abs(dx) > 4:
                self.rect.x += self.speed if dx > 0 else -self.speed
            if abs(dy) > 4:
                self.rect.y += self.speed if dy > 0 else -self.speed

            # Si hay una pared enfrente y está en el suelo, intentar saltar
            if self.on_ground:
                future_rect = self.rect.move(self.speed if dx > 0 else -self.speed, 0)
                if any(future_rect.colliderect(w) for w in walls):
                    self.velocity_y = self.jump_strength

            # Avanzar al siguiente punto si está cerca

        # Actualizar dirección y animación
        if dx > 0:
            self.facing_right = True
        elif dx < 0:
            self.facing_right = False

        if abs(dx) > 0 or abs(dy) > 0:
            self.frame_counter += 1
            if self.frame_counter >= 10:
                self.current_frame = (self.current_frame + 1) % 2
                self.frame_counter = 0
        else:
            self.current_frame = 0
            if abs(dx) < 4 and abs(dy) < 4:
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
            image = self.images_right[self.current_frame] if self.facing_right else self.images_left[self.current_frame]
            surface.blit(image, self.rect.topleft)
        