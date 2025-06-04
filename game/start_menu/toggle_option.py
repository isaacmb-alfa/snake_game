import pygame
from .config import WIDTH, WHITE, YELLOW

class ToggleOption:
    def __init__(self, menu_font):
        self.menu_font = menu_font

    def draw(self, screen, label, value, y, selected=False):
        color = YELLOW if selected else WHITE
        text = self.menu_font.render(f'{label}: {"On" if value else "Off"}', True, color)
        rect = text.get_rect(center=(WIDTH//2, y))
        screen.blit(text, rect)
