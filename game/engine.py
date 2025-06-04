import pygame
from snake.config import WIDTH, HEIGHT, SNAKE_SPEED, BLACK, WHITE, UP, DOWN, LEFT, RIGHT
from snake.sprites import load_sprites
from snake.snake import Snake
from snake.food import Food
from ui import draw_score, draw_pause_overlay, draw_game_over_overlay, draw_pause_button, get_score_color
from assets import load_font, load_image, load_tile
from start_menu.start_menu import StartMenu
from ui_pause_menu.pause_menu import PauseMenu

def run_game():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake Game')

    # Mostrar pantalla de inicio
    menu = StartMenu()
    menu.run(screen)
    # Obtener velocidad seleccionada del menú
    selected_speed = getattr(menu, 'selected_speed', SNAKE_SPEED)
    base_speed = selected_speed
    current_speed = base_speed
    print(f"[DEBUG] Velocidad seleccionada para el juego: {selected_speed}")

    load_sprites()

    # Fuentes y recursos
    font = load_font('assets/fonts/8bitOperatorPlus8-Regular.ttf', 25)
    pause_font = load_font('assets/fonts/8bitOperatorPlus8-Bold.ttf', 24, fallback='Arial')
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
    pause_menu = PauseMenu(pause_font)
    # Configuración de velocidad y dirección
    current_speed = selected_speed
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
            # --- Manejo de botones de pausa ---
            if paused and not game_over:
                action = pause_menu.handle_event(event)
                if action == 'continue':
                    paused = False
                elif action == 'restart':
                    snake = Snake()
                    food = Food(snake.positions)
                    score = 0
                    game_over = False
                    paused = False
                elif action == 'quit':
                    pygame.quit()
                    return

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
            pause_menu.update()
            pause_menu.draw(screen)
        # Botón de pausa/play (siempre visible y clickeable)
        draw_pause_button(screen, pause_button_rect, paused, pause_btn_img, play_btn_img, pause_font)

        # Score
        score_color = get_score_color(score)
        draw_score(screen, font, score, score_color, WIDTH)
        if game_over:
            draw_game_over_overlay(screen, WIDTH, HEIGHT, game_over_font, restart_font)
        # Ajustar velocidad del juego
        if boost_active and not paused and not game_over:
            current_speed = int(base_speed * 2)
        else:
            current_speed = base_speed
            
        pygame.display.update()
        clock.tick(current_speed)
