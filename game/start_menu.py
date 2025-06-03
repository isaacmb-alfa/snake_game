import pygame
from snake.config import WIDTH, HEIGHT, WHITE, BLACK, GREEN, YELLOW
from assets import load_font, load_image


class StartMenu:
    def __init__(self):
        self.title_font = load_font(
            'assets/fonts/8bitOperatorPlus8-Bold.ttf', 72)
        self.menu_font = load_font(
            'assets/fonts/8bitOperatorPlus8-Regular.ttf', 32)
        self.footer_font = load_font(
            'assets/fonts/8bitOperatorPlus8-Regular.ttf', 18)
        self.bg_color = (7, 7, 7)
        self.button_color = (60, 180, 80)
        self.button_hover = (80, 220, 120)
        self.button_rect = pygame.Rect(WIDTH//2-120, HEIGHT-180, 240, 60)
        self.levels = ['Fácil', 'Normal', 'Difícil']
        self.level_idx = 1
        self.sound_on = True
        self.music_volume = 5
        self.bg_options = ['Default']
        self.bg_idx = 0
        self.snake_skins = ['Default']
        self.skin_idx = 0
        self.running = True
        self.selected = None
        self.levels = ['Normal', 'Hard', 'Very Hard']
        self.level_idx = 0
        self.level_anim_offset = 0  # Offset para animación
        self.level_animating = False
        self.level_anim_direction = 0  # -1 izquierda, 1 derecha
        self.level_anim_target = 0
        self.level_anim_speed = 20  # px por frame
        # Calcula el ancho máximo del texto de nivel
        self.menu_font = load_font(
            'assets/fonts/8bitOperatorPlus8-Regular.ttf', 32)
        self.level_max_width = max(self.menu_font.size(l)[
                                   0] for l in self.levels)
        self.level_left_arrow = None
        self.level_right_arrow = None
        # Guarda las posiciones de las flechas para el selector de nivel
        self.level_left_arrow = None
        self.level_right_arrow = None

    def draw(self, screen):
        screen.fill(self.bg_color)
        # Título
        title = self.title_font.render('Snake Dev', True, YELLOW)
        title_rect = title.get_rect(center=(WIDTH//2, 60))
        screen.blit(title, title_rect)
        # Distribución vertical mejorada
        y = 150
        spacing = 55
        # --- Pasa el valor actual del nivel ---
        self._draw_selector(screen, 'Nivel', self.levels[self.level_idx], y, selected=(
            self.selected == 'level'))
        y += spacing
        self._draw_toggle(screen, 'Sonido', self.sound_on, y,
                          selected=(self.selected == 'sound'))
        y += spacing
        self._draw_slider(screen, 'Música', self.music_volume,
                          y, selected=(self.selected == 'music'))
        y += spacing + 10
        self._draw_bg_selector(screen, y)
        y += 130
        self._draw_skin_selector(screen, y)
        # Botón iniciar (ahora debajo de la preview de skin)
        btn_y = y + 90
        self.button_rect = pygame.Rect(WIDTH//2-120, btn_y, 240, 60)
        mouse = pygame.mouse.get_pos()
        color = self.button_hover if self.button_rect.collidepoint(
            mouse) else self.button_color
        pygame.draw.rect(screen, color, self.button_rect, border_radius=20)
        pygame.draw.rect(screen, WHITE, self.button_rect, 3, border_radius=20)
        btn_text = self.menu_font.render('Iniciar', True, WHITE)
        btn_rect = btn_text.get_rect(center=self.button_rect.center)
        screen.blit(btn_text, btn_rect)
        # Footer
        footer = self.footer_font.render(
            f'{WIDTH}x{HEIGHT}  |  Desarrollado por DevCreador ®', True, (180, 180, 180))
        screen.blit(footer, (WIDTH//2 - footer.get_width()//2, HEIGHT-40))

    def _draw_selector(self, screen, label, value, y, selected=False):
        font = self.menu_font
        color = YELLOW if selected else WHITE


        # ...dentro de _draw_selector...
        if label == 'Nivel':
            font = self.menu_font
            color = YELLOW if selected else WHITE
            level_texts = [font.render(l, True, color) for l in self.levels]
            max_level_width = max(t.get_width() for t in level_texts)
            rect_width = max_level_width + 40  # margen horizontal
            rect_height = 48

            # 1. Calcula la posición del label y la dejas FIJA
            label_text = font.render(f'{label}:', True, color)
            label_rect = label_text.get_rect(left=WIDTH//2 - 180, centery=y)
            screen.blit(label_text, label_rect)

            # 2. Calcula el rectángulo de niveles/flechas a partir del label_rect.right
            spacing = 80
            area_rect = pygame.Rect(label_rect.right + spacing,
                                    y - rect_height // 2, rect_width, rect_height)

            # Flechas
            left_arrow_rect = pygame.Rect(
                area_rect.left - 40, area_rect.centery - 14, 30, 28)
            right_arrow_rect = pygame.Rect(
                area_rect.right + 10, area_rect.centery - 14, 30, 28)
            self.level_left_arrow = left_arrow_rect
            self.level_right_arrow = right_arrow_rect

            # Dibuja flechas
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

            # Fondo translúcido SOLO para los niveles
            area_bg = pygame.Surface(
                (area_rect.width, area_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(area_bg, (255, 255, 255, 120),
                            area_bg.get_rect(), border_radius=5)
            prev_clip = screen.get_clip()
            screen.set_clip(area_rect)
            screen.blit(area_bg, area_rect.topleft)

            # Animación de deslizamiento SOLO dentro del rectángulo
            base_x = area_rect.centerx
            text_y = area_rect.centery
            if self.level_animating:
                offset = self.level_anim_offset
                idx_from = (self.level_idx -
                            self.level_anim_direction) % len(self.levels)
                idx_to = self.level_idx
                text_from = font.render(self.levels[idx_from], True, color)
                text_to = font.render(self.levels[idx_to], True, color)
                screen.blit(text_from, text_from.get_rect(
                    center=(base_x - offset, text_y)))
                screen.blit(text_to, text_to.get_rect(
                    center=(base_x - offset + self.level_anim_direction*max_level_width, text_y)))
            else:
                text = font.render(self.levels[self.level_idx], True, color)
                screen.blit(text, text.get_rect(center=(base_x, text_y)))
            # Borde del rectángulo
            pygame.draw.rect(screen, WHITE, area_rect, 2, border_radius=5)
            screen.set_clip(prev_clip)

    def _draw_toggle(self, screen, label, value, y, selected=False):
        font = self.menu_font
        color = YELLOW if selected else WHITE
        text = font.render(f'{label}: {"On" if value else "Off"}', True, color)
        rect = text.get_rect(center=(WIDTH//2, y))
        screen.blit(text, rect)

    def _draw_slider(self, screen, label, value, y, selected=False):
        font = self.menu_font
        color = YELLOW if selected else WHITE
        # Ajustar posición del texto y barra para que no se encimen
        text = font.render(f'{label}:', True, color)
        text_rect = text.get_rect(right=WIDTH//2-20, centery=y)
        screen.blit(text, text_rect)
        # Barra
        bar_rect = pygame.Rect(WIDTH//2, y-12, 120, 24)
        pygame.draw.rect(screen, WHITE, bar_rect, 2, border_radius=8)
        fill_rect = pygame.Rect(
            bar_rect.x+2, bar_rect.y+2, int((value/10)*116), 20)
        pygame.draw.rect(screen, GREEN, fill_rect, border_radius=8)
        # Porcentaje
        percent_text = font.render(f'{value*10}%', True, color)
        percent_rect = percent_text.get_rect(left=bar_rect.right+10, centery=y)
        screen.blit(percent_text, percent_rect)

    def _draw_bg_selector(self, screen, y):
        # Selector de fondo y miniatura
        font = self.menu_font
        label = 'Fondo'
        value = self.bg_options[self.bg_idx]
        color = WHITE
        # --- Comentario: Sección de selector de fondo ---
        # Etiqueta y valor
        text = font.render(f'{label}:', True, color)
        text_rect = text.get_rect(right=WIDTH//2-60, centery=y+30)
        screen.blit(text, text_rect)
        # Valor (por ejemplo, 'Default')
        value_text = font.render(f'{value}', True, color)
        value_rect = value_text.get_rect(left=text_rect.right+10, centery=y+30)
        screen.blit(value_text, value_rect)
        # Miniatura
        thumb_rect = pygame.Rect(
            WIDTH//2+130, y-20, 120, 120)  # x desplazado +10px
        # --- Fondo blanco translúcido para la miniatura con border radius ---
        thumb_bg = pygame.Surface(
            (thumb_rect.width, thumb_rect.height), pygame.SRCALPHA)
        thumb_bg.fill((0, 0, 0, 0))  # Fondo totalmente transparente
        pygame.draw.rect(
            thumb_bg, (255, 255, 255, 100),  # Color blanco translúcido
            thumb_bg.get_rect(), border_radius=5
        )
        screen.blit(thumb_bg, thumb_rect.topleft)

        pygame.draw.rect(screen, WHITE, thumb_rect, 2, border_radius=5)
        # Vista previa real del fondo si existe tile_img
        try:
            from assets import load_tile
            tile_img = load_tile('assets/img/tile.png')
            if tile_img:
                tile_img = pygame.transform.smoothscale(tile_img, (100, 100))
                screen.blit(tile_img, (thumb_rect.x+10, thumb_rect.y+10))
            else:
                # Si no existe, deja el fondo vacío
                pass
        except Exception:
            pass

    def _draw_skin_selector(self, screen, y):
        # --- Comentario: Sección de selector de skin ---
        font = self.menu_font
        label = 'Skin'
        value = self.snake_skins[self.skin_idx]
        color = WHITE
        # Etiqueta y valor
        text = font.render(f'{label}:', True, color)
        text_rect = text.get_rect(right=WIDTH//2-90, centery=y+20)
        screen.blit(text, text_rect)
        value_text = font.render(f'{value}', True, color)
        value_rect = value_text.get_rect(left=text_rect.right+10, centery=y+20)
        screen.blit(value_text, value_rect)
        # Preview de serpiente
        preview_rect = pygame.Rect(WIDTH//2+90, y, 120, 60)
        # Fondo negro para la preview
        pygame.draw.rect(screen, BLACK, preview_rect, border_radius=5)
        pygame.draw.rect(screen, WHITE, preview_rect, 2, border_radius=5)
        # --- Comentario: Usar sprites reales desde assets/img ---
        from snake.sprites import SPRITES
        # Cargar sprites si no están cargados
        if not SPRITES.get('tail'):
            from snake.sprites import load_sprites
            load_sprites()
        # Centrar los segmentos dentro del marco
        seg_w = 24
        total_w = seg_w * 4
        x = preview_rect.x + (preview_rect.width - total_w) // 2 + seg_w // 2
        y0 = preview_rect.centery
        # Cola
        tail_img = pygame.transform.smoothscale(
            SPRITES['tail'], (seg_w, seg_w))
        screen.blit(tail_img, (x-seg_w//2, y0-seg_w//2))
        x += seg_w
        # Cuerpo 1
        body_img = pygame.transform.smoothscale(
            SPRITES['body'], (seg_w, seg_w))
        screen.blit(body_img, (x-seg_w//2, y0-seg_w//2))
        x += seg_w
        # Cuerpo 2
        body_img2 = pygame.transform.smoothscale(
            SPRITES['body'], (seg_w, seg_w))
        screen.blit(body_img2, (x-seg_w//2, y0-seg_w//2))
        x += seg_w
        # Cabeza
        head_img = pygame.transform.smoothscale(
            SPRITES['head'], (seg_w, seg_w))
        screen.blit(head_img, (x-seg_w//2, y0-seg_w//2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                self.running = False
            # --- Manejo de clic en flechas de nivel ---
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
        # --- Animación de deslizamiento de nivel ---
        if self.level_animating:
            self.level_anim_offset += self.level_anim_speed * self.level_anim_direction
            if abs(self.level_anim_offset) >= self.level_max_width:
                # Termina animación y cambia el índice
                self.level_idx = (
                    self.level_idx + self.level_anim_direction) % len(self.levels)
                self.level_animating = False
                self.level_anim_offset = 0

    def run(self, screen):
        clock = pygame.time.Clock()
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                self.handle_event(event)
            self.update()  # Llama a update para animación
            self.draw(screen)
            pygame.display.update()
            clock.tick(60)
