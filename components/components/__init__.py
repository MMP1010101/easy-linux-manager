"""
Inicializador del módulo de componentes
"""

from .menu import MenuWidget
from .terminal import TerminalWidget
from .easy_mode import EasyWidget
from .dependencies import DependenciesWidget
from .file_explorer import FileExplorerWidget

__all__ = [
    'MenuWidget',
    'TerminalWidget', 
    'EasyWidget',
    'DependenciesWidget',
    'FileExplorerWidget'
]
