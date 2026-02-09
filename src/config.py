# --- CONFIG FILE/ARCHIVO DE CONFIGURACIÓN ---
import os
import sys
#--- 0. RESOURCE PATH FUNCTION/FUNCIÓN DE RUTA DE RECURSOS ---
def get_path(relative_path):
    """Get the absolute path to a resource, works for both development and PyInstaller
    /Obtener la ruta absoluta a un recurso, funciona tanto para desarrollo como para PyInstaller
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS/PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception: 
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)
# --- 1. SCREEN SETTINGS/CONFIGURACIÓN DE PANTALLA ---
SCREEN_WIDTH = 800 # Ancho de pantalla
SCREEN_HEIGHT = 600 # Altura de pantalla
FPS = 60 # Cuadros por segundo

# --- 2. GRID SETTINGS/CONFIGURACIÓN DE LA CUADRÍCULA ---
GRID_ROWS = 4 # Filas de la cuadrícula
GRID_COLS = 5 # columnas de la cuadrícula
CARD_GAP = 15  # Gap between cards/Espacio entre cartas
TOTAL_PAIRS = (GRID_ROWS * GRID_COLS) // 2 #Total pairs in the game/Total de pares en el juego
# --- 3. COLORS/COLORES ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
INDIGO = (75, 0, 130)
VIOLET = (148, 0, 211)

# --- 4. ASSETS PATHS/RUTAS DE LOS RECURSOS ---
# Get the parent directory of the current file/ Obtener el directorio padre del archivo actual
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

# --- 5. LANGUAGE SETTINGS/CONFIGURACIÓN DE IDIOMA ---
LANGUAGE = 'es'  # Default language/Idioma predeterminado
TEXTS = {
    'en': {
        'title': 'Electronics Memory Game',
        'start': 'Start Game',
        'Lang': 'Language: EN',
        'restart': 'Restart',
        'win': 'You Win!',
        'pairs': 'Pairs Found: ',
        'exit': 'Exit',
        'main_menu': 'Main Menu',
        'author':'Game by ZhuFer'
    },
    'es': {
        'title': 'Memorama Electrónico',
        'start': 'Iniciar Juego',
        'Lang': 'Idioma: ES',
        'restart': 'Reiniciar',
        'win': '¡Ganaste!',
        'pairs': 'Pares Encontrados: ',
        'exit': 'Salir',
        'main_menu': 'Menú',
        'author':'Juego por Fernando Zúñiga González'
    }
}

def get_text(key):
    """Get the text based on the current language and key
    /Obtener el texto según el idioma actual y la clave
    """
        
    return TEXTS[LANGUAGE].get(key, key)

# -- 6. GAME DATA ---
# Indexes for card pairs/Índices para pares de cartas
_COMPONENTS = {
    'en': [
        "Resistor", "Capacitor", "Inductor", "Diode", "Transistor", 
        "LED", "Battery", "Switch", "Fuse", "Ground"
    ],
    'es': [
        "Resistencia", "Capacitor", "Inductor", "Diodo", "Transistor", 
        "LED", "Batería", "Interruptor", "Fusible", "Tierra"
    ]
}
def get_component_name(index):
    """Get the component name based on the current language and index
    /Obtener el nombre del componente según el idioma actual e índice  
    """
    return _COMPONENTS[LANGUAGE][index]