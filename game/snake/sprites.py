import pygame
import os
import sys
try:
    from ..resource_util import resource_path
except ImportError:
    from resource_util import resource_path
from .config import GRID_SIZE, GREEN, YELLOW, WHITE, RED

# Directorio base para los sprites
IMG_DIR = 'assets/img'

# Diccionario global de sprites
SPRITES = {}

SPRITES_PATHS_EXTRA_TURNS = {
    'body_turn_right_up': resource_path('assets/img/snake_body_turn_right_up.png'),
    'body_turn_up_right': resource_path('assets/img/snake_body_turn_up_right.png'),
    'body_turn_left_up': resource_path('assets/img/snake_body_turn_left_up.png'),
    'body_turn_up_left': resource_path('assets/img/snake_body_turn_up_left.png'),
    'body_turn_right_down': resource_path('assets/img/snake_body_turn_right_down.png'),
    'body_turn_down_right': resource_path('assets/img/snake_body_turn_down_right.png'),
    'body_turn_left_down': resource_path('assets/img/snake_body_turn_left_down.png'),
    'body_turn_down_left': resource_path('assets/img/snake_body_turn_down_left.png'),
}

def recreate_turn_sprites():
    """Regenera los sprites de curvas y los guarda en la carpeta de assets"""
    base_dir = resource_path('assets/img')
    os.makedirs(base_dir, exist_ok=True)
    
    # Crear y guardar los sprites de curvas
    turn_sprites = {
        'snake_body_turn_up_right.png': create_turn_sprite_up_right(),
        'snake_body_turn_up_left.png': create_turn_sprite_up_left(),
        'snake_body_turn_down_right.png': create_turn_sprite_down_right(),
        'snake_body_turn_down_left.png': create_turn_sprite_down_left(),
        'snake_body_turn_right_up.png': create_turn_sprite_up_right(),
        'snake_body_turn_left_up.png': create_turn_sprite_up_left(),
        'snake_body_turn_right_down.png': create_turn_sprite_down_right(),
        'snake_body_turn_left_down.png': create_turn_sprite_down_left()
    }
    
    for filename, surface in turn_sprites.items():
        file_path = os.path.join(base_dir, filename)
        pygame.image.save(surface, file_path)
        print(f"Sprite regenerado: {filename}")

def create_default_sprites():
    """Crea los sprites por defecto si no existen en la carpeta de assets"""
    base_dir = resource_path('assets/img')
    os.makedirs(base_dir, exist_ok=True)
    
    sprites_to_create = {
        'snake_head.png': lambda: create_head_sprite(),
        'snake_body.png': lambda: create_body_sprite(GREEN),
        'snake_body_h.png': lambda: create_body_h_sprite(),
        'snake_body_v.png': lambda: create_body_v_sprite(),
        'snake_tail.png': lambda: create_tail_sprite(),
        'food.png': lambda: create_food_sprite(),
        'snake_body_turn_up_right.png': lambda: create_turn_sprite_up_right(),
        'snake_body_turn_up_left.png': lambda: create_turn_sprite_up_left(),
        'snake_body_turn_down_right.png': lambda: create_turn_sprite_down_right(),
        'snake_body_turn_down_left.png': lambda: create_turn_sprite_down_left(),
        'snake_body_turn_right_up.png': lambda: create_turn_sprite_up_right(),
        'snake_body_turn_left_up.png': lambda: create_turn_sprite_up_left(),
        'snake_body_turn_right_down.png': lambda: create_turn_sprite_down_right(),
        'snake_body_turn_left_down.png': lambda: create_turn_sprite_down_left()
    }
    
    sprites_created = False
    for filename, create_func in sprites_to_create.items():
        file_path = os.path.join(base_dir, filename)
        if not os.path.exists(file_path):
            surface = create_func()
            pygame.image.save(surface, file_path)
            sprites_created = True
            print(f"Sprite creado: {filename}")
    
    if sprites_created:
        print("Se han creado los sprites por defecto en game/assets/img/")

