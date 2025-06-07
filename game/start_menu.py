import pygame
import sys
from snake.config import WIDTH, HEIGHT, WHITE, BLACK, GREEN, YELLOW
from assets import load_font, load_image
from start_menu.title import StartMenuTitle
from start_menu.level_selector import LevelSelector
from start_menu.toggle_option import ToggleOption
from start_menu.music_slider import MusicSlider
from start_menu.bg_selector import BgSelector
from start_menu.skin_selector import SkinSelector


class StartMenu:
    def __init__(self):
        self.config = None  # Puedes cargar config si lo deseas
        self.title = StartMenuTitle(load_font('assets/fonts/8bitOperatorPlus8-Bold.ttf', 72))
        self.levels = ['Normal', 'Hard', 'Very Hard']
        self.level_speeds = [4, 8, 12]  # Asociar velocidad a cada nivel
        self.level_idx = 0
        self.selected_speed = self.level_speeds[self.level_idx]
        self.level_selector = LevelSelector(load_font('assets/fonts/8bitOperatorPlus8-Regular.ttf', 32), self.levels)
        self.toggle_option = ToggleOption(load_font('assets/fonts/8bitOperatorPlus8-Regular.ttf', 32))
        self.music_slider = MusicSlider(load_font('assets/fonts/8bitOperatorPlus8-Regular.ttf', 32))
        self.bg_selector = BgSelector(load_font('assets/fonts/8bitOperatorPlus8-Regular.ttf', 32), ['Default'])
        self.skin_selector = SkinSelector(load_font('assets/fonts/8bitOperatorPlus8-Regular.ttf', 32), ['Default'])
        self.footer_font = load_font('assets/fonts/8bitOperatorPlus8-Regular.ttf', 18)
        self.bg_color = (7, 7, 7)
        self.button_color = (60, 180, 80)
        self.button_hover = (80, 220, 120)
        self.button_rect = pygame.Rect(WIDTH//2-120, HEIGHT-180, 240, 60)
        self.sound_on = True
        self.music_volume = 5
        self.running = True
        self.selected = None

    def draw(self, screen):
        screen.fill(self.bg_color)
        y = 150
        spacing = 55
        self.title.draw(screen)
        self.level_selector.draw(screen, y, selected=(self.selected=='level'))
        y += spacing
        self.toggle_option.draw(screen, 'Sonido', self.sound_on, y, selected=(self.selected=='sound'))
        y += spacing
        self.music_slider.draw(screen, 'Música', self.music_volume, y, selected=(self.selected=='music'))
        y += spacing + 10
        self.bg_selector.draw(screen, y)
        y += 130
        self.skin_selector.draw(screen, y)
        btn_y = y + 90
        self.button_rect = pygame.Rect(WIDTH//2-120, btn_y, 240, 60)
        mouse = pygame.mouse.get_pos()
        color = self.button_hover if self.button_rect.collidepoint(mouse) else self.button_color
        pygame.draw.rect(screen, color, self.button_rect, border_radius=20)
        pygame.draw.rect(screen, WHITE, self.button_rect, 3, border_radius=20)
        btn_text = self.toggle_option.menu_font.render('Iniciar', True, WHITE)
        btn_rect = btn_text.get_rect(center=self.button_rect.center)
        screen.blit(btn_text, btn_rect)
        footer = self.footer_font.render(f'{WIDTH}x{HEIGHT}  |  Desarrollado por DevCreador ®', True, (180,180,180))
        screen.blit(footer, (WIDTH//2 - footer.get_width()//2, HEIGHT-40))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                self.running = False
        self.level_selector.handle_event(event)
        # Aquí puedes agregar navegación con teclado/flechas

    def update(self):
        # --- Animación de deslizamiento de nivel ---
        if hasattr(self, 'level_selector'):
            self.level_selector.update()
        # Actualizar velocidad seleccionada si cambia el nivel
        if hasattr(self, 'level_idx') and hasattr(self, 'level_speeds'):
            self.selected_speed = self.level_speeds[self.level_idx]

    def run(self, screen):
        clock = pygame.time.Clock()
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_event(event)
            self.update()
            self.draw(screen)
            pygame.display.update()
            clock.tick(60)
