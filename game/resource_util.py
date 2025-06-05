# resource_util.py
import sys
import os


def resource_path(relative_path):
    """
    Retorna la ruta absoluta al recurso, considerando si se ejecuta desde PyInstaller o en desarrollo.
    """
    if hasattr(sys, '_MEIPASS'):
        # Modo empaquetado con PyInstaller
        base_path = sys._MEIPASS
        # Corrige ruta solo si no empieza por 'game/'
        if not relative_path.startswith('game/'):
            relative_path = os.path.join('game', relative_path)
    else:
        # Modo desarrollo: parte desde el directorio raíz del proyecto
        base_path = os.path.abspath(os.path.dirname(__file__))

    full_path = os.path.join(base_path, relative_path)
    return full_path
