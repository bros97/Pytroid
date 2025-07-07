# scripts/level.py
import pygame

# Tamaño de cada tile
TILE_SIZE = 40

# Mapa del nivel: 0 = vacío, 1 = pared/suelo
level_map = [
    [1]*20,
    [1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,0,1,0,1,1,0,1,0,1,1,1,0,0,1],
    [1,0,0,0,0,0,1,1,0,0,0,0,1,0,0,0,1,1,0,1],
    [1,0,1,1,0,1,0,0,0,1,1,1,1,1,1,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1],
    [1]*20,
]

def draw_level(surface):
    for row_index, row in enumerate(level_map):
        for col_index, tile in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            if tile == 1:
                pygame.draw.rect(surface, (100, 100, 255), (x, y, TILE_SIZE, TILE_SIZE))  # azul
            elif tile == 2:
                pygame.draw.rect(surface, (255, 0, 0), (x, y, TILE_SIZE, TILE_SIZE))  # zona del jefe final

