#!/usr/bin/env python3
"""
Easy Mode widget para la aplicación Linux GUI
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class EasyWidget(QWidget):
    """Widget para el modo Easy"""
    
    def __init__(self, theme_manager, current_theme, parent=None):
        super().__init__(parent)
        
        self.theme_manager = theme_manager
        self.current_theme = current_theme
        
        self.setup_fonts()
        self.setup_ui()
        self.apply_theme()
    
    def setup_fonts(self):
        """Configurar fuentes personalizadas"""
        self.title_font = QFont("Roboto", 18, QFont.Weight.Bold)
        self.menu_font = QFont("Roboto", 14, QFont.Weight.Bold)
    
    def setup_ui(self):
        """Crear la interfaz de usuario del modo Easy"""
        self.setObjectName("modeWidget")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        
        title = QLabel("✨ EASY MODE")
        title.setObjectName("easyTitle")
        title.setFont(self.title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        info = QLabel("Esta funcionalidad estará disponible próximamente...")
        info.setObjectName("modeInfo")
        info.setFont(self.menu_font)
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)
        
        layout.addStretch()
    
    def apply_theme(self):
        """Aplicar tema al widget"""
        from styles.mode_styles import get_mode_styles
        theme = self.theme_manager.get_theme(self.current_theme)
        mode_styles = get_mode_styles(theme, "easy")
        self.setStyleSheet(mode_styles)
    
    def change_theme(self, theme_name):
        """Cambiar tema del widget"""
        self.current_theme = theme_name
        self.apply_theme()
