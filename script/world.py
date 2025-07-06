# En world.py
class Room:
    def __init__(self, x, y, width, height):
        self.tiles = [[0 for _ in range(width)] for _ in range(height)]  # 0 = aire, 1 = plataforma
        self.doors = {"left": None, "right": None, "up": None, "down": None}  # Conexiones a otras salas