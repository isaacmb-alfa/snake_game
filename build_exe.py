import os
import sys
import shutil
import subprocess
from pathlib import Path

# === CONFIGURACIÓN ===
icon = "snake.ico"
main = "launcher.py"
assets = "game/assets"
dist = Path("dist")
exe_name = "Snake Game-DevCreador.exe"
portable_folder = dist / "snake_portable"
portable_exe = portable_folder / exe_name
installer = dist / "Snake Game Installer.exe"
rar_comment = dist / "comment.txt"  # ahora se generará aquí
winrar = Path("C:/Program Files/WinRAR/WinRAR.exe")

# === GENERAR comment.txt ===
comment_content = f"""\
;The comment below contains SFX script commands
Path=SnakePortable
SavePath
Setup="{exe_name}"
Silent=0
Overwrite=1
Title=Snake Game - DevCreador
"""


# === VERIFICACIONES INICIALES ===
if not Path(icon).exists():
    raise FileNotFoundError(f"Icono '{icon}' no encontrado.")
if not Path(main).exists():
    raise FileNotFoundError(f"Archivo principal '{main}' no encontrado.")
if not Path(assets).exists():
    raise FileNotFoundError(f"Assets '{assets}' no encontrados.")
if not winrar.exists():
    raise FileNotFoundError("⚠️ WinRAR no encontrado en la ruta especificada.")

# === LIMPIAR CARPETAS ANTERIORES ===
for folder in ["dist", "build", "__pycache__"]:
    if Path(folder).exists():
        shutil.rmtree(folder)
        
# === CREAR comment.txt ===
dist.mkdir(parents=True, exist_ok=True)  # por si aún no existe
rar_comment.write_text(comment_content, encoding='utf-8')
print(f"📝 Archivo 'comment.txt' generado en: {rar_comment.resolve()}")

# === COMPILAR CON PYINSTALLER ===
subprocess.run([
    sys.executable, "-m", "PyInstaller", "--noconfirm", "--onefile", "--windowed",
    f"--icon={icon}",
    f"--add-data={assets};game/assets",
    f"--name={exe_name.replace('.exe', '')}",
    main
], check=True)

# === VERIFICAR QUE SE CREÓ EL EXE ===
exe_path = dist / exe_name
if not exe_path.exists():
    raise FileNotFoundError(f"❌ No se encontró el archivo {exe_path}")

# === COPIAR EL EXE A CARPETA PORTÁTIL ===
portable_folder.mkdir(parents=True, exist_ok=True)
shutil.copy(exe_path, portable_exe)
print(f"✅ .exe copiado correctamente a carpeta '{portable_folder.name}'.")

# === CREAR INSTALADOR AUTOEXTRAÍBLE ===
print("\n📦 Archivos que se incluirán en el instalador:")
print(f"  - {portable_exe}")

print("\n⚙️ Creando autoextraíble con WinRAR...\n")

command = [
    str(winrar), "a", "-r", "-sfx",
    "-ep1",  # evita almacenar rutas
    f"-z{rar_comment.resolve()}",
    f"-iicon{Path(icon).resolve()}",
    str(installer.resolve()),
    str(exe_name)
]

print("🛠️ Comando que se ejecutará:")
print(" ".join(f'"{arg}"' if " " in arg else arg for arg in command))

try:
    subprocess.run(command, check=True, cwd=portable_folder)
    print("\n✅ Instalador autoextraíble creado con éxito en:")
    print(f"   {installer}")
except subprocess.CalledProcessError as e:
    print("\n❌ Error al crear el instalador con WinRAR.")
    print("Código de error:", e.returncode)
