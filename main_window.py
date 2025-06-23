#!/usr/bin/env python3
"""
Ventana principal de la aplicación Linux GUI
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QComboBox, QStackedWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from styles import ThemeManager, get_general_menu_styles, get_menu_styles
from components import MenuWidget, TerminalWidget, EasyWidget, DependenciesWidget


class MainWindow(QMainWindow):
    """Ventana principal con menú de navegación"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🐧 Linux GUI - Interfaz Épica PyQt6")
        self.setGeometry(100, 100, 1200, 800)
        
        # Configuración de temas
        self.theme_manager = ThemeManager()
        self.current_theme = "dark_cyberpunk"
        
        # Configurar fuentes
        self.setup_fonts()
        
        # Crear interfaz principal
        self.setup_ui()
        
        # Aplicar tema inicial
        self.apply_theme()
    
    def setup_fonts(self):
        """Configurar fuentes personalizadas"""
        self.title_font = QFont("Roboto", 18, QFont.Weight.Bold)
        self.menu_font = QFont("Roboto", 14, QFont.Weight.Bold)
        self.button_font = QFont("Roboto", 12, QFont.Weight.Bold)
    
    def setup_ui(self):
        """Crear la interfaz de usuario principal"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Stack widget para cambiar entre pantallas
        self.stacked_widget = QStackedWidget()
        
        # Crear páginas
        self.create_pages()
        
        # Agregar páginas al stack
        self.stacked_widget.addWidget(self.menu_page)
        self.stacked_widget.addWidget(self.terminal_page)
        self.stacked_widget.addWidget(self.easy_page)
        self.stacked_widget.addWidget(self.dependencies_page)
        
        # Barra superior con tema
        self.create_header(main_layout)
        
        # Agregar stack widget
        main_layout.addWidget(self.stacked_widget)
        
        # Mostrar página de menú por defecto
        self.stacked_widget.setCurrentWidget(self.menu_page)
    
    def create_pages(self):
        """Crear todas las páginas de la aplicación"""
        # Página del menú principal
        self.menu_page = MenuWidget(self)
        
        # Página del terminal
        self.terminal_page = TerminalWidget(self.theme_manager, self.current_theme, self)
        
        # Página Easy Mode
        self.easy_page = EasyWidget(self.theme_manager, self.current_theme, self)
        
        # Página Dependencies
        self.dependencies_page = DependenciesWidget(self.theme_manager, self.current_theme, self)
    
    def create_header(self, layout):
        """Crear barra superior"""
        header_layout = QHBoxLayout()
        
        # Botón de regreso (oculto inicialmente)
        self.back_button = QPushButton("⬅️ Volver")
        self.back_button.setObjectName("backButton")
        self.back_button.setFont(self.button_font)
        self.back_button.clicked.connect(self.go_back_to_menu)
        self.back_button.setVisible(False)
        header_layout.addWidget(self.back_button)
        
        # Espaciador
        header_layout.addStretch()
        
        # Selector de tema
        theme_label = QLabel("Tema:")
        header_layout.addWidget(theme_label)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(self.theme_manager.get_theme_names())
        self.theme_combo.setCurrentText(self.current_theme)
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        header_layout.addWidget(self.theme_combo)
        
        layout.addLayout(header_layout)
    
    def show_terminal(self):
        """Mostrar página del terminal"""
        self.stacked_widget.setCurrentWidget(self.terminal_page)
        self.back_button.setVisible(True)
        self.setWindowTitle("🐧 Linux GUI - Terminal")
    
    def show_easy(self):
        """Mostrar página Easy"""
        self.stacked_widget.setCurrentWidget(self.easy_page)
        self.back_button.setVisible(True)
        self.setWindowTitle("🐧 Linux GUI - Easy Mode")
    
    def show_dependencies(self):
        """Mostrar página Install Dependencies"""
        self.stacked_widget.setCurrentWidget(self.dependencies_page)
        self.back_button.setVisible(True)
        self.setWindowTitle("🐧 Linux GUI - Install Dependencies")
    
    def go_back_to_menu(self):
        """Volver al menú principal"""
        self.stacked_widget.setCurrentWidget(self.menu_page)
        self.back_button.setVisible(False)
        self.setWindowTitle("🐧 Linux GUI - Interfaz Épica PyQt6")
    
    def change_theme(self, theme_name):
        """Cambiar tema de la aplicación"""
        self.current_theme = theme_name
        
        # Cambiar tema en todas las páginas
        self.terminal_page.change_theme(theme_name)
        self.easy_page.change_theme(theme_name)
        self.dependencies_page.change_theme(theme_name)
        
        # Aplicar tema general
        self.apply_theme()
    
    def apply_theme(self):
        """Aplicar el tema actual"""
        theme = self.theme_manager.get_theme(self.current_theme)
        
        # Aplicar estilos generales
        general_styles = get_general_menu_styles(theme)
        menu_styles = get_menu_styles(theme)
        combined_styles = general_styles + menu_styles
        
        self.setStyleSheet(combined_styles)
        
        # Aplicar tema específico al menú
        self.menu_page.apply_theme(combined_styles)
    
    def closeEvent(self, event):
        """Manejar cierre de aplicación principal"""
        # Limpiar recursos de todas las páginas
        if hasattr(self, 'terminal_page'):
            self.terminal_page.closeEvent(event)
        
        # Aceptar el evento de cierre
        event.accept()
