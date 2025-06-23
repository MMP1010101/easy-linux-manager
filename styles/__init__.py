"""
Inicializador del módulo de estilos
"""

from .themes import ThemeManager
from .menu_styles import get_menu_styles, get_general_menu_styles
from .terminal_styles import get_terminal_styles, get_terminal_text_colors
from .mode_styles import get_mode_styles, get_form_styles

__all__ = [
    'ThemeManager',
    'get_menu_styles',
    'get_general_menu_styles', 
    'get_terminal_styles',
    'get_terminal_text_colors',
    'get_mode_styles',
    'get_form_styles'
]
