import pygame
import random
import sys
import time
import os
from pathlib import Path

# Inicializa pygame
pygame.init()

# Constantes de configuración de la ventana y el juego
WIDTH, HEIGHT = 600, 600  # Tamaño de la ventana
GRID_SIZE = 20             # Tamaño de cada celda de la cuadrícula
GRID_WIDTH = WIDTH // GRID_SIZE   # Número de celdas horizontales
GRID_HEIGHT = HEIGHT // GRID_SIZE # Número de celdas verticales
SNAKE_SPEED = 5         # Velocidad de la serpiente (frames por segundo)

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

# Variables globales para almacenar los sprites
SPRITES = {}

def create_default_sprites():
    """Crea sprites básicos para el juego si no existen"""
    # Crea el directorio assets si no existe
    assets_dir = Path('assets')
    assets_dir.mkdir(exist_ok=True)
    
    # Definir los sprites a crear
    sprites_to_create = {
        'snake_head.png': lambda: create_head_sprite(),
        'snake_body.png': lambda: create_body_sprite(GREEN),
        'snake_body_h.png': lambda: create_body_h_sprite(),
        'snake_body_v.png': lambda: create_body_v_sprite(),
        'snake_tail.png': lambda: create_tail_sprite(),
        'food.png': lambda: create_food_sprite(),
        'snake_body_turn_up_right.png': lambda: create_turn_sprite_up_right(),    # Rojo - Arriba-Derecha
        'snake_body_turn_up_left.png': lambda: create_turn_sprite_up_left(),      # Verde - Arriba-Izquierda
        'snake_body_turn_down_right.png': lambda: create_turn_sprite_down_right(),  # Azul - Abajo-Derecha
        'snake_body_turn_down_left.png': lambda: create_turn_sprite_down_left()     # Amarillo - Abajo-Izquierda
    }
    
    sprites_created = False
    
    # Crear cada sprite si no existe
    for filename, create_func in sprites_to_create.items():
        file_path = assets_dir / filename
        if not file_path.exists():
            surface = create_func()
            pygame.image.save(surface, str(file_path))
            print(f"Creado: {file_path}")
            sprites_created = True
    
    if sprites_created:
        print("Se han creado sprites básicos en la carpeta 'assets'.")
        print("Puedes reemplazarlos con tus propias imágenes más tarde.")