def create_head_sprite():
    surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    points = [(0, 0), (0, GRID_SIZE), (GRID_SIZE, GRID_SIZE // 2)]
    pygame.draw.polygon(surface, YELLOW, points)
    pygame.draw.polygon(surface, WHITE, points, 1)
    return surface

def create_body_sprite(color=GREEN):
    surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    rect = pygame.Rect(0, 0, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, WHITE, rect, 1)
    return surface

def create_body_h_sprite():
    surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    rect = pygame.Rect(0, GRID_SIZE // 4, GRID_SIZE, GRID_SIZE // 2)
    pygame.draw.rect(surface, GREEN, rect)
    pygame.draw.rect(surface, WHITE, rect, 1)
    return surface

def create_body_v_sprite():
    surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    rect = pygame.Rect(GRID_SIZE // 4, 0, GRID_SIZE // 2, GRID_SIZE)
    pygame.draw.rect(surface, GREEN, rect)
    pygame.draw.rect(surface, WHITE, rect, 1)
    return surface

def create_tail_sprite():
    surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    points = [(GRID_SIZE, 0), (GRID_SIZE, GRID_SIZE), (0, GRID_SIZE // 2)]
    pygame.draw.polygon(surface, GREEN, points)
    pygame.draw.polygon(surface, WHITE, points, 1)
    return surface

def create_food_sprite():
    surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(surface, RED, (GRID_SIZE // 2, GRID_SIZE // 2), GRID_SIZE // 2)
    pygame.draw.circle(surface, WHITE, (GRID_SIZE // 2, GRID_SIZE // 2), GRID_SIZE // 2, 1)
    return surface

def create_turn_sprite_up_right():
    surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    points = [
        (GRID_SIZE // 4, GRID_SIZE),          # Bottom left of vertical part
        (GRID_SIZE // 4, GRID_SIZE // 4),     # Top left of vertical part
        (GRID_SIZE // 2, GRID_SIZE // 4),     # Top right of vertical part
        (GRID_SIZE // 2, GRID_SIZE // 2),     # Inner corner
        (GRID_SIZE, GRID_SIZE // 2),          # Right of horizontal part
        (GRID_SIZE, GRID_SIZE * 3 // 4),      # Bottom right of horizontal part
        (GRID_SIZE // 2, GRID_SIZE * 3 // 4), # Bottom left of horizontal part
        (GRID_SIZE // 2, GRID_SIZE)           # Bottom right of vertical part
    ]
    pygame.draw.polygon(surface, GREEN, points)
    pygame.draw.polygon(surface, WHITE, points, 1)
    # Optional inner corner line for visual detail
    pygame.draw.line(surface, WHITE, (GRID_SIZE // 4, GRID_SIZE // 2), (GRID_SIZE // 2, GRID_SIZE // 2), 1)
    pygame.draw.line(surface, WHITE, (GRID_SIZE // 2, GRID_SIZE // 2), (GRID_SIZE // 2, GRID_SIZE * 3 // 4), 1)
    return surface

def create_turn_sprite_up_left():
    surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    points = [
        (GRID_SIZE * 3 // 4, GRID_SIZE),      # Bottom right of vertical part
        (GRID_SIZE * 3 // 4, GRID_SIZE // 4), # Top right of vertical part
        (GRID_SIZE // 2, GRID_SIZE // 4),     # Top left of vertical part
        (GRID_SIZE // 2, GRID_SIZE // 2),     # Inner corner
        (0, GRID_SIZE // 2),                  # Left of horizontal part
        (0, GRID_SIZE * 3 // 4),              # Bottom left of horizontal part
        (GRID_SIZE // 2, GRID_SIZE * 3 // 4), # Bottom right of horizontal part
        (GRID_SIZE // 2, GRID_SIZE)           # Bottom left of vertical part
    ]
    pygame.draw.polygon(surface, GREEN, points)
    pygame.draw.polygon(surface, WHITE, points, 1)
    # Optional inner corner line for visual detail
    pygame.draw.line(surface, WHITE, (GRID_SIZE * 3 // 4, GRID_SIZE // 2), (GRID_SIZE // 2, GRID_SIZE // 2), 1)
    pygame.draw.line(surface, WHITE, (GRID_SIZE // 2, GRID_SIZE // 2), (GRID_SIZE // 2, GRID_SIZE * 3 // 4), 1)
    return surface

def create_turn_sprite_down_right():
    surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    points = [
        (GRID_SIZE // 4, GRID_SIZE // 2),        # Middle left of vertical part
        (GRID_SIZE // 4, GRID_SIZE),             # Bottom left of vertical part
        (GRID_SIZE // 2, GRID_SIZE),             # Bottom right of vertical part
        (GRID_SIZE // 2, GRID_SIZE // 2),        # Inner corner
        (GRID_SIZE, GRID_SIZE // 2),             # Right of horizontal part
        (GRID_SIZE, GRID_SIZE // 4),             # Top right of horizontal part
        (GRID_SIZE // 2, GRID_SIZE // 4),        # Top left of horizontal part
        (GRID_SIZE // 2, GRID_SIZE // 2)         # Inner corner (repeated)
    ]
    pygame.draw.polygon(surface, GREEN, points)
    pygame.draw.polygon(surface, WHITE, points, 1)
    # Optional inner corner line for visual detail
    pygame.draw.line(surface, WHITE, (GRID_SIZE // 4, GRID_SIZE // 2), (GRID_SIZE // 2, GRID_SIZE // 2), 1)
    pygame.draw.line(surface, WHITE, (GRID_SIZE // 2, GRID_SIZE // 2), (GRID_SIZE // 2, GRID_SIZE), 1)
    return surface

def create_turn_sprite_down_left():
    surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    points = [
        (GRID_SIZE * 3 // 4, GRID_SIZE // 2),        # Middle right of vertical part
        (GRID_SIZE * 3 // 4, GRID_SIZE),             # Bottom right of vertical part
        (GRID_SIZE // 2, GRID_SIZE),                 # Bottom left of vertical part
        (GRID_SIZE // 2, GRID_SIZE // 2),            # Inner corner
        (0, GRID_SIZE // 2),                         # Left of horizontal part
        (0, GRID_SIZE // 4),                         # Top left of horizontal part
        (GRID_SIZE // 2, GRID_SIZE // 4),            # Top right of horizontal part
        (GRID_SIZE // 2, GRID_SIZE // 2)             # Inner corner (repeated)
    ]
    pygame.draw.polygon(surface, GREEN, points)
    pygame.draw.polygon(surface, WHITE, points, 1)
    # Optional inner corner line for visual detail
    pygame.draw.line(surface, WHITE, (GRID_SIZE * 3 // 4, GRID_SIZE // 2), (GRID_SIZE // 2, GRID_SIZE // 2), 1)
    pygame.draw.line(surface, WHITE, (GRID_SIZE // 2, GRID_SIZE // 2), (GRID_SIZE // 2, GRID_SIZE), 1)
    return surface

def load_sprites():
    """Carga o genera todos los sprites necesarios para el juego"""
    global SPRITES
    
    # Definir todos los sprites necesarios y sus rutas
    sprites_paths = {
        'head': 'snake_head.png',
        'body': 'snake_body.png',
        'body_h': 'snake_body_h.png',
        'body_v': 'snake_body_v.png',
        'tail': 'snake_tail.png',
        'food': 'food.png',
        'body_turn_up_right': 'snake_body_turn_up_right.png',
        'body_turn_up_left': 'snake_body_turn_up_left.png',
        'body_turn_down_right': 'snake_body_turn_down_right.png',
        'body_turn_down_left': 'snake_body_turn_down_left.png',
        'body_turn_right_up': 'snake_body_turn_right_up.png',
        'body_turn_left_up': 'snake_body_turn_left_up.png',
        'body_turn_right_down': 'snake_body_turn_right_down.png',
        'body_turn_left_down': 'snake_body_turn_left_down.png'
    }    # Colores de depuración para las curvas
    turn_debug_colors = {
        'body_turn_up_right': (255, 0, 0),      # Rojo
        'body_turn_up_left': (0, 255, 0),       # Verde
        'body_turn_down_right': (0, 0, 255),    # Azul
        'body_turn_down_left': (255, 255, 0),   # Amarillo
        'body_turn_right_up': (255, 128, 128),  # Rosa
        'body_turn_left_up': (128, 255, 128),   # Verde claro
        'body_turn_right_down': (128, 128, 255),# Azul claro
        'body_turn_left_down': (255, 255, 128)  # Amarillo claro
    }

    # Cargar o generar cada sprite
    for name, filename in sprites_paths.items():
        full_path = resource_path(os.path.join(IMG_DIR, filename))
        try:
            sprite = pygame.image.load(full_path).convert_alpha()
            SPRITES[name] = pygame.transform.scale(sprite, (GRID_SIZE, GRID_SIZE))
        except (pygame.error, FileNotFoundError):
            surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
            if name == 'head':
                pygame.draw.circle(surface, YELLOW, (GRID_SIZE//2, GRID_SIZE//2), GRID_SIZE//2)
                pygame.draw.circle(surface, WHITE, (GRID_SIZE//2, GRID_SIZE//2), GRID_SIZE//2, 1)
            elif name == 'tail':
                pygame.draw.circle(surface, GREEN, (GRID_SIZE//2, GRID_SIZE//2), GRID_SIZE//2)
                pygame.draw.circle(surface, WHITE, (GRID_SIZE//2, GRID_SIZE//2), GRID_SIZE//2, 1)
            elif name == 'body' or name == 'body_h' or name == 'body_v':
                pygame.draw.rect(surface, GREEN, pygame.Rect(0, 0, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, WHITE, pygame.Rect(0, 0, GRID_SIZE, GRID_SIZE), 1)
            elif name.startswith('body_turn'):
                color = turn_debug_colors.get(name, GREEN)
                pygame.draw.rect(surface, color, pygame.Rect(0, 0, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, WHITE, pygame.Rect(0, 0, GRID_SIZE, GRID_SIZE), 1)
            elif name == 'food':
                pygame.draw.circle(surface, RED, (GRID_SIZE//2, GRID_SIZE//2), GRID_SIZE//2)
                pygame.draw.circle(surface, WHITE, (GRID_SIZE//2, GRID_SIZE//2), GRID_SIZE//2, 1)
            SPRITES[name] = surface
