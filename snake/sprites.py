import pygame
import os
from .config import GRID_SIZE, GREEN, YELLOW, WHITE, RED

SPRITES = {}

SPRITES_PATHS_EXTRA_TURNS = {
    'body_turn_right_up': os.path.join('assets', 'snake_body_turn_right_up.png'),
    'body_turn_up_right': os.path.join('assets', 'snake_body_turn_up_right.png'),
    'body_turn_left_up': os.path.join('assets', 'snake_body_turn_left_up.png'),
    'body_turn_up_left': os.path.join('assets', 'snake_body_turn_up_left.png'),
    'body_turn_right_down': os.path.join('assets', 'snake_body_turn_right_down.png'),
    'body_turn_down_right': os.path.join('assets', 'snake_body_turn_down_right.png'),
    'body_turn_left_down': os.path.join('assets', 'snake_body_turn_left_down.png'),
    'body_turn_down_left': os.path.join('assets', 'snake_body_turn_down_left.png'),
}

def recreate_turn_sprites():
    """Force recreation of the turn sprites and save them to assets folder"""
    from pathlib import Path
    assets_dir = Path('assets')
    assets_dir.mkdir(exist_ok=True)
    
    # Create and save the turn sprites
    turn_sprites = {
        'snake_body_turn_up_right.png': create_turn_sprite_up_right(),
        'snake_body_turn_up_left.png': create_turn_sprite_up_left(),
        'snake_body_turn_down_right.png': create_turn_sprite_down_right(),
        'snake_body_turn_down_left.png': create_turn_sprite_down_left()
    }
    
    for filename, surface in turn_sprites.items():
        file_path = assets_dir / filename
        pygame.image.save(surface, str(file_path))
        print(f"Recreated and saved: {filename}")

def create_default_sprites():
    from pathlib import Path
    assets_dir = Path('assets')
    assets_dir.mkdir(exist_ok=True)
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
        'snake_body_turn_down_left.png': lambda: create_turn_sprite_down_left()
    }
    for filename, create_func in sprites_to_create.items():
        file_path = assets_dir / filename
        if not file_path.exists():
            surface = create_func()
            pygame.image.save(surface, str(file_path))

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
    import os
    global SPRITES
    sprites_paths = {
        'head': os.path.join('assets', 'snake_head.png'),
        'body': os.path.join('assets', 'snake_body.png'),
        'body_h': os.path.join('assets', 'snake_body_h.png'),
        'body_v': os.path.join('assets', 'snake_body_v.png'),
        'tail': os.path.join('assets', 'snake_tail.png'),
        'food': os.path.join('assets', 'food.png'),
        # Solo los 4 giros originales, los 8 nuevos se agregan abajo
        'body_turn_up_right': os.path.join('assets', 'snake_body_turn_up_right.png'),
        'body_turn_up_left': os.path.join('assets', 'snake_body_turn_up_left.png'),
        'body_turn_down_right': os.path.join('assets', 'snake_body_turn_down_right.png'),
        'body_turn_down_left': os.path.join('assets', 'snake_body_turn_down_left.png'),
    }
    # Agregar los 8 sprites de giro extendidos
    sprites_paths.update(SPRITES_PATHS_EXTRA_TURNS)
    turn_debug_colors = {
        'body_turn_up_right': (255, 0, 0),
        'body_turn_up_left': (0, 255, 0),
        'body_turn_down_right': (0, 0, 255),
        'body_turn_down_left': (255, 255, 0),
        # Colores para los nuevos
        'body_turn_right_up': (255, 128, 128),
        'body_turn_left_up': (128, 255, 128),
        'body_turn_right_down': (128, 128, 255),
        'body_turn_left_down': (255, 255, 128),
    }
    for name, path in sprites_paths.items():
        try:
            sprite = pygame.image.load(path).convert_alpha()
            SPRITES[name] = pygame.transform.scale(sprite, (GRID_SIZE, GRID_SIZE))
        except pygame.error:
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
