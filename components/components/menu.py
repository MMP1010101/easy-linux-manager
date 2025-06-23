#!/usr/bin/env python3
"""
Menú principal de la aplicación Linux GUI
"""

import os
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap


class MenuWidget(QWidget):
    """Widget del menú principal"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setup_fonts()
        self.setup_ui()
    
    def setup_fonts(self):
        """Configurar fuentes personalizadas"""
        self.menu_font = QFont("Roboto", 14, QFont.Weight.Bold)
    
    def setup_ui(self):
        """Crear la interfaz de usuario del menú"""
        # Layout principal horizontal
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Set object name for theme styling
        self.setObjectName("menuPageWidget")
        
        # Área para la imagen del logo en el lado izquierdo
        self.create_logo_area(layout)
        
        # Área para los botones en el lado derecho
        self.create_buttons_area(layout)
    
    def create_logo_area(self, layout):
        """Crear área del logo"""
        logo_area = QWidget()
        logo_area.setMinimumWidth(550)  # Forzar un ancho mínimo grande
        logo_area.setObjectName("logoArea")
        logo_layout = QVBoxLayout(logo_area)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setSpacing(0)
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Logo (utiliza una etiqueta para mostrar la imagen)
        eye_logo = QLabel()
        eye_logo.setObjectName("logoLabel")
        # Llenar todo el espacio disponible
        eye_logo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logo.png")
        eye_pixmap = QPixmap(logo_path)
        
        if eye_pixmap.isNull():
            eye_logo.setText("👁️⚡")
            eye_logo.setFont(QFont("Arial", 180, QFont.Weight.Bold))
            eye_logo.setStyleSheet("color: white; background-color: #0d1117;")
            print(f"⚠️ No se pudo cargar la imagen del logo desde: {logo_path}")
        else:
            print(f"✅ Logo cargado correctamente desde: {logo_path}")
            # Hacer el logo MUCHO más grande (ocupando al menos la mitad del espacio)
            eye_logo.setPixmap(eye_pixmap.scaled(780, 780, 
                              Qt.AspectRatioMode.KeepAspectRatio, 
                              Qt.TransformationMode.SmoothTransformation))
            # Eliminar cualquier espacio blanco alrededor de la imagen
            eye_logo.setObjectName("logoLabel")
        
        eye_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addStretch(1)  # Espacio flexible arriba
        logo_layout.addWidget(eye_logo)
        logo_layout.addStretch(1)  # Espacio flexible abajo
        
        layout.addWidget(logo_area, 1)
    
    def create_buttons_area(self, layout):
        """Crear área de botones"""
        buttons_area = QWidget()
        buttons_area.setObjectName("buttonsArea")
        buttons_layout = QVBoxLayout(buttons_area)
        buttons_layout.setContentsMargins(20, 20, 20, 20)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        buttons_layout.setSpacing(20)
        
        # Set object name for theme styling
        buttons_area.setObjectName("buttonsArea")
        
        # Botón Terminal
        terminal_button = QPushButton("▶ terminal")
        terminal_button.setObjectName("menuButton")
        terminal_button.setFont(self.menu_font)
        terminal_button.setFixedSize(400, 80)
        if self.parent_window:
            terminal_button.clicked.connect(self.parent_window.show_terminal)
        buttons_layout.addWidget(terminal_button)
        
        # Botón Easy
        easy_button = QPushButton("▶ easy")
        easy_button.setObjectName("menuButton")
        easy_button.setFont(self.menu_font)
        easy_button.setFixedSize(400, 80)
        if self.parent_window:
            easy_button.clicked.connect(self.parent_window.show_easy)
        buttons_layout.addWidget(easy_button)
        
        # Botón Install Dependencies
        deps_button = QPushButton("▶ install easy dependencies")
        deps_button.setObjectName("menuButton")
        deps_button.setFont(self.menu_font)
        deps_button.setFixedSize(400, 80)
        if self.parent_window:
            deps_button.clicked.connect(self.parent_window.show_dependencies)
        buttons_layout.addWidget(deps_button)
        
        layout.addWidget(buttons_area, 1)
    
    def apply_theme(self, theme_styles):
        """Aplicar tema al menú"""
        self.setStyleSheet(theme_styles)
