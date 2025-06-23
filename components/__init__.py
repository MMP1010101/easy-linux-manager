"""
Inicializador del módulo de componentes
"""

from .menu import MenuWidget
from .terminal import TerminalWidget
from .easy_mode import EasyWidget
from .dependencies import DependenciesWidget

__all__ = [
    'MenuWidget',
    'TerminalWidget', 
    'EasyWidget',
    'DependenciesWidget'
]
