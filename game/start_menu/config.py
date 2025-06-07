import pygame
from ..snake.config import WIDTH, HEIGHT, WHITE, BLACK, GREEN, YELLOW
from ..assets import load_font

class StartMenuConfig:
    def __init__(self):
        self.title_font = load_font('assets/fonts/8bitOperatorPlus8-Bold.ttf', 72)
        self.menu_font = load_font('assets/fonts/8bitOperatorPlus8-Regular.ttf', 32)
        self.footer_font = load_font('assets/fonts/8bitOperatorPlus8-Regular.ttf', 18)
        self.bg_color = (8, 8, 8)
        self.button_color = (60, 180, 80)
        self.button_hover = (80, 220, 120)
        self.levels = ['Normal', 'Hard', 'Very Hard']
        self.bg_options = ['Default']
        self.snake_skins = ['Default']
