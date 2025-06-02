import pygame
from pathlib import Path

# Constantes de configuración de la ventana y el juego
WIDTH, HEIGHT = 800, 700# Tamaño de la ventana
GRID_SIZE = 20             # Tamaño de cada celda de la cuadrícula
GRID_WIDTH = WIDTH // GRID_SIZE   # Número de celdas horizontales
GRID_HEIGHT = HEIGHT // GRID_SIZE # Número de celdas verticales
SNAKE_SPEED = 4         # Velocidad de la serpiente (frames por segundo)

# Definición de colores en formato RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Direcciones posibles de movimiento (x, y)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

__all__ = [
    'WIDTH', 'HEIGHT', 'GRID_SIZE', 'GRID_WIDTH', 'GRID_HEIGHT', 'SNAKE_SPEED',
    'BLACK', 'WHITE', 'GREEN', 'RED', 'YELLOW',
    'UP', 'DOWN', 'LEFT', 'RIGHT'
]
