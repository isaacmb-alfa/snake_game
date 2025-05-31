# Snake Game 🐍

Juego clásico de Snake hecho en Python con Pygame.

---

## 📦 Estructura del proyecto

```
snake_game/
│
├── game/                  # Código fuente y recursos
│   ├── main.py            # Punto de entrada
│   ├── snake/             # Módulos del juego
│   ├── assets/
│   │   ├── img/           # Sprites e imágenes
│   │   └── sounds/        # (opcional) Sonidos
│   └── ...
├── build_exe.ps1          # Script para compilar y empaquetar
├── snake.ico              # Icono del juego
├── .gitignore             # Archivos/carpetas a ignorar en git
└── README.md              # (este archivo)
```

---

## 🚀 Cómo jugar

1. Instala las dependencias:
   ```
   pip install pygame
   ```
2. Ejecuta el juego:
   ```
   cd game
   python main.py
   ```

### Controles
- Flechas: Mover la serpiente
- Espacio: Reiniciar tras perder

---

## 🛠️ Cómo compilar a .exe y crear instalador portable

1. **Coloca tu icono personalizado** como `snake.ico` en la raíz del proyecto.
2. **Ejecuta el script de build:**
   - Abre PowerShell en la carpeta raíz del proyecto.
   - Ejecuta:
     ```
     ./build_exe.ps1
     ```
   - Esto generará:
     - Un ejecutable `main.exe` en `dist/`
     - Una carpeta portable `dist/snake_portable/` con todo lo necesario
     - Un instalador autoextraíble `dist/snake_installer.exe` (requiere 7-Zip instalado y en el PATH)

3. **Distribución:**
   - Puedes compartir la carpeta `snake_portable/` o el instalador `snake_installer.exe`.
   - El usuario solo debe ejecutar `main.exe` para jugar.

---

## 📝 Notas de desarrollo
- Todos los recursos (sprites, sonidos) deben ir en `game/assets/img/` o `game/assets/sounds/`.
- El código fuente está en `game/snake/` y el punto de entrada es `game/main.py`.
- El script de build limpia y empaqueta todo automáticamente.
- No subas a git las carpetas `build/`, `dist/`, `snake_portable/`, ni archivos generados automáticamente.

---

## 🐍 Créditos
- Código y arte: DevCreador
- Motor: [Pygame](https://www.pygame.org/)

---

¡Disfruta programando y jugando!
