# build_exe.ps1 - Compila el juego Snake a .exe y crea un instalador portable

# CONFIGURACIÓN
$icon = "snake.ico"
$main = "game/main.py"
$assetsPath = "game/assets"
$distPath = "dist"
$exeName = "Snake Game-DevCreador.exe"
$portableFolder = "snake_portable"
$rarCommentFile = "comment.txt"   # Contiene configuración del extractor WinRAR
$installerName = "Snake Game-DevCreador.exe"
$installerPath = Join-Path $distPath $installerName

# COMPROBACIONES INICIALES
if (!(Test-Path $icon)) {
    Write-Host "[ERROR] No se encontró el icono '$icon'. Coloca el archivo .ico en la raíz del proyecto." -ForegroundColor Red
    exit 1
}
if (!(Test-Path $main)) {
    Write-Host "[ERROR] No se encontró el archivo principal '$main'. Revisa la ruta." -ForegroundColor Red
    exit 1
}
if (!(Test-Path $assetsPath)) {
    Write-Host "[ERROR] No se encontró la carpeta de assets '$assetsPath'." -ForegroundColor Red
    exit 1
}

# INSTALAR PYINSTALLER SI FALTA
Write-Host "Verificando PyInstaller..."
if (-not (Get-Command pyinstaller -ErrorAction SilentlyContinue)) {
    Write-Host "Instalando pyinstaller..."
    try {
        pip install pyinstaller
    }
    catch {
        Write-Host "[ERROR] Falló la instalación de PyInstaller. Asegúrate de que pip esté en tu PATH." -ForegroundColor Red
        exit 1
    }
}
else {
    Write-Host "PyInstaller ya está instalado."
}


# EMPAQUETADO CON PYINSTALLER
Write-Host "Compilando $main a .exe..."
try {
    # Asegúrate de que los paths sean absolutos o relativos al script si es necesario
    # PyInstaller requiere paths absolutos para --add-data si el script se ejecuta desde otro directorio
    $fullAssetsPath = (Resolve-Path $assetsPath).Path
    $fullMainPath = (Resolve-Path $main).Path

    pyinstaller --noconfirm --onefile --windowed --icon=$icon --add-data "$fullAssetsPath;game/assets" $fullMainPath
}
catch {
    Write-Host "[ERROR] Falló la compilación con PyInstaller." -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}


# VERIFICAR EJECUTABLE
$exePath = Join-Path $distPath $exeName
if (!(Test-Path $exePath)) {
    Write-Host "[ERROR] Falló la compilación. El archivo '$exeName' no fue generado." -ForegroundColor Red
    exit 1
}
else {
    Write-Host "✅ Ejecutable '$exeName' generado exitosamente." -ForegroundColor Green
}

# CREAR CARPETA PORTABLE
$portablePath = Join-Path $distPath $portableFolder
Write-Host "Creando carpeta portable en '$portablePath'..."
if (Test-Path $portablePath) { Remove-Item -Path $portablePath -Recurse -Force }
New-Item -ItemType Directory -Path $portablePath | Out-Null

# COPIAR EJECUTABLE
Write-Host "Copiando ejecutable a la carpeta portable..."
Copy-Item -Path $exePath -Destination $portablePath -Force

# ======================
# CREAR INSTALADOR AUTOEXTRAÍBLE CON WINRAR
# ======================

# Verificar WinRAR en rutas comunes
$winrarPath = ""
$winrarFound = $false

if (Test-Path "${env:ProgramFiles}\WinRAR\WinRAR.exe") {
    $winrarPath = "${env:ProgramFiles}\WinRAR\WinRAR.exe"
    $winrarFound = $true
}
elseif (Test-Path "${env:ProgramFiles(x86)}\WinRAR\WinRAR.exe") {
    $winrarPath = "${env:ProgramFiles(x86)}\WinRAR\WinRAR.exe"
    $winrarFound = $true
}

if($winrarFound){
    Write-Host "📦 Creando instalador autoextraible con WinRAR..."
    try {
        # El comando de WinRAR debe ser ejecutado con el operador de llamada '&'
        # Asegúrate de que el archivo 'comment.txt' exista y tenga el contenido deseado para la configuración SFX
        & "$winrarPath" a -r -sfx -z"$rarCommentFile" -iicon"$icon" "$installerPath" "$portablePath\*"

        Write-Host "✅ ¡Instalador WinRAR creado exitosamente! Ejecuta '$installerName' para instalar el juego." -ForegroundColor Green
    }
    catch {
        Write-Host "[ERROR] Fallo la creacion del instalador WinRAR." -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
    }
}
else {
    Write-Host "[ADVERTENCIA] No se encontro WinRAR en el sistema. No se pudo crear el instalador autoextraible." -ForegroundColor Yellow
    Write-Host "Puedes distribuir la carpeta '$portableFolder' manualmente o usar 7-Zip si lo prefieres."
}

# ======================
# LIMPIEZA FINAL
# ======================
Write-Host "🧹 Limpiando archivos temporales..."
Remove-Item "build" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$distPath\$exeName" -Force -ErrorAction SilentlyContinue
Remove-Item "$distPath\snake_portable" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "*.spec" -Force -ErrorAction SilentlyContinue

Write-Host "🎮 ¡Listo! El ejecutable esta en '$distPath\$portableFolder'." -ForegroundColor Cyan

