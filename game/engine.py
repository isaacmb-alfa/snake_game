import pygame
from snake.config import WIDTH, HEIGHT, SNAKE_SPEED, BLACK, WHITE, UP, DOWN, LEFT, RIGHT
from snake.sprites import load_sprites
from snake.snake import Snake
from snake.food import Food
from ui import draw_score, draw_pause_overlay, draw_game_over_overlay, draw_pause_button, get_score_color
from assets import load_font, load_image, load_tile
from start_menu import StartMenu

def run_game():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake Game')

    # Mostrar pantalla de inicio
    menu = StartMenu()
    menu.run(screen)

    load_sprites()

    # Fuentes y recursos
    font = load_font('assets/fonts/8bitOperatorPlus8-Regular.ttf', 25)
    pause_font = load_font('assets/fonts/8bitOperatorPlus8-Bold.ttf', 32, fallback='Arial')
    pause_text_font = load_font('assets/fonts/8bitOperatorPlus8-Bold.ttf', 100, fallback='Arial')
    game_over_font = load_font('assets/fonts/8bitOperatorPlus8-Bold.ttf', 100, fallback='Arial')
    restart_font = load_font('assets/fonts/8bitOperatorPlus8-Regular.ttf', 32, fallback='Arial')
    pause_btn_img = load_image('assets/img/pause_btn.png')
    play_btn_img = load_image('assets/img/play_btn.png')
    tile_img = load_tile('assets/img/tile.png')

    snake = Snake()
    food = Food(snake.positions)
    score = 0
    game_over = False
    paused = False
    pause_button_rect = pygame.Rect(WIDTH - 50, 10, 40, 40)
    # Configuración de velocidad y dirección
    current_speed = SNAKE_SPEED
    boost_active = False
    key_to_direction = {
        pygame.K_UP: UP,
        pygame.K_DOWN: DOWN,
        pygame.K_LEFT: LEFT,
        pygame.K_RIGHT: RIGHT
    }
    direction_to_key = {
        UP: pygame.K_UP,
        DOWN: pygame.K_DOWN,
        LEFT: pygame.K_LEFT,
        RIGHT: pygame.K_RIGHT
    }

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_SPACE:
                        snake = Snake()
                        food = Food(snake.positions)
                        score = 0
                        game_over = False
                else:
                    if event.key in key_to_direction:
                        snake.change_direction(key_to_direction[event.key])
                        if snake.direction == key_to_direction[event.key]:
                            boost_active = True
            elif event.type == pygame.KEYUP:
                if event.key in key_to_direction:
                    if snake.direction == key_to_direction[event.key]:
                        boost_active = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over and pause_button_rect.collidepoint(event.pos):
                    paused = not paused

        if not game_over and not paused:
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

        # Superposición negra semitransparente al pausar
        if paused:
            draw_pause_overlay(screen, WIDTH, HEIGHT, pause_text_font)

        # Botón de pausa/play (siempre visible y clickeable)
        draw_pause_button(screen, pause_button_rect, paused, pause_btn_img, play_btn_img, pause_font)

        # Score
        score_color = get_score_color(score)
        draw_score(screen, font, score, score_color, WIDTH)
        if game_over:
            draw_game_over_overlay(screen, WIDTH, HEIGHT, game_over_font, restart_font)
        if boost_active and not paused and not game_over:
            current_speed = int(SNAKE_SPEED * 2)
        else:
            current_speed = SNAKE_SPEED
        pygame.display.update()
        clock.tick(current_speed)
