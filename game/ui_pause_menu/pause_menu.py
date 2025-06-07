import pygame
import math
import random
from ..snake.config import WIDTH, HEIGHT

class PauseMenuButton:
    def __init__(self, rect, color, label, font, action):
        self.base_rect = pygame.Rect(rect)
        self.rect = self.base_rect.copy()
        self.base_color = color
        self.color = color
        self.label = label
        self.font = font
        self.action = action
        # Animación pulsante
        self.pulse_phase = random.uniform(0, math.pi * 2)  # Fase aleatoria para cada botón
        self.pulse_speed = random.uniform(1.2, 1.7)        # Velocidad ligeramente diferente
        self.pulse_scale = 1.0
        self.pulse_amplitude = 0.07  # Amplitud del escalado (7%)

    def update(self):
        # Animación de "respiración" (pulsante)
        t = pygame.time.get_ticks() / 1000.0
        scale = 1.0 + self.pulse_amplitude * math.sin(self.pulse_phase + t * self.pulse_speed)
        self.pulse_scale = scale
        # Redimensionar el rect para el efecto pulsante
        cx, cy = self.base_rect.center
        w = int(self.base_rect.width * scale)
        h = int(self.base_rect.height * scale)
        self.rect = pygame.Rect(0, 0, w, h)
        self.rect.center = (cx, cy)
        # Color más brillante al máximo de la animación
        factor = (scale - 1.0) / self.pulse_amplitude if self.pulse_amplitude != 0 else 0
        factor = max(0, min(factor, 1))
        r, g, b = self.base_color
        self.color = (
            min(int(r + 30 * factor), 255),
            min(int(g + 30 * factor), 255),
            min(int(b + 30 * factor), 255)
        )

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=8)
        pygame.draw.rect(screen, (255,255,255), self.rect, 2, border_radius=8)
        text = self.font.render(self.label, True, (255,255,255))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered(event.pos):
            return self.action
        return None

class PauseMenu:
    def __init__(self, font):
        btn_width = 180
        btn_height = 60
        spacing = 32
        total_width = btn_width * 3 + spacing * 2
        start_x = WIDTH // 2 - total_width // 2
        y = HEIGHT // 2 + 60
        self.buttons = [
            PauseMenuButton((start_x, y, btn_width, btn_height), (60,180,80), 'Continuar', font, 'continue'),
            PauseMenuButton((start_x+btn_width+spacing, y, btn_width, btn_height), (255,200,40), 'Reiniciar', font, 'restart'),
            PauseMenuButton((start_x+2*(btn_width+spacing), y, btn_width, btn_height), (220,60,60), 'Cerrar', font, 'quit'),
        ]

    def update(self):
        for btn in self.buttons:
            btn.update()

    def draw(self, screen):
        for btn in self.buttons:
            btn.draw(screen)

    def handle_event(self, event):
        for btn in self.buttons:
            action = btn.handle_event(event)
            if action:
                return action
        return None
