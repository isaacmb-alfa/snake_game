import pygame
from .config import WIDTH, WHITE
from assets import load_tile

class BgSelector:
    def __init__(self, menu_font, bg_options):
        self.menu_font = menu_font
        self.bg_options = bg_options
        self.bg_idx = 0

    def draw(self, screen, y):
        font = self.menu_font
        label = 'Fondo'
        value = self.bg_options[self.bg_idx]
        color = WHITE
        text = font.render(f'{label}:', True, color)
        text_rect = text.get_rect(right=WIDTH//2-60, centery=y+30)
        screen.blit(text, text_rect)
        value_text = font.render(f'{value}', True, color)
        value_rect = value_text.get_rect(left=text_rect.right+10, centery=y+30)
        screen.blit(value_text, value_rect)
        thumb_rect = pygame.Rect(WIDTH//2+130, y-20, 120, 120)
        thumb_bg = pygame.Surface((thumb_rect.width, thumb_rect.height), pygame.SRCALPHA)
        thumb_bg.fill((0, 0, 0, 0))
        pygame.draw.rect(thumb_bg, (255, 255, 255, 100), thumb_bg.get_rect(), border_radius=5)
        screen.blit(thumb_bg, thumb_rect.topleft)
        pygame.draw.rect(screen, WHITE, thumb_rect, 2, border_radius=5)
        try:
            tile_img = load_tile('assets/img/tile.png')
            if tile_img:
                tile_img = pygame.transform.smoothscale(tile_img, (100, 100))
                screen.blit(tile_img, (thumb_rect.x+10, thumb_rect.y+10))
        except Exception:
            pass
