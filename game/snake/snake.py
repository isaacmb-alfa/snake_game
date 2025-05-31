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

        # Dirección de entrada (de prev a current)
        dx_in = current_pos[0] - prev_pos[0]
        dy_in = current_pos[1] - prev_pos[1]
        # Dirección de salida (de current a next)
        dx_out = next_pos[0] - current_pos[0]
        dy_out = next_pos[1] - current_pos[1]

        # Normalizar a -1, 0, 1
        if dx_in != 0: dx_in = dx_in // abs(dx_in)
        if dy_in != 0: dy_in = dy_in // abs(dy_in)
        if dx_out != 0: dx_out = dx_out // abs(dx_out)
        if dy_out != 0: dy_out = dy_out // abs(dy_out)

        # Rectos
        if (dx_in, dy_in) == (dx_out, dy_out):
            if dx_in != 0 and dy_in == 0:
                return 'body_h'  # Horizontal
            elif dx_in == 0 and dy_in != 0:
                return 'body_v'  # Vertical
            else:
                return 'body'

        # Mapear (entrada, salida) a sprite de curva
        # Ahora hay 8 sprites distintos para los 8 giros posibles
        turns = {
            # Derecha -> Arriba
            ((1,0),(0,-1)): 'body_turn_right_up',
            # Arriba -> Derecha
            ((0,-1),(1,0)): 'body_turn_up_right',
            # Izquierda -> Arriba
            ((-1,0),(0,-1)): 'body_turn_left_up',
            # Arriba -> Izquierda
            ((0,-1),(-1,0)): 'body_turn_up_left',
            # Derecha -> Abajo
            ((1,0),(0,1)): 'body_turn_right_down',
            # Abajo -> Derecha
            ((0,1),(1,0)): 'body_turn_down_right',
            # Izquierda -> Abajo
            ((-1,0),(0,1)): 'body_turn_left_down',
            # Abajo -> Izquierda
            ((0,1),(-1,0)): 'body_turn_down_left',
        }
        key = ((dx_in, dy_in), (dx_out, dy_out))
        if key in turns:
            return turns[key]
        # Si no está, prueba la inversa (por seguridad)
        key_inv = ((dx_out, dy_out), (dx_in, dy_in))
        if key_inv in turns:
            return turns[key_inv]

        print(f"ADVERTENCIA: Giro no detectado: entrada ({dx_in},{dy_in}) salida ({dx_out},{dy_out}) en pos {current_pos}")
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
                # --- Curvas: ahora hay 8 tipos ---
                if segment_type in [
                    'body_turn_right_up',
                    'body_turn_up_right',
                    'body_turn_left_up',
                    'body_turn_up_left',
                    'body_turn_right_down',
                    'body_turn_down_right',
                    'body_turn_left_down',
                    'body_turn_down_left',
                ]:
                    surface.blit(SPRITES[segment_type], rect)
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