def create_head_sprite():
    """Crea un sprite triangular para la cabeza"""
    surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    # Triángulo amarillo apuntando a la derecha
    points = [(0, 0), (0, GRID_SIZE), (GRID_SIZE, GRID_SIZE // 2)]
    pygame.draw.polygon(surface, YELLOW, points)
    pygame.draw.polygon(surface, WHITE, points, 1)
    return surface

def create_body_sprite(color=GREEN):
    """Crea un sprite cuadrado para el cuerpo"""
    surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    rect = pygame.Rect(0, 0, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, WHITE, rect, 1)
    return surface

def create_body_h_sprite():
    """Crea un sprite rectangular horizontal para el cuerpo"""
    surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    # Rectángulo más ancho que alto
    rect = pygame.Rect(0, GRID_SIZE // 4, GRID_SIZE, GRID_SIZE // 2)
    pygame.draw.rect(surface, GREEN, rect)
    pygame.draw.rect(surface, WHITE, rect, 1)
    return surface

def create_body_v_sprite():
    """Crea un sprite rectangular vertical para el cuerpo"""
    surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    # Rectángulo más alto que ancho
    rect = pygame.Rect(GRID_SIZE // 4, 0, GRID_SIZE // 2, GRID_SIZE)
    pygame.draw.rect(surface, GREEN, rect)
    pygame.draw.rect(surface, WHITE, rect, 1)
    return surface

def create_tail_sprite():
    """Crea un sprite triangular para la cola"""
    surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    # Triángulo verde apuntando a la izquierda
    points = [(GRID_SIZE, 0), (GRID_SIZE, GRID_SIZE), (0, GRID_SIZE // 2)]
    pygame.draw.polygon(surface, GREEN, points)
    pygame.draw.polygon(surface, WHITE, points, 1)
    return surface

def create_food_sprite():
    """Crea un sprite circular para la comida"""
    surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(surface, RED, (GRID_SIZE // 2, GRID_SIZE // 2), GRID_SIZE // 2)
    pygame.draw.circle(surface, WHITE, (GRID_SIZE // 2, GRID_SIZE // 2), GRID_SIZE // 2, 1)
    return surface

def create_turn_sprite_up_right():
    """Crea un sprite para la curva arriba-derecha (rojo)"""
    surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    # Dibuja una forma de curva que va hacia arriba y a la derecha
    points = [
        (0, GRID_SIZE),              # Esquina inferior izquierda
        (0, GRID_SIZE // 2),         # Medio izquierdo
        (GRID_SIZE // 2, GRID_SIZE // 2), # Centro
        (GRID_SIZE // 2, 0),         # Medio superior
        (GRID_SIZE, 0),              # Esquina superior derecha
        (GRID_SIZE, GRID_SIZE // 2), # Medio derecho
        (GRID_SIZE // 2, GRID_SIZE), # Medio inferior
    ]
    pygame.draw.polygon(surface, (255, 0, 0), points)  # Rojo
    pygame.draw.polygon(surface, WHITE, points, 1)
    # Dibuja una flecha pequeña indicando la dirección
    pygame.draw.line(surface, WHITE, (GRID_SIZE // 4, GRID_SIZE // 2), (GRID_SIZE // 2, GRID_SIZE // 4), 2)
    pygame.draw.line(surface, WHITE, (GRID_SIZE // 2, GRID_SIZE // 4), (GRID_SIZE * 3 // 4, GRID_SIZE // 2), 2)
    return surface

def create_turn_sprite_up_left():
    """Crea un sprite para la curva arriba-izquierda (verde)"""
    surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    # Dibuja una forma de curva que va hacia arriba y a la izquierda
    points = [
        (0, 0),                      # Esquina superior izquierda
        (GRID_SIZE // 2, 0),         # Medio superior
        (GRID_SIZE // 2, GRID_SIZE // 2), # Centro
        (GRID_SIZE, GRID_SIZE // 2), # Medio derecho
        (GRID_SIZE, GRID_SIZE),      # Esquina inferior derecha
        (GRID_SIZE // 2, GRID_SIZE), # Medio inferior
        (GRID_SIZE // 2, GRID_SIZE // 2), # Centro
        (0, GRID_SIZE // 2),         # Medio izquierdo
    ]
    pygame.draw.polygon(surface, (0, 255, 0), points)  # Verde
    pygame.draw.polygon(surface, WHITE, points, 1)
    # Dibuja una flecha pequeña indicando la dirección
    pygame.draw.line(surface, WHITE, (GRID_SIZE * 3 // 4, GRID_SIZE // 2), (GRID_SIZE // 2, GRID_SIZE // 4), 2)
    pygame.draw.line(surface, WHITE, (GRID_SIZE // 2, GRID_SIZE // 4), (GRID_SIZE // 4, GRID_SIZE // 2), 2)
    return surface

def create_turn_sprite_down_right():
    """Crea un sprite para la curva abajo-derecha (azul)"""
    surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    # Dibuja una forma de curva que va hacia abajo y a la derecha
    points = [
        (0, 0),                      # Esquina superior izquierda
        (0, GRID_SIZE // 2),         # Medio izquierdo
        (GRID_SIZE // 2, GRID_SIZE // 2), # Centro
        (GRID_SIZE // 2, GRID_SIZE), # Medio inferior
        (GRID_SIZE, GRID_SIZE),      # Esquina inferior derecha
        (GRID_SIZE, GRID_SIZE // 2), # Medio derecho
        (GRID_SIZE // 2, GRID_SIZE // 2), # Centro
        (GRID_SIZE // 2, 0),         # Medio superior
    ]
    pygame.draw.polygon(surface, (0, 0, 255), points)  # Azul
    pygame.draw.polygon(surface, WHITE, points, 1)
    # Dibuja una flecha pequeña indicando la dirección
    pygame.draw.line(surface, WHITE, (GRID_SIZE // 4, GRID_SIZE // 2), (GRID_SIZE // 2, GRID_SIZE * 3 // 4), 2)
    pygame.draw.line(surface, WHITE, (GRID_SIZE // 2, GRID_SIZE * 3 // 4), (GRID_SIZE * 3 // 4, GRID_SIZE // 2), 2)
    return surface

def create_turn_sprite_down_left():
    """Crea un sprite para la curva abajo-izquierda (amarillo)"""
    surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    # Dibuja una forma de curva que va hacia abajo y a la izquierda
    points = [
        (0, GRID_SIZE),              # Esquina inferior izquierda
        (GRID_SIZE // 2, GRID_SIZE), # Medio inferior
        (GRID_SIZE // 2, GRID_SIZE // 2), # Centro
        (GRID_SIZE, GRID_SIZE // 2), # Medio derecho
        (GRID_SIZE, 0),              # Esquina superior derecha
        (GRID_SIZE // 2, 0),         # Medio superior
        (GRID_SIZE // 2, GRID_SIZE // 2), # Centro
        (0, GRID_SIZE // 2),         # Medio izquierdo
    ]
    pygame.draw.polygon(surface, (255, 255, 0), points)  # Amarillo
    pygame.draw.polygon(surface, WHITE, points, 1)
    # Dibuja una flecha pequeña indicando la dirección
    pygame.draw.line(surface, WHITE, (GRID_SIZE * 3 // 4, GRID_SIZE // 2), (GRID_SIZE // 2, GRID_SIZE * 3 // 4), 2)
    pygame.draw.line(surface, WHITE, (GRID_SIZE // 2, GRID_SIZE * 3 // 4), (GRID_SIZE // 4, GRID_SIZE // 2), 2)
    return surface

def load_sprites():
    """Carga los sprites necesarios para el juego"""
    global SPRITES
    
    # Rutas de los sprites
    sprites_paths = {
        'head': os.path.join('assets', 'snake_head.png'),
        'body': os.path.join('assets', 'snake_body.png'),
        'body_h': os.path.join('assets', 'snake_body_h.png'),
        'body_v': os.path.join('assets', 'snake_body_v.png'),
        'tail': os.path.join('assets', 'snake_tail.png'),
        'food': os.path.join('assets', 'food.png'),
        'body_turn_up_right': os.path.join('assets', 'snake_body_turn_up_right.png'),
        'body_turn_up_left': os.path.join('assets', 'snake_body_turn_up_left.png'),
        'body_turn_down_right': os.path.join('assets', 'snake_body_turn_down_right.png'),
        'body_turn_down_left': os.path.join('assets', 'snake_body_turn_down_left.png')
    }
    
    # Colores de depuración para las vueltas
    turn_debug_colors = {
        'body_turn_up_right': (255, 0, 0),      # Rojo
        'body_turn_up_left': (0, 255, 0),       # Verde
        'body_turn_down_right': (0, 0, 255),    # Azul
        'body_turn_down_left': (255, 255, 0)    # Amarillo
    }
    
    # Verifica si los sprites existen, si no, crea sprites de reserva
    for name, path in sprites_paths.items():
        try:
            # Intenta cargar la imagen
            sprite = pygame.image.load(path).convert_alpha()
            # Redimensiona al tamaño de la cuadrícula
            SPRITES[name] = pygame.transform.scale(sprite, (GRID_SIZE, GRID_SIZE))
        except pygame.error:
            # Si la imagen no existe, crea un surface como reserva
            surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
            
            if name == 'head':
                # Círculo amarillo para la cabeza
                pygame.draw.circle(surface, YELLOW, (GRID_SIZE//2, GRID_SIZE//2), GRID_SIZE//2)
                pygame.draw.circle(surface, WHITE, (GRID_SIZE//2, GRID_SIZE//2), GRID_SIZE//2, 1)
            elif name == 'tail':
                # Círculo verde para la cola
                pygame.draw.circle(surface, GREEN, (GRID_SIZE//2, GRID_SIZE//2), GRID_SIZE//2)
                pygame.draw.circle(surface, WHITE, (GRID_SIZE//2, GRID_SIZE//2), GRID_SIZE//2, 1)
            elif name == 'body' or name == 'body_h' or name == 'body_v':
                # Cuadrado verde para el cuerpo
                pygame.draw.rect(surface, GREEN, pygame.Rect(0, 0, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, WHITE, pygame.Rect(0, 0, GRID_SIZE, GRID_SIZE), 1)
            elif name.startswith('body_turn'):
                # Usa colores de depuración para las curvas
                color = turn_debug_colors.get(name, GREEN)
                pygame.draw.rect(surface, color, pygame.Rect(0, 0, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, WHITE, pygame.Rect(0, 0, GRID_SIZE, GRID_SIZE), 1)
            elif name == 'food':
                # Círculo rojo para la comida
                pygame.draw.circle(surface, RED, (GRID_SIZE//2, GRID_SIZE//2), GRID_SIZE//2)
                pygame.draw.circle(surface, WHITE, (GRID_SIZE//2, GRID_SIZE//2), GRID_SIZE//2, 1)
                
            SPRITES[name] = surface
            print(f"Aviso: No se pudo cargar {path}, usando sprite de reserva.")
    
    # Elimina los sprites antiguos que puedan estar causando problemas
    sprites_missing = False
    for name, path in sprites_paths.items():
        if name.startswith('body_turn') and not os.path.exists(path):
            sprites_missing = True
    
    if sprites_missing:
        print("Recreando sprites de curvas...")
        # Elimina los sprites existentes para forzar recreación
        assets_dir = os.path.join('assets')
        for file in os.listdir(assets_dir):
            if file.startswith('snake_body_turn'):
                try:
                    os.remove(os.path.join(assets_dir, file))
                    print(f"Eliminado: {file}")
                except:
                    pass
        print("Ejecuta el juego de nuevo para crear los sprites nuevos.")

class Snake:
    def __init__(self):
        # La serpiente inicia en el centro de la pantalla
        # Inicializa con dos unidades: cabeza y un segmento de cuerpo
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2), (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2)]
        self.direction = RIGHT         # Dirección actual
        self.next_direction = RIGHT   # Próxima dirección (para evitar reversa instantánea)
        self.grow = False             # Indica si debe crecer en la siguiente actualización
        
        # Copias de los sprites con rotaciones específicas
        self.head_sprites = self._create_rotated_sprites('head')
        self.tail_sprites = self._create_rotated_sprites('tail')
    
    def _create_rotated_sprites(self, sprite_name):
        """Crea versiones rotadas de un sprite para cada dirección"""
        sprites = {}
        base_sprite = SPRITES[sprite_name]
        
        # Rotaciones para cada dirección
        sprites[RIGHT] = base_sprite
        sprites[DOWN] = pygame.transform.rotate(base_sprite, 270)
        sprites[LEFT] = pygame.transform.rotate(base_sprite, 180)
        sprites[UP] = pygame.transform.rotate(base_sprite, 90)
        
        return sprites
        
    def get_head_position(self):
        # Devuelve la posición de la cabeza de la serpiente
        return self.positions[0]
    
    def update(self):
        # Cambia la dirección solo si no es la opuesta a la actual
        if (self.next_direction[0] * -1, self.next_direction[1] * -1) != self.direction:
            self.direction = self.next_direction
        
        head = self.get_head_position()
        x, y = self.direction
        new_head = (head[0] + x, head[1] + y)  # Calcula la nueva posición de la cabeza
        
        # Verifica colisión con el cuerpo o los bordes (fin del juego)
        if (new_head in self.positions[1:] or
            new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            return False
        
        self.positions.insert(0, new_head)  # Mueve la cabeza a la nueva posición
        
        if not self.grow:
            self.positions.pop()  # Elimina la última parte de la cola si no debe crecer
        else:
            self.grow = False     # Si debe crecer, mantiene la cola y resetea el flag
            
        return True  # Movimiento exitoso
    
    def _get_segment_type(self, i):
        """Determina el tipo de segmento y su orientación"""
        # Si es la cabeza o la cola, no es una curva
        if i == 0 or i == len(self.positions) - 1:
            return None
        
        # Necesitamos 3 posiciones para determinar si hay una curva
        prev_pos = self.positions[i-1]  # Segmento anterior
        current_pos = self.positions[i]  # Segmento actual
        next_pos = self.positions[i+1]  # Segmento siguiente
        
        # Obtiene las direcciones entre los segmentos
        # De anterior a actual
        dx1 = current_pos[0] - prev_pos[0]
        dy1 = current_pos[1] - prev_pos[1]
        
        # De actual a siguiente
        dx2 = next_pos[0] - current_pos[0]
        dy2 = next_pos[1] - current_pos[1]
        
        # Normaliza las direcciones
        if dx1 != 0:
            dx1 = dx1 // abs(dx1)
        if dy1 != 0:
            dy1 = dy1 // abs(dy1)
        if dx2 != 0:
            dx2 = dx2 // abs(dx2)
        if dy2 != 0:
            dy2 = dy2 // abs(dy2)
        
        # Comprueba si hay cambio de dirección
        if (dx1, dy1) == (dx2, dy2):
            # No hay curva, es un segmento recto
            # Determina si es horizontal o vertical
            if dx1 != 0 and dy1 == 0:  # Movimiento horizontal
                return 'body_h'
            elif dx1 == 0 and dy1 != 0:  # Movimiento vertical
                return 'body_v'
            else:
                return 'body'  # Caso por defecto (no debería ocurrir)
        
        # Determina el tipo de curva basado en la dirección
        # Nombres de las curvas:
        # - up_right: Sube y gira a la derecha (o viene de la izquierda y sube)
        # - up_left: Sube y gira a la izquierda (o viene de la derecha y sube)
        # - down_right: Baja y gira a la derecha (o viene de la izquierda y baja)
        # - down_left: Baja y gira a la izquierda (o viene de la derecha y baja)
        
        # Casos donde viene de izquierda/derecha y sube/baja
        if (dx1, dy1) == (1, 0) and (dx2, dy2) == (0, -1):  # Derecha -> Arriba
            return 'body_turn_up_right'
        elif (dx1, dy1) == (1, 0) and (dx2, dy2) == (0, 1):  # Derecha -> Abajo
            return 'body_turn_down_right'
        elif (dx1, dy1) == (-1, 0) and (dx2, dy2) == (0, -1):  # Izquierda -> Arriba
            return 'body_turn_up_left'
        elif (dx1, dy1) == (-1, 0) and (dx2, dy2) == (0, 1):  # Izquierda -> Abajo
            return 'body_turn_down_left'
        
        # Casos donde viene de arriba/abajo y va a izquierda/derecha
        elif (dx1, dy1) == (0, -1) and (dx2, dy2) == (1, 0):  # Arriba -> Derecha
            return 'body_turn_up_right'
        elif (dx1, dy1) == (0, -1) and (dx2, dy2) == (-1, 0):  # Arriba -> Izquierda
            return 'body_turn_up_left'
        elif (dx1, dy1) == (0, 1) and (dx2, dy2) == (1, 0):  # Abajo -> Derecha
            return 'body_turn_down_right'
        elif (dx1, dy1) == (0, 1) and (dx2, dy2) == (-1, 0):  # Abajo -> Izquierda
            return 'body_turn_down_left'
        
        # Si llegamos aquí, es un caso extraño que no deberíamos ver
        print(f"¡Caso de curva no detectado!: ({dx1},{dy1}) -> ({dx2},{dy2})")
        return 'body'
    
    def render(self, surface):
        """Dibuja la serpiente usando sprites"""
        for i, p in enumerate(self.positions):
            rect = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            
            if i == 0:  # Es la cabeza
                # Usa el sprite de cabeza rotado según la dirección
                surface.blit(self.head_sprites[self.direction], rect)
            elif i == len(self.positions) - 1:  # Es la cola
                # Calcula la dirección de la cola
                tail_direction = self._get_tail_direction()
                surface.blit(self.tail_sprites[tail_direction], rect)
            else:  # Es un segmento del cuerpo
                # Determina si es una curva, un segmento horizontal o vertical
                segment_type = self._get_segment_type(i)
                if segment_type and segment_type in SPRITES:
                    surface.blit(SPRITES[segment_type], rect)
                else:
                    # Si no podemos determinar el tipo o no tenemos el sprite, usamos el predeterminado
                    surface.blit(SPRITES['body'], rect)
    
    def _get_tail_direction(self):
        """Determina la dirección de la cola basándose en el penúltimo segmento"""
        if len(self.positions) < 2:
            return RIGHT  # Dirección por defecto
        
        # Obtiene las posiciones de los últimos dos segmentos
        last = self.positions[-1]
        second_last = self.positions[-2]
        
        # Calcula la dirección desde el último hacia el penúltimo
        dx = second_last[0] - last[0]
        dy = second_last[1] - last[1]
        
        # Asegura que solo se mueva en una dirección (horizontal o vertical)
        if abs(dx) > abs(dy):
            return RIGHT if dx > 0 else LEFT
        else:
            return DOWN if dy > 0 else UP
    
    def change_direction(self, direction):
        # Cambia la dirección de movimiento (si es válida)
        self.next_direction = direction
        
    def grow_snake(self):
        # Indica que la serpiente debe crecer en la próxima actualización
        self.grow = True

class Food:
    def __init__(self, snake_positions):
        # Coloca la comida en una posición aleatoria que no ocupe la serpiente
        self.position = self.get_random_position(snake_positions)
        
    def get_random_position(self, snake_positions):
        # Busca una posición aleatoria libre en la cuadrícula
        position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        while position in snake_positions:
            position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        return position
    
    def render(self, surface):
        # Dibuja la comida en pantalla usando el sprite
        rect = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
        surface.blit(SPRITES['food'], rect)
        
def main():
    clock = pygame.time.Clock()  # Controla la velocidad del juego
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Crea la ventana
    pygame.display.set_caption('Snake Game')
    
    # Crea sprites por defecto si no existen y luego carga los sprites
    create_default_sprites()
    load_sprites()
    
    # Si hay sprites que no existen, forzar recreación
    missing_sprites = False
    for path in [os.path.join('assets', f'snake_body_turn_{direction}_{side}.png') 
                for direction in ['up', 'down'] for side in ['left', 'right']]:
        if not os.path.exists(path):
            missing_sprites = True
    
    if missing_sprites:
        # Elimina todos los sprites para forzar recreación
        import shutil
        assets_dir = 'assets'
        if os.path.exists(assets_dir):
            for file in os.listdir(assets_dir):
                if file.startswith('snake_body_turn'):
                    try:
                        os.remove(os.path.join(assets_dir, file))
                    except:
                        pass
        # Vuelve a crear los sprites
        create_default_sprites()
        load_sprites()
    
    font = pygame.font.SysFont('Arial', 25)  # Fuente para mostrar texto
    
    snake = Snake()  # Crea la serpiente
    food = Food(snake.positions)  # Crea la comida
    
    score = 0
    game_over = False
    
    while True:
        # Manejo de eventos (teclado, cerrar ventana, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_SPACE:
                        # Reinicia el juego
                        snake = Snake()
                        food = Food(snake.positions)
                        score = 0
                        game_over = False
                else:
                    # Cambia la dirección según la tecla presionada
                    if event.key == pygame.K_UP:
                        snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction(RIGHT)
        
        if not game_over:
            # Actualiza la posición de la serpiente
            if not snake.update():
                game_over = True  # Si colisiona, termina el juego
                
            # Verifica si la serpiente come la comida
            if snake.get_head_position() == food.position:
                snake.grow_snake()  # La serpiente crece
                food = Food(snake.positions)  # Nueva comida
                score += 1  # Aumenta el puntaje
                
            # La colisión con la pared ya se maneja en snake.update()
                
        # Dibuja todos los elementos en pantalla
        screen.fill(BLACK)  # Fondo negro
        
        snake.render(screen)  # Dibuja la serpiente
        food.render(screen)   # Dibuja la comida
        
        # Dibuja el puntaje
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (5, 5))
        
        if game_over:
            # Muestra mensaje de Game Over
            game_over_text = font.render("Game Over! Press SPACE to restart", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
        
        pygame.display.update()  # Actualiza la pantalla
        clock.tick(SNAKE_SPEED)  # Controla la velocidad del juego

if __name__ == "__main__":
    main()

