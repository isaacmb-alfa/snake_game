import subprocess
from pathlib import Path
import shutil

# Rutas
project_root = Path(__file__).parent.resolve()
dist = project_root / "dist"
portable_folder = dist / "SnakePortable"
icon = project_root / "snake.ico"
comment = project_root / "comment.txt"
exe_name = "Snake Game-DevCreador.exe"
exe_source = dist / exe_name
exe_target = portable_folder / exe_name
installer = dist / "Snake Game Installer.exe"
winrar = Path("C:/Program Files/WinRAR/WinRAR.exe")

print("📦 Verificando archivos requeridos...")

# Asegurar carpeta portátil
portable_folder.mkdir(parents=True, exist_ok=True)

# Copiar EXE a la carpeta portable
if exe_source.exists():
    shutil.copy(exe_source, exe_target)
    print(f"✅ .exe copiado correctamente a carpeta '{portable_folder.name}'.")
else:
    print("❌ No se encontró el archivo .exe para empaquetar.")
    exit(1)

# Comando WinRAR
print("\n📄 Archivos que se incluirán en el instalador:")
print(f"  - {exe_target}")

print("\n⚙️ Creando autoextraíble con WinRAR...\n")

command = [
    str(winrar), "a", "-r", "-sfx",
    "-ep1",  # <- Aquí el cambio CLAVE para no guardar rutas
    f"-z{comment.resolve()}",
    f"-iicon{icon.resolve()}",
    str(installer.resolve()),
    str(exe_target.name)
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
