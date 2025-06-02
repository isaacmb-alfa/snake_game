import pygame
import os

def load_font(path, size, fallback=None):
    try:
        return pygame.font.Font(path, size)
    except Exception:
        if fallback:
            return pygame.font.SysFont(fallback, size)
        return pygame.font.SysFont('Arial', size)

def load_image(path):
    try:
        return pygame.image.load(path).convert_alpha()
    except Exception:
        return None

def load_tile(path):
    try:
        return pygame.image.load(path).convert()
    except Exception:
        return None
