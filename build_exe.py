import os
import sys
import shutil
import subprocess
import glob
from pathlib import Path

icon = "snake.ico"
main = "game/main.py"
assets = "game/assets"
dist = Path("dist")
exe_name = "Snake Game-DevCreador.exe"
portable_folder = dist / "snake_portable"
installer = dist / exe_name
rar_comment = "comment.txt"
winrar = r"C:\Program Files\WinRAR\WinRAR.exe"

# Verificar paths
if not Path(icon).exists():
    raise FileNotFoundError(f"Icono '{icon}' no encontrado.")
if not Path(main).exists():
    raise FileNotFoundError(f"Archivo principal '{main}' no encontrado.")
if not Path(assets).exists():
    raise FileNotFoundError(f"Assets '{assets}' no encontrados.")

# Limpiar carpetas viejas
for folder in ["dist", "build", "__pycache__"]:
    if Path(folder).exists():
        shutil.rmtree(folder)

# Ejecutar PyInstaller
subprocess.run([
    sys.executable, "-m", "PyInstaller", "--noconfirm", "--onefile", "--windowed",
    f"--icon={icon}",
    f"--add-data={assets};game/assets",
    f"--name=Snake Game-DevCreador",
    main
], check=True)

# Verifica que el EXE se haya generado
exe_path = dist / exe_name
if not exe_path.exists():
    raise FileNotFoundError(f"⚠️ No se encontró el archivo {exe_path}")

# Crear carpeta portable
if portable_folder.exists():
    shutil.rmtree(portable_folder)
portable_folder.mkdir(parents=True)

# Copiar EXE
shutil.copy(exe_path, portable_folder)
print("✅ .exe copiado correctamente a carpeta portable.")

# Crear instalador autoextraíble con WinRAR
if Path(winrar).exists():
    try:
        icon_path = Path(icon).resolve()
        comment_path = Path(rar_comment).resolve()
        output_path = installer.resolve()

        subprocess.run([
            winrar, "a", "-r", "-sfx",
            f"-z{comment_path}",
            f"-iicon{icon_path}",
            str(output_path),
            *[str(f.resolve()) for f in portable_folder.glob("*")]
        ], check=True)

        print("✅ Instalador creado con éxito.")
    except subprocess.CalledProcessError as e:
        print("❌ Error al crear el instalador con WinRAR.")
        print("Código de error:", e.returncode)
else:
    print("⚠️ WinRAR no encontrado.")

