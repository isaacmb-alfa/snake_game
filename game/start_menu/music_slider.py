import pygame
from .config import WIDTH, WHITE, YELLOW, GREEN

class MusicSlider:
    def __init__(self, menu_font):
        self.menu_font = menu_font

    def draw(self, screen, label, value, y, selected=False):
        color = YELLOW if selected else WHITE
        font = self.menu_font
        text = font.render(f'{label}:', True, color)
        text_rect = text.get_rect(right=WIDTH//2-20, centery=y)
        screen.blit(text, text_rect)
        bar_rect = pygame.Rect(WIDTH//2, y-12, 120, 24)
        pygame.draw.rect(screen, WHITE, bar_rect, 2, border_radius=8)
        fill_rect = pygame.Rect(bar_rect.x+2, bar_rect.y+2, int((value/10)*116), 20)
        pygame.draw.rect(screen, GREEN, fill_rect, border_radius=8)
        percent_text = font.render(f'{value*10}%', True, color)
        percent_rect = percent_text.get_rect(left=bar_rect.right+10, centery=y)
        screen.blit(percent_text, percent_rect)
