# build_exe.ps1
# Script de PowerShell para compilar el juego Snake a un .exe con icono personalizado

# Cambia el nombre del icono aquí si usas otro
$icon = "snake.ico"
$main = "main.py"

# Verifica que el icono existe
if (!(Test-Path $icon)) {
    Write-Host "[ERROR] No se encontró el icono $icon. Coloca el archivo .ico en la raíz del proyecto."
    exit 1
}

# Instala pyinstaller si no está instalado
if (-not (pip show pyinstaller 2>$null)) {
    Write-Host "Instalando pyinstaller..."
    pip install pyinstaller
}

# Ejecuta pyinstaller
Write-Host "Compilando $main a .exe con icono $icon..."
pyinstaller --onefile --windowed --icon=$icon $main

Write-Host "\n¡Compilación finalizada! El ejecutable está en la carpeta dist/"
Write-Host "Recuerda copiar la carpeta 'assets' junto al .exe para que el juego funcione correctamente."

# Copia la carpeta assets junto al .exe (sin __pycache__)
$distPath = Join-Path -Path $PSScriptRoot -ChildPath "dist"
$exeName = "main.exe"
$exePath = Join-Path -Path $distPath -ChildPath $exeName

# Copia assets si no existe
if (!(Test-Path "$distPath/assets")) {
    Copy-Item -Path "assets" -Destination $distPath -Recurse
}

# Copia la carpeta snake (sin __pycache__)
if (!(Test-Path "$distPath/snake")) {
    Copy-Item -Path "snake" -Destination $distPath -Recurse
    Remove-Item -Path "$distPath/snake/__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host "¡Listo! Ejecuta $exeName desde la carpeta dist/ y tendrás todo lo necesario."
