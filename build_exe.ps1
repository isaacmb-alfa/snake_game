# build_exe.ps1
# Script de PowerShell para compilar el juego Snake a un .exe con icono personalizado y crear un instalador autoextraíble

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

# Prepara carpeta portable
$distPath = Join-Path -Path $PSScriptRoot -ChildPath "dist"
$portablePath = Join-Path -Path $distPath -ChildPath "snake_portable"
$exeName = "main.exe"
$exePath = Join-Path -Path $distPath -ChildPath $exeName

# Limpia carpeta portable si existe
if (Test-Path $portablePath) { Remove-Item -Path $portablePath -Recurse -Force }
New-Item -ItemType Directory -Path $portablePath | Out-Null

# Copia el .exe
Copy-Item -Path $exePath -Destination $portablePath
# Copia assets
Copy-Item -Path "assets" -Destination $portablePath -Recurse
# Copia snake (sin __pycache__)
Copy-Item -Path "snake" -Destination $portablePath -Recurse
Remove-Item -Path "$portablePath/snake/__pycache__" -Recurse -Force -ErrorAction SilentlyContinue

# Crea el instalador autoextraíble usando 7-Zip (debe estar en el PATH)
$installerName = "snake_installer.exe"
$installerPath = Join-Path -Path $distPath -ChildPath $installerName

if (Get-Command 7z -ErrorAction SilentlyContinue) {
    Write-Host "Creando instalador autoextraíble..."
    Push-Location $distPath
    7z a -r -sfx"C:\Program Files\7-Zip\7z.sfx" $installerName "snake_portable/*"
    Pop-Location
    Write-Host "\n¡Instalador creado! Ejecuta $installerName y elige la carpeta de destino para extraer el juego."
    Write-Host "Puedes borrar la carpeta snake_portable si lo deseas."
} else {
    Write-Host "[ADVERTENCIA] 7-Zip no está instalado o no está en el PATH. Instala 7-Zip y agrega '7z' al PATH para crear el instalador autoextraíble."
    Write-Host "El juego portable está en dist/snake_portable/"
}

Write-Host "\n¡Listo! Ejecuta el instalador o usa la carpeta portable para jugar."
