import pygame
import sys
from snake.config import WIDTH, HEIGHT, SNAKE_SPEED, BLACK, WHITE, UP, DOWN, LEFT, RIGHT
from snake.sprites import create_default_sprites, load_sprites
from snake.snake import Snake
from snake.food import Food
import shutil
import os

# Limpia la caché __pycache__ al iniciar
pycache_path = os.path.join(os.path.dirname(__file__), "snake", "__pycache__")
if os.path.exists(pycache_path):
    shutil.rmtree(pycache_path)

# Ajuste para que la ruta base de assets sea relativa a este archivo
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets", "img")

# Monkeypatch para que pygame.image.load busque en assets/img por defecto
import pygame
_original_load = pygame.image.load

def _patched_load(path, *args, **kwargs):
    if not os.path.isabs(path) and not os.path.exists(path):
        path = os.path.join(ASSETS_PATH, path)
    return _original_load(path, *args, **kwargs)
pygame.image.load = _patched_load


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake Game')

    # Crea sprites por defecto si no existen y luego carga los sprites
    # create_default_sprites()
    load_sprites()

    font = pygame.font.SysFont('Arial', 25)
    snake = Snake()
    food = Food(snake.positions)
    score = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_SPACE:
                        snake = Snake()
                        food = Food(snake.positions)
                        score = 0
                        game_over = False
                else:
                    if event.key == pygame.K_UP:
                        snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction(RIGHT)

        if not game_over:
            if not snake.update():
                game_over = True
            if snake.get_head_position() == food.position:
                snake.grow_snake()
                food = Food(snake.positions)
                score += 1

        screen.fill(BLACK)
        snake.render(screen)
        food.render(screen)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (5, 5))
        if game_over:
            game_over_text = font.render("Game Over! Press SPACE to restart", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
        pygame.display.update()
        clock.tick(SNAKE_SPEED)

if __name__ == "__main__":
    main()
