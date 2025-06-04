import pygame
from .config import WIDTH, YELLOW

class LevelSelector:
    def __init__(self, menu_font, levels):
        self.menu_font = menu_font
        self.levels = levels
        self.level_idx = 0
        self.level_anim_offset = 0
        self.level_animating = False
        self.level_anim_direction = 0
        self.level_anim_speed = 10
        self.level_left_arrow = None
        self.level_right_arrow = None
        self.level_max_width = max(self.menu_font.size(l)[0] for l in self.levels)

    def draw(self, screen, y, selected=False):
        # Colores personalizados para cada nivel
        level_colors = [
            (60, 180, 80),    # Verde opaco para Normal
            (255, 220, 60),   # Amarillo para Hard
            (220, 120, 30)    # Naranja oscuro para Very Hard
        ]
        color = level_colors[self.level_idx]
        font = self.menu_font
        label_text = font.render('Nivel:', True, color)
        label_width = label_text.get_width()
        max_level_width = self.level_max_width
        rect_width = max_level_width + 90
        rect_height = 40
        spacing = 80  # El espacio central entre ambos elementos

        # Calcular el ancho total del bloque
        total_width = label_width + spacing + rect_width
        start_x = WIDTH // 2 - total_width // 2

        # Posicionar el texto y el área de selección
        label_rect = label_text.get_rect(left=start_x, centery=y)
        area_rect = pygame.Rect(label_rect.right + spacing, y - rect_height // 2, rect_width, rect_height)
        # Asegurarse de que el label se dibuje
        screen.blit(label_text, label_rect)
        left_arrow_rect = pygame.Rect(area_rect.left - 40, area_rect.centery - 14, 30, 28)
        right_arrow_rect = pygame.Rect(area_rect.right + 10, area_rect.centery - 14, 30, 28)
        self.level_left_arrow = left_arrow_rect
        self.level_right_arrow = right_arrow_rect
        pygame.draw.polygon(screen, color, [
            (left_arrow_rect.right, left_arrow_rect.top),
            (left_arrow_rect.left, left_arrow_rect.centery),
            (left_arrow_rect.right, left_arrow_rect.bottom)
        ])
        pygame.draw.polygon(screen, color, [
            (right_arrow_rect.left, right_arrow_rect.top),
            (right_arrow_rect.right, right_arrow_rect.centery),
            (right_arrow_rect.left, right_arrow_rect.bottom)
        ])
        # Fondo translúcido del área de nivel
        area_bg = pygame.Surface((area_rect.width, area_rect.height), pygame.SRCALPHA)
        area_bg_color = (*color, 120)  # Transparencia
        pygame.draw.rect(area_bg, area_bg_color, area_bg.get_rect(), border_radius=5)
        prev_clip = screen.get_clip()
        screen.set_clip(area_rect)
        screen.blit(area_bg, area_rect.topleft)
        base_x = area_rect.centerx
        text_y = area_rect.centery
        if self.level_animating:
            offset = self.level_anim_offset
            idx_from = (self.level_idx - self.level_anim_direction) % len(self.levels)
            idx_to = self.level_idx
            text_from = font.render(self.levels[idx_from], True, color)
            text_to = font.render(self.levels[idx_to], True, color)
            screen.blit(text_from, text_from.get_rect(center=(base_x - offset, text_y)))
            screen.blit(text_to, text_to.get_rect(center=(base_x - offset + self.level_anim_direction*max_level_width, text_y)))
        else:
            text = font.render(self.levels[self.level_idx], True, color)
            screen.blit(text, text.get_rect(center=(base_x, text_y)))
        pygame.draw.rect(screen, color, area_rect, 2, border_radius=5)
        screen.set_clip(prev_clip)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.level_left_arrow and self.level_left_arrow.collidepoint(event.pos):
                if not self.level_animating:
                    self.level_anim_direction = -1
                    self.level_animating = True
                    self.level_anim_offset = 0
            if self.level_right_arrow and self.level_right_arrow.collidepoint(event.pos):
                if not self.level_animating:
                    self.level_anim_direction = 1
                    self.level_animating = True
                    self.level_anim_offset = 0

    def update(self):
        if self.level_animating:
            self.level_anim_offset += self.level_anim_speed * self.level_anim_direction
            if abs(self.level_anim_offset) >= self.level_max_width:
                self.level_idx = (self.level_idx + self.level_anim_direction) % len(self.levels)
                self.level_animating = False
                self.level_anim_offset = 0
