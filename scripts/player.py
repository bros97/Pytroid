import pygame
from scripts.bullet import Bullet

class Player:
    def __init__(self, x=100, y=100):
        self.width = 30
        self.height = 40
        self.color = (255, 100, 100)
        self.speed = 4
        self.jump_power = -12
        self.gravity = 0.8
        self.velocity_y = 0
        self.on_ground = False

        self.rect = pygame.Rect(x, y, self.width, self.height)

        self.bullets = []
        self.shoot_cooldown = 0
        self.direction = "right"

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
            self.direction = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
            self.direction = "right"

        # Saltar si está en el suelo
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False

        return dx

    def move(self, dx, walls):
        # Movimiento horizontal
        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall):
                if dx > 0:
                    self.rect.right = wall.left
                elif dx < 0:
                    self.rect.left = wall.right

        # Aplicar gravedad
        self.velocity_y += self.gravity
        if self.velocity_y > 10:
            self.velocity_y = 10  # terminal velocity

        self.rect.y += self.velocity_y

        # Verificar colisiones verticales
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

    def shoot(self):
        if self.shoot_cooldown == 0:
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction)
            self.bullets.append(bullet)
            self.shoot_cooldown = 15

    def update(self, walls):
        dx = self.handle_input()
        self.move(dx, walls)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_j]:
            self.shoot()

        self.bullets = [b for b in self.bullets if b.update(walls)]

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        for bullet in self.bullets:
            bullet.draw(surface)
