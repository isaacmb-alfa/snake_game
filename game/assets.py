import pygame
from .resource_util import resource_path

def load_font(path, size, fallback=None):
    font_path = resource_path(path)
    print(f"[DEBUG] Intentando cargar fuente desde: {font_path}")
    try:
        print(f"[DEBUG] Fuente no encontrada: {font_path} {size}")
        return pygame.font.Font(font_path, size)
    except Exception:
        if fallback:
            print(f"[DEBUG] Usando fuente de respaldo: {fallback} {size}")
            return pygame.font.SysFont(fallback, size)
        return pygame.font.SysFont('Arial', size)

def load_image(path):
    try:
        return pygame.image.load(resource_path(path)).convert_alpha()
    except Exception:
        return None

def load_tile(path):
    try:
        return pygame.image.load(resource_path(path)).convert()
    except Exception:
        return None
