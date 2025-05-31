import pygame
import random
from .config import GRID_WIDTH, GRID_HEIGHT, GRID_SIZE, RED, WHITE
from .sprites import SPRITES

class Food:
    def __init__(self, snake_positions):
        self.position = self.get_random_position(snake_positions)

    def get_random_position(self, snake_positions):
        position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        while position in snake_positions:
            position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        return position

    def render(self, surface):
        rect = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
        surface.blit(SPRITES['food'], rect)
