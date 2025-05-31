import pygame
from .config import GRID_WIDTH, GRID_HEIGHT, RIGHT, UP, LEFT, DOWN, GRID_SIZE
from .sprites import SPRITES

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2), (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.grow = False
        self.head_sprites = self._create_rotated_sprites('head')
        self.tail_sprites = self._create_rotated_sprites('tail')

    def _create_rotated_sprites(self, sprite_name):
        sprites = {}
        base_sprite = SPRITES[sprite_name]
        sprites[RIGHT] = base_sprite
        sprites[DOWN] = pygame.transform.rotate(base_sprite, 270)
        sprites[LEFT] = pygame.transform.rotate(base_sprite, 180)
        sprites[UP] = pygame.transform.rotate(base_sprite, 90)
        return sprites

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        if (self.next_direction[0] * -1, self.next_direction[1] * -1) != self.direction:
            self.direction = self.next_direction
        head = self.get_head_position()
        x, y = self.direction
        new_head = (head[0] + x, head[1] + y)
        if (new_head in self.positions[1:] or
            new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            return False
        self.positions.insert(0, new_head)
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False
        return True

    def _get_segment_type(self, i):
        if i == 0 or i == len(self.positions) - 1:
            return None
    
        prev_pos = self.positions[i-1]
        current_pos = self.positions[i]
        next_pos = self.positions[i+1]
    
        dx1 = current_pos[0] - prev_pos[0]
        dy1 = current_pos[1] - prev_pos[1]
        dx2 = next_pos[0] - current_pos[0]
        dy2 = next_pos[1] - current_pos[1]
    
        if dx1 != 0: dx1 = dx1 // abs(dx1)
        if dy1 != 0: dy1 = dy1 // abs(dy1)
        if dx2 != 0: dx2 = dx2 // abs(dx2)
        if dy2 != 0: dy2 = dy2 // abs(dy2)
    
        # Debug: imprimir valores en los giros
        if (dx1, dy1) != (dx2, dy2):
            print(f"DEBUG - Giro detectado en pos {current_pos}:")
            print(f"  Dirección anterior (dx1,dy1): ({dx1},{dy1})")
            print(f"  Dirección siguiente (dx2,dy2): ({dx2},{dy2})")

        # Segmentos rectos
        if (dx1, dy1) == (dx2, dy1):
            if dx1 != 0 and dy1 == 0:
                return 'body_h'  # 🠒🠒 o 🠐🠐
            elif dx1 == 0 and dy1 != 0:
                return 'body_v'  # 🠑🠑 o 🠓🠓
            else:
                return 'body'

        # Giros horizontales y verticales, cada uno con su condición separada y corregida
        # 🠒🠑 (derecha-arriba)
        if dx1 == 1 and dy1 == 0 and dx2 == 0 and dy2 == -1:
            return 'body_turn_up_right'  # derecha->arriba
        # 🠐🠑 (izquierda-arriba)
        if dx1 == -1 and dy1 == 0 and dx2 == 0 and dy2 == -1:
            return 'body_turn_up_left'  # izquierda->arriba
        # 🠒🠓 (derecha-abajo)
        if dx1 == 1 and dy1 == 0 and dx2 == 0 and dy2 == 1:
            return 'body_turn_down_right'  # derecha->abajo
        # 🠐🠓 (izquierda-abajo)
        if dx1 == -1 and dy1 == 0 and dx2 == 0 and dy2 == 1:
            return 'body_turn_down_left'  # izquierda->abajo
        # 🠑🠒 (arriba-derecha)
        if dx1 == 0 and dy1 == -1 and dx2 == 1 and dy2 == 0:
            return 'body_turn_down_right'  # arriba->derecha (corrige: antes era up_right)
        # 🠑🠐 (arriba-izquierda)
        if dx1 == 0 and dy1 == -1 and dx2 == -1 and dy2 == 0:
            return 'body_turn_down_left'  # arriba->izquierda (corrige: antes era up_left)
        # 🠓🠒 (abajo-derecha)
        if dx1 == 0 and dy1 == 1 and dx2 == 1 and dy2 == 0:
            return 'body_turn_up_right'  # abajo->derecha (corrige: antes era down_right)
        # 🠓🠐 (abajo-izquierda)
        if dx1 == 0 and dy1 == 1 and dx2 == -1 and dy2 == 0:
            return 'body_turn_up_left'  # abajo->izquierda (corrige: antes era down_left)

        print(f"ADVERTENCIA: Giro no detectado: ({dx1},{dy1}) -> ({dx2},{dy2}) en pos {current_pos}")
        return 'body'

    def render(self, surface):
        """
        Dibuja la serpiente en pantalla.
        - La cabeza y la cola usan sprites rotados según la dirección.
        - Los segmentos del cuerpo pueden ser rectos (horizontal 🠒🠐 o vertical 🠑🠓) o curvas.
        - Las curvas usan siempre el sprite 'body_turn_up_right' rotado según el tipo de giro.
        Casos de curvas (comentados con flechas):
            🠒🠑  (derecha-arriba)      -> 'body_turn_up_right',   rotación 0°
            🠒🠓  (derecha-abajo)       -> 'body_turn_down_right', rotación 90°
            🠐🠑  (izquierda-arriba)    -> 'body_turn_up_left',    rotación 270°
            🠐🠓  (izquierda-abajo)     -> 'body_turn_down_left',  rotación 180°
            🠑🠒  (arriba-derecha)      -> 'body_turn_up_right',   rotación 0°
            🠑🠐  (arriba-izquierda)    -> 'body_turn_up_left',    rotación 270°
            🠓🠒  (abajo-derecha)       -> 'body_turn_down_right', rotación 90°
            🠓🠐  (abajo-izquierda)     -> 'body_turn_down_left',  rotación 180°
        """
        for i, p in enumerate(self.positions):
            rect = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            if i == 0:
                # Cabeza: sprite rotado según dirección actual
                surface.blit(self.head_sprites[self.direction], rect)
            elif i == len(self.positions) - 1:
                # Cola: sprite rotado según dirección de la cola
                tail_direction = self._get_tail_direction()
                surface.blit(self.tail_sprites[tail_direction], rect)
            else:
                segment_type = self._get_segment_type(i)
                # --- Curvas ---
                # Usamos siempre el sprite 'body_turn_up_right' y lo rotamos según el tipo de giro
                # Ver comentarios arriba para entender cada caso
                angle = None
                if segment_type == 'body_turn_up_right':      # 🠒🠑 o 🠑🠒
                    angle = 0
                elif segment_type == 'body_turn_down_right':  # 🠒🠓 o 🠓🠒
                    angle = 90
                elif segment_type == 'body_turn_down_left':   # 🠐🠓 o 🠓🠐
                    angle = 180
                elif segment_type == 'body_turn_up_left':     # 🠐🠑 o 🠑🠐
                    angle = 270
                if angle is not None:
                    sprite = pygame.transform.rotate(SPRITES['body_turn_up_right'], angle)
                    surface.blit(sprite, rect)
                # --- Rectos ---
                elif segment_type == 'body_h':  # 🠒🠒 o 🠐🠐
                    surface.blit(SPRITES['body_h'], rect)
                elif segment_type == 'body_v':  # 🠑🠑 o 🠓🠓
                    surface.blit(SPRITES['body_v'], rect)
                else:
                    # Por defecto, usa el sprite de cuerpo normal
                    surface.blit(SPRITES['body'], rect)

    def _get_tail_direction(self):
        if len(self.positions) < 2:
            return RIGHT
        last = self.positions[-1]
        second_last = self.positions[-2]
        dx = second_last[0] - last[0]
        dy = second_last[1] - last[1]
        if abs(dx) > abs(dy):
            return RIGHT if dx > 0 else LEFT
        else:
            return DOWN if dy > 0 else UP

    def change_direction(self, direction):
        self.next_direction = direction

    def grow_snake(self):
        self.grow = True
