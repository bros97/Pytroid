# menu.py
class Menu:
    def __init__(self):
        self.options = ["Jugar", "Salir"]
        self.selected = 0

    def draw(self, screen):
        for i, opt in enumerate(self.options):
            color = (255, 0, 0) if i == self.selected else (255, 255, 255)
            screen.blit(font.render(opt, True, color), (100, 100 + i * 50))