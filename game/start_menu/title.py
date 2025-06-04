import pygame
from .config import WIDTH, YELLOW

class StartMenuTitle:
    def __init__(self, font):
        self.font = font
    def draw(self, screen):
        title = self.font.render('Snake Dev', True, YELLOW)
        title_rect = title.get_rect(center=(WIDTH//2, 70))
        screen.blit(title, title_rect)
