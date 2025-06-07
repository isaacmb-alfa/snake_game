import pygame
from ..snake.config import WIDTH, HEIGHT
from ..version import VERSION


def draw_footer(screen, font):
    footer = font.render(f'{WIDTH}x{HEIGHT}  |  Desarrollado por DevCreador ® | versión {VERSION} ', True, (180,180,180))
    screen.blit(footer, (WIDTH//2 - footer.get_width()//2, HEIGHT-40))
