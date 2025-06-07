import pygame
from ..snake.config import WIDTH, WHITE, BLACK
from ..snake.sprites import SPRITES, load_sprites

class SkinSelector:
    def __init__(self, menu_font, snake_skins):
        self.menu_font = menu_font
        self.snake_skins = snake_skins
        self.skin_idx = 0

    def draw(self, screen, y):
        font = self.menu_font
        label = 'Skin'
        value = self.snake_skins[self.skin_idx]
        color = WHITE
        text = font.render(f'{label}:', True, color)
        text_rect = text.get_rect(right=WIDTH//2-90, centery=y+20)
        screen.blit(text, text_rect)
        value_text = font.render(f'{value}', True, color)
        value_rect = value_text.get_rect(left=text_rect.right+10, centery=y+20)
        screen.blit(value_text, value_rect)
        preview_rect = pygame.Rect(WIDTH//2+90, y, 120, 60)
        pygame.draw.rect(screen, BLACK, preview_rect, border_radius=5)
        pygame.draw.rect(screen, WHITE, preview_rect, 2, border_radius=5)
        if not SPRITES.get('tail'):
            load_sprites()
        seg_w = 24
        total_w = seg_w * 4
        x = preview_rect.x + (preview_rect.width - total_w) // 2 + seg_w // 2
        y0 = preview_rect.centery
        tail_img = pygame.transform.smoothscale(SPRITES['tail'], (seg_w, seg_w))
        screen.blit(tail_img, (x-seg_w//2, y0-seg_w//2))
        x += seg_w
        body_img = pygame.transform.smoothscale(SPRITES['body'], (seg_w, seg_w))
        screen.blit(body_img, (x-seg_w//2, y0-seg_w//2))
        x += seg_w
        body_img2 = pygame.transform.smoothscale(SPRITES['body'], (seg_w, seg_w))
        screen.blit(body_img2, (x-seg_w//2, y0-seg_w//2))
        x += seg_w
        head_img = pygame.transform.smoothscale(SPRITES['head'], (seg_w, seg_w))
        screen.blit(head_img, (x-seg_w//2, y0-seg_w//2))
