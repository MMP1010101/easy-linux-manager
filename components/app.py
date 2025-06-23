#!/usr/bin/env python3
"""
Terminal GUI épico usando PyQt6 - Aplicación Principal
Interfaz moderna para terminal Linux con temas personalizables
Arquitectura modular organizada
"""

import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow


def main():
    """Función principal"""
    app = QApplication(sys.argv)
    
    # Configurar aplicación
    app.setApplicationName("Linux GUI")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("Epic Linux Tools")
    
    # Crear y mostrar ventana principal
    window = MainWindow()
    window.show()
    
    # Ejecutar aplicación
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
