# Nombre: Maylon Javier Polanco
# Matrícula: 15-EISN-2-004

import pygame

TILE_SIZE = 40

# Nivel estilo lineal con obstáculos y jefe al final
level_map = [
    [1]*30,
    [1] + [0]*28 + [1],
    [1,0,1,0,1,0,1,0,1,0,1,0,0,0,1,1,0,0,1,0,1,0,1,0,1,0,1,0,0,1],
    [1] + [0]*28 + [1],
    [1]*30
]

def draw_level(surface):
    for row_index, row in enumerate(level_map):
        for col_index, tile in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            if tile == 1:
                pygame.draw.rect(surface, (100, 100, 255), (x, y, TILE_SIZE, TILE_SIZE))
