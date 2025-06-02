import pygame

def draw_score(screen, font, score, color, width):
    score_text = font.render(f"Score: {score}", True, color)
    score_rect = score_text.get_rect(center=(width // 2, 40))
    # Usar el mismo color para el borde del rectángulo, pero con alpha para el fondo
    rect_surface = pygame.Surface((score_rect.width + 20, score_rect.height + 10), pygame.SRCALPHA)
    # Fondo semitransparente del mismo color (con alpha 80)
    bg_color = (*color, 80) if len(color) == 3 else color
    pygame.draw.rect(rect_surface, bg_color, rect_surface.get_rect())
    # Borde del mismo color que el texto
    pygame.draw.rect(rect_surface, color, rect_surface.get_rect(), 2)
    screen.blit(rect_surface, (score_rect.x - 10, score_rect.y - 5))
    screen.blit(score_text, score_rect)

def get_score_color(score):
    if score < 6:
        return (255, 255, 255)  # Blanco
    elif 6 <= score <= 10:
        return (255, 255, 0)    # Amarillo
    elif 11 <= score <= 20:
        return (0, 255, 0)      # Verde
    else:
        return (128, 0, 128)    # Morado

def draw_pause_overlay(screen, width, height, font):
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))
    pause_text = font.render("PAUSE", True, (255, 255, 255))
    pause_text_rect = pause_text.get_rect(center=(width // 2, height // 2))
    screen.blit(pause_text, pause_text_rect)

def draw_game_over_overlay(screen, width, height, font_big, font_small):
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))
    game_over_text = font_big.render("Game Over!", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(width // 2, height // 2 - 50))
    screen.blit(game_over_text, game_over_rect)
    restart_text = font_small.render("Press SPACE to restart", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(width // 2, height // 2 + 40))
    screen.blit(restart_text, restart_rect)

def draw_pause_button(screen, rect, paused, pause_btn_img, play_btn_img, pause_font):
    pygame.draw.rect(screen, (0,0,0,0), rect)
    pygame.draw.rect(screen, (255,255,255), rect, 2)
    if paused:
        if play_btn_img:
            btn_img = pygame.transform.smoothscale(play_btn_img, (rect.width-6, rect.height-6))
            btn_rect = btn_img.get_rect(center=rect.center)
            screen.blit(btn_img, btn_rect)
        else:
            pause_text = pause_font.render('▶', True, (255,255,255))
            pause_text_rect = pause_text.get_rect(center=rect.center)
            screen.blit(pause_text, pause_text_rect)
    else:
        if pause_btn_img:
            btn_img = pygame.transform.smoothscale(pause_btn_img, (rect.width-6, rect.height-6))
            btn_rect = btn_img.get_rect(center=rect.center)
            screen.blit(btn_img, btn_rect)
        else:
            pause_text = pause_font.render('⏸', True, (255,255,255))
            pause_text_rect = pause_text.get_rect(center=rect.center)
            screen.blit(pause_text, pause_text_rect)
