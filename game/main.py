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

    font = pygame.font.Font('assets/fonts/8bitOperatorPlus8-Regular.ttf', 25)
    snake = Snake()
    food = Food(snake.positions)
    score = 0
    game_over = False

    # Cargar tile de fondo
    try:
        tile_img = pygame.image.load('tile.png').convert()
    except Exception:
        tile_img = None

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

        # Dibuja el fondo con tiles
        if tile_img:
            for x in range(0, WIDTH, tile_img.get_width()):
                for y in range(0, HEIGHT, tile_img.get_height()):
                    screen.blit(tile_img, (x, y))
        else:
            screen.fill(BLACK)
        snake.render(screen)
        food.render(screen)
        # Estilo condicional del score
        if score < 6:
            score_color = WHITE
        elif 6 <= score <= 10:
            score_color = (255, 255, 0)  # Amarillo
        elif 11 <= score <= 20:
            score_color = (0, 255, 0)    # Verde
        else:
            score_color = (128, 0, 128)  # Morado

        score_text = font.render(f"Score: {score}", True, score_color)
        score_rect = score_text.get_rect(center=(WIDTH // 2, 40))
        # Dibujar rectángulo transparente con borde blanco
        rect_surface = pygame.Surface((score_rect.width + 20, score_rect.height + 10), pygame.SRCALPHA) #rectangulo transparente
        pygame.draw.rect(rect_surface, (0,0,0,0), rect_surface.get_rect())  # Fondo totalmente transparente
        pygame.draw.rect(rect_surface, (255,255,255), rect_surface.get_rect(), 1)  # Borde blanco
        # Blit del rectángulo y luego el texto
        screen.blit(rect_surface, (score_rect.x - 10, score_rect.y - 5))
        screen.blit(score_text, score_rect)
        if game_over:
            game_over_text = font.render("Game Over! Press SPACE to restart", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
        pygame.display.update()
        clock.tick(SNAKE_SPEED)

if __name__ == "__main__":
    main()
