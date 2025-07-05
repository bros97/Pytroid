import pygame
import sys

#  Pygame
pygame.init()

# Pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Metroid-like en VS Code")

# Jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill((255, 0, 0))  # Rojo (placeholder)
        self.rect = self.image.get_rect(center=(100, 300))
        self.speed = 5
        self.jump_power = -15
        self.velocity_y = 0
        self.gravity = 0.8

    def update(self):
        # Movimiento horizontal
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Gravedad y salto
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Limitar al suelo
        if self.rect.bottom > 500:
            self.rect.bottom = 500
            self.velocity_y = 0

    def jump(self):
        if self.rect.bottom >= 500:  # Solo puede saltar si está en el suelo
            self.velocity_y = self.jump_power

# Plataforma
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 255, 0))  # Verde
        self.rect = self.image.get_rect(topleft=(x, y))

# Grupos de sprites
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

# Crear jugador y plataformas
player = Player()
all_sprites.add(player)
platforms.add(Platform(0, 550, 800, 50))  # Suelo
platforms.add(Platform(300, 450, 200, 20))  # Plataforma

# Reloj
clock = pygame.time.Clock()

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    # Actualizar
    all_sprites.update()

    # Dibujar
    screen.fill((0, 0, 0))  # Fondo negro
    all_sprites.draw(screen)
    platforms.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()