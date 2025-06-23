#!/usr/bin/env python3
"""
Terminal GUI épico usando PyQt6
Interfaz moderna para terminal Linux con temas personalizables
"""

import sys
import os
import subprocess
import threading
import queue
import time
import random
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel, QFrame, QComboBox,
    QScrollArea, QMessageBox, QInputDialog, QSplitter, QStackedWidget
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QProcess
from PyQt6.QtGui import QFont, QTextCursor, QPixmap, QPalette, QColor


class CommandRunner(QThread):
    """Hilo para ejecutar comandos sin bloquear la interfaz"""
    output_ready = pyqtSignal(str, str)  # texto, tipo
    finished_execution = pyqtSignal()
    password_required = pyqtSignal(str)  # comando que requiere contraseña
    
    def __init__(self, command, password=None):
        super().__init__()
        self.command = command
        self.password = password
        self.process = None
        # Timeout más largo para comandos de instalación
        self.timeout = 300 if any(keyword in command.lower() for keyword in ['install', 'upgrade', 'update']) else 30
    
    def run(self):
        try:
            if self.command.strip() == "clear":
                self.output_ready.emit("CLEAR_TERMINAL", "clear")
                return
            
            if self.command.startswith("cd "):
                path = self.command[3:].strip()
                try:
                    os.chdir(os.path.expanduser(path))
                    self.output_ready.emit(f"📂 Directorio cambiado a: {os.getcwd()}\n", "success")
                except Exception as e:
                    self.output_ready.emit(f"❌ Error: {str(e)}\n", "error")
                return
            
            # Manejar comandos sudo
            if self.command.strip().startswith("sudo "):
                self._run_sudo_command()
                return
            
            # Ejecutar comando normal con salida en tiempo real
            self._run_command_realtime()
                
        except subprocess.TimeoutExpired:
            if self.process:
                self.process.kill()
            self.output_ready.emit("⏰ Comando cancelado por timeout (30s)\n", "error")
        except Exception as e:
            self.output_ready.emit(f"❌ Error ejecutando comando: {str(e)}\n", "error")
        finally:
            self.finished_execution.emit()
    
    def _run_command_realtime(self):
        """Ejecutar comando con salida en tiempo real"""
        try:
            self.process = subprocess.Popen(
                self.command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # Combinar stderr con stdout
                text=True,
                bufsize=1,  # Línea por línea
                universal_newlines=True,
                cwd=os.getcwd()
            )
            
            # Leer salida línea por línea
            while True:
                output = self.process.stdout.readline()
                if output == '' and self.process.poll() is not None:
                    break
                if output:
                    self.output_ready.emit(output, "normal")
            
            # Obtener código de retorno
            return_code = self.process.poll()
            if return_code != 0:
                self.output_ready.emit(f"❌ Comando terminó con código de error: {return_code}\n", "error")
                
        except Exception as e:
            self.output_ready.emit(f"❌ Error ejecutando comando: {str(e)}\n", "error")
    
    def _run_sudo_command(self):
        """Ejecutar comando sudo con contraseña y salida en tiempo real"""
        try:
            if not self.password:
                self.password_required.emit(self.command)
                return
            
            # Ejecutar comando sudo con contraseña
            self.process = subprocess.Popen(
                ['sudo', '-S'] + self.command.split()[1:],  # -S lee contraseña desde stdin
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # Combinar stderr con stdout
                text=True,
                bufsize=1,  # Línea por línea
                universal_newlines=True,
                cwd=os.getcwd()
            )
            
            # Enviar contraseña
            self.process.stdin.write(self.password + '\n')
            self.process.stdin.flush()
            self.process.stdin.close()
            
            # Leer salida línea por línea
            while True:
                output = self.process.stdout.readline()
                if output == '' and self.process.poll() is not None:
                    break
                if output and "password" not in output.lower():
                    self.output_ready.emit(output, "normal")
            
            # Verificar código de retorno
            return_code = self.process.poll()
            if return_code == 0:
                self.output_ready.emit("✅ Comando sudo ejecutado exitosamente\n", "success")
            else:
                self.output_ready.emit(f"❌ Error en comando sudo (código: {return_code})\n", "error")
                
        except subprocess.TimeoutExpired:
            if self.process:
                self.process.kill()
            self.output_ready.emit("⏰ Comando sudo cancelado por timeout\n", "error")
        except Exception as e:
            self.output_ready.emit(f"❌ Error ejecutando sudo: {str(e)}\n", "error")


class MainWindow(QMainWindow):
    """Ventana principal con menú de navegación"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🐧 Linux GUI - Interfaz Épica PyQt6")
        self.setGeometry(100, 100, 1200, 800)
        
        # Configuración de temas (igual que antes)
        self.themes = {
            "dark_cyberpunk": {
                "bg": "#0d1117",
                "fg": "#58a6ff", 
                "accent": "#39d353",
                "text": "#f0f6fc",
                "terminal_bg": "#010409",
                "terminal_fg": "#7ee787",
                "button_bg": "#238636",
                "button_fg": "#ffffff",
                "error_fg": "#f85149",
                "status_fg": "#8b949e",
                "selection_bg": "#1f6feb",
                "border_color": "#30363d"
            },
            "hacker_matrix": {
                "bg": "#000000",
                "fg": "#00ff00",
                "accent": "#00aa00", 
                "text": "#00ff00",
                "terminal_bg": "#0a0a0a",
                "terminal_fg": "#00ff00",
                "button_bg": "#005500",
                "button_fg": "#00ff00",
                "error_fg": "#ff0000",
                "status_fg": "#00aa00",
                "selection_bg": "#003300",
                "border_color": "#00aa00"
            },
            "midnight_blue": {
                "bg": "#1a1b26",
                "fg": "#7aa2f7",
                "accent": "#bb9af7",
                "text": "#c0caf5", 
                "terminal_bg": "#16161e",
                "terminal_fg": "#a9b1d6",
                "button_bg": "#414868",
                "button_fg": "#c0caf5",
                "error_fg": "#f7768e",
                "status_fg": "#565f89",
                "selection_bg": "#283457",
                "border_color": "#414868"
            }
        }
        
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
        self.create_menu_page()
        self.create_terminal_page()
        self.create_easy_page()
        self.create_dependencies_page()
        
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
    
    def create_header(self, layout):
        """Crear barra superior"""
        header_layout = QHBoxLayout()
        
        # Botón de regreso (oculto inicialmente)
        self.back_button = QPushButton("⬅️ Volver")
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
        self.theme_combo.addItems(list(self.themes.keys()))
        self.theme_combo.setCurrentText(self.current_theme)
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        header_layout.addWidget(self.theme_combo)
        
        layout.addLayout(header_layout)
    
    def create_menu_page(self):
        """Crear página del menú principal"""
        self.menu_page = QWidget()
        layout = QVBoxLayout(self.menu_page)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)
        
        # Título principal
        title_label = QLabel("🐧 LINUX GUI ÉPICO")
        title_label.setFont(self.title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Subtítulo
        subtitle_label = QLabel("Selecciona una opción:")
        subtitle_label.setFont(self.menu_font)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle_label)
        
        # Espaciador
        layout.addStretch()
        
        # Botones del menú
        menu_buttons_layout = QVBoxLayout()
        menu_buttons_layout.setSpacing(20)
        
        # Botón Terminal
        terminal_button = QPushButton("▶️ Terminal")
        terminal_button.setFont(self.menu_font)
        terminal_button.setFixedHeight(80)
        terminal_button.clicked.connect(self.show_terminal)
        menu_buttons_layout.addWidget(terminal_button)
        
        # Botón Easy
        easy_button = QPushButton("✨ Easy")
        easy_button.setFont(self.menu_font)
        easy_button.setFixedHeight(80)
        easy_button.clicked.connect(self.show_easy)
        menu_buttons_layout.addWidget(easy_button)
        
        # Botón Install Dependencies
        deps_button = QPushButton("📦 Install Dependencies")
        deps_button.setFont(self.menu_font)
        deps_button.setFixedHeight(80)
        deps_button.clicked.connect(self.show_dependencies)
        menu_buttons_layout.addWidget(deps_button)
        
        layout.addLayout(menu_buttons_layout)
        layout.addStretch()
        
        # Info del sistema
        info_label = QLabel(f"Sistema: {os.uname().sysname} | Usuario: {os.getenv('USER', 'usuario')}")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)
    
    def create_terminal_page(self):
        """Crear página del terminal (usando la clase TerminalGUI existente)"""
        self.terminal_page = TerminalWidget(self.themes, self.current_theme)
    
    def create_easy_page(self):
        """Crear página Easy (placeholder por ahora)"""
        self.easy_page = QWidget()
        layout = QVBoxLayout(self.easy_page)
        layout.setContentsMargins(50, 50, 50, 50)
        
        title = QLabel("✨ EASY MODE")
        title.setFont(self.title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        info = QLabel("Esta funcionalidad estará disponible próximamente...")
        info.setFont(self.menu_font)
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)
        
        layout.addStretch()
    
    def create_dependencies_page(self):
        """Crear página Install Dependencies (placeholder por ahora)"""
        self.dependencies_page = QWidget()
        layout = QVBoxLayout(self.dependencies_page)
        layout.setContentsMargins(50, 50, 50, 50)
        
        title = QLabel("📦 INSTALL DEPENDENCIES")
        title.setFont(self.title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        info = QLabel("Esta funcionalidad estará disponible próximamente...")
        info.setFont(self.menu_font)
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)
        
        layout.addStretch()
    
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
        self.terminal_page.change_theme(theme_name)
        self.apply_theme()
    
    def apply_theme(self):
        """Aplicar el tema actual"""
        theme = self.themes[self.current_theme]
        
        # Estilo CSS para toda la aplicación
        style = f"""
        QMainWindow {{
            background-color: {theme['bg']};
            color: {theme['text']};
        }}
        
        QWidget {{
            background-color: {theme['bg']};
            color: {theme['text']};
        }}
        
        QLabel {{
            color: {theme['text']};
            background-color: transparent;
        }}
        
        QPushButton {{
            background-color: {theme['button_bg']};
            color: {theme['button_fg']};
            border: none;
            border-radius: 10px;
            padding: 15px 20px;
            font-weight: bold;
        }}
        
        QPushButton:hover {{
            background-color: {theme['accent']};
        }}
        
        QPushButton:pressed {{
            background-color: {theme['selection_bg']};
        }}
        
        QComboBox {{
            background-color: {theme['button_bg']};
            color: {theme['button_fg']};
            border: 2px solid {theme['border_color']};
            border-radius: 5px;
            padding: 5px;
        }}
        
        QComboBox:hover {{
            border-color: {theme['accent']};
        }}
        """
        
        self.setStyleSheet(style)


class TerminalWidget(QWidget):
    """Widget del terminal para usar dentro de MainWindow"""
    def __init__(self, themes, current_theme):
        super().__init__()
        
        self.themes = themes
        self.current_theme = current_theme
        self.command_history = []
        self.history_index = 0
        self.command_runner = None
        
        # Configurar fuentes
        self.setup_fonts()
        
        # Crear interfaz
        self.setup_ui()
        
        # Aplicar tema inicial
        self.apply_theme()
        
        # Configurar timers y efectos
        self.setup_timers()
        
        # Mensaje de bienvenida
        self.show_welcome_message()
    
    def setup_fonts(self):
        """Configurar fuentes personalizadas"""
        self.title_font = QFont("Roboto", 14, QFont.Weight.Bold)
        self.terminal_font = QFont("JetBrains Mono", 11)
        self.button_font = QFont("Roboto", 10, QFont.Weight.Bold)
        self.status_font = QFont("Roboto", 9)
    
    def setup_ui(self):
        """Crear la interfaz de usuario del terminal"""
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        # Título del terminal
        title_label = QLabel("🐧 TERMINAL ÉPICA")
        title_label.setFont(self.title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Separador decorativo
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFixedHeight(2)
        main_layout.addWidget(separator)
        
        # Área del terminal
        self.create_terminal_area(main_layout)
        
        # Área de entrada
        self.create_input_area(main_layout)
        
        # Botones rápidos
        self.create_quick_buttons(main_layout)
        
        # Barra de estado
        self.create_status_bar(main_layout)
    
    def create_terminal_area(self, layout):
        """Crear área del terminal"""
        # Frame contenedor del terminal
        terminal_frame = QFrame()
        terminal_frame.setFrameStyle(QFrame.Shape.Box)
        terminal_frame.setLineWidth(2)
        
        terminal_layout = QVBoxLayout(terminal_frame)
        terminal_layout.setContentsMargins(5, 5, 5, 5)
        
        # Área de texto del terminal
        self.terminal_output = QTextEdit()
        self.terminal_output.setFont(self.terminal_font)
        self.terminal_output.setReadOnly(True)
        self.terminal_output.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        terminal_layout.addWidget(self.terminal_output)
        
        layout.addWidget(terminal_frame)
    
    def create_input_area(self, layout):
        """Crear área de entrada de comandos"""
        input_layout = QHBoxLayout()
        
        # Prompt
        prompt_label = QLabel("$")
        prompt_label.setFont(self.terminal_font)
        input_layout.addWidget(prompt_label)
        
        # Campo de entrada
        self.command_input = QLineEdit()
        self.command_input.setFont(self.terminal_font)
        self.command_input.returnPressed.connect(self.execute_command)
        self.command_input.setPlaceholderText("Escribe tu comando aquí...")
        input_layout.addWidget(self.command_input)
        
        # Botón ejecutar
        self.execute_button = QPushButton("EJECUTAR")
        self.execute_button.setFont(self.button_font)
        self.execute_button.clicked.connect(self.execute_command)
        self.execute_button.setFixedWidth(100)
        input_layout.addWidget(self.execute_button)
        
        layout.addLayout(input_layout)
        
        # Configurar navegación por historial
        self.command_input.keyPressEvent = self.handle_key_press
    
    def create_quick_buttons(self, layout):
        """Crear botones de comandos rápidos"""
        buttons_layout = QHBoxLayout()
        
        quick_commands = [
            ("✨ Limpiar", "clear"),
            ("📂 Archivos", "ls -la"),
            ("📊 Sistema", "htop" if self.command_exists("htop") else "top"),
            ("💾 Disco", "df -h"),
            ("🧠 Memoria", "free -h"),
            ("❓ Ayuda", "help")
        ]
        
        for text, cmd in quick_commands:
            button = QPushButton(text)
            button.setFont(self.button_font)
            button.clicked.connect(lambda checked, command=cmd: self.quick_command(command))
            button.setFixedHeight(35)
            buttons_layout.addWidget(button)
        
        layout.addLayout(buttons_layout)
    
    def create_status_bar(self, layout):
        """Crear barra de estado"""
        status_layout = QHBoxLayout()
        
        # Etiqueta de estado
        self.status_label = QLabel(f"▶️ Terminal listo - Directorio: {os.getcwd()}")
        self.status_label.setFont(self.status_font)
        status_layout.addWidget(self.status_label)
        
        # Espaciador
        status_layout.addStretch()
        
        # Indicador de proceso
        self.process_indicator = QLabel("●")
        self.process_indicator.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        status_layout.addWidget(self.process_indicator)
        
        layout.addLayout(status_layout)
    
    def setup_timers(self):
        """Configurar timers y efectos"""
        # Timer para animar el indicador de proceso
        self.indicator_timer = QTimer()
        self.indicator_timer.timeout.connect(self.animate_indicator)
        self.indicator_timer.start(800)
    
    def apply_theme(self):
        """Aplicar el tema actual"""
        theme = self.themes[self.current_theme]
        
        # Estilo CSS para toda la aplicación
        style = f"""
        QMainWindow {{
            background-color: {theme['bg']};
            color: {theme['text']};
        }}
        
        QWidget {{
            background-color: {theme['bg']};
            color: {theme['text']};
        }}
        
        QLabel {{
            color: {theme['text']};
            background-color: transparent;
        }}
        
        QTextEdit {{
            background-color: {theme['terminal_bg']};
            color: {theme['terminal_fg']};
            border: 2px solid {theme['border_color']};
            border-radius: 5px;
            padding: 10px;
            font-family: monospace;
            line-height: 1.2;
        }}
        
        QLineEdit {{
            background-color: {theme['terminal_bg']};
            color: {theme['text']};
            border: 2px solid {theme['border_color']};
            border-radius: 5px;
            padding: 8px;
        }}
        
        QLineEdit:focus {{
            border-color: {theme['accent']};
        }}
        
        QPushButton {{
            background-color: {theme['button_bg']};
            color: {theme['button_fg']};
            border: none;
            border-radius: 5px;
            padding: 8px 16px;
            font-weight: bold;
        }}
        
        QPushButton:hover {{
            background-color: {theme['accent']};
        }}
        
        QPushButton:pressed {{
            background-color: {theme['selection_bg']};
        }}
        
        QComboBox {{
            background-color: {theme['button_bg']};
            color: {theme['button_fg']};
            border: 2px solid {theme['border_color']};
            border-radius: 5px;
            padding: 5px;
        }}
        
        QComboBox:hover {{
            border-color: {theme['accent']};
        }}
        
        QFrame {{
            border: 2px solid {theme['border_color']};
            border-radius: 5px;
        }}
        
        QFrame[frameShape="4"] {{
            background-color: {theme['accent']};
            border: none;
        }}
        """
        
        self.setStyleSheet(style)
        
        # Actualizar colores específicos de labels
        self.status_label.setStyleSheet(f"color: {theme['status_fg']};")
        self.process_indicator.setStyleSheet(f"color: {theme['accent']};")
    
    def show_welcome_message(self):
        """Mostrar mensaje de bienvenida"""
        welcome_msg = f"""🐧 Bienvenido a Linux Terminal GUI PyQt6
Esta es una terminal completamente funcional con tema {self.current_theme}.
Puedes ejecutar cualquier comando de Linux aquí.

Directorio actual: {os.getcwd()}
Usuario: {os.getenv('USER', 'usuario')}
Sistema: {os.uname().sysname} {os.uname().release}

Comandos especiales:
- 'clear' - Limpiar terminal
- 'cd directorio' - Cambiar directorio
- 'help' - Mostrar ayuda

¡Disfruta de tu experiencia de terminal épica! ✨

"""
        self.terminal_output.setPlainText(welcome_msg)
    
    def command_exists(self, cmd):
        """Verificar si un comando existe"""
        try:
            subprocess.run(['which', cmd], capture_output=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def handle_key_press(self, event):
        """Manejar teclas especiales en el campo de entrada"""
        if event.key() == Qt.Key.Key_Up:
            self.history_up()
        elif event.key() == Qt.Key.Key_Down:
            self.history_down()
        else:
            # Comportamiento normal
            QLineEdit.keyPressEvent(self.command_input, event)
    
    def history_up(self):
        """Navegar hacia arriba en el historial"""
        if self.command_history and self.history_index > 0:
            self.history_index -= 1
            self.command_input.setText(self.command_history[self.history_index])
    
    def history_down(self):
        """Navegar hacia abajo en el historial"""
        if self.command_history and self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.command_input.setText(self.command_history[self.history_index])
        elif self.command_history and self.history_index == len(self.command_history) - 1:
            self.history_index = len(self.command_history)
            self.command_input.clear()
    
    def change_theme(self, theme_name):
        """Cambiar tema del widget terminal"""
        self.current_theme = theme_name
        self.apply_theme()
        
        # Mensaje en terminal
        self.append_output(f"✨ Tema cambiado a: {theme_name}\n", "success")
    
    def quick_command(self, command):
        """Ejecutar comando rápido"""
        self.command_input.setText(command)
        self.execute_command()
    
    def execute_command(self):
        """Ejecutar comando ingresado"""
        command = self.command_input.text().strip()
        if not command:
            return
        
        # Añadir al historial
        if not self.command_history or command != self.command_history[-1]:
            self.command_history.append(command)
        self.history_index = len(self.command_history)
        
        # Agregar separación visual si no es el primer comando
        if self.command_history:
            self.append_output("\n", "normal")
        
        # Mostrar comando en terminal
        current_dir = os.path.basename(os.getcwd())
        prompt = f"{os.getenv('USER', 'user')}@{current_dir}:$ "
        self.append_output(prompt + command + "\n", "command")
        
        # Limpiar entrada
        self.command_input.clear()
        
        # Deshabilitar entrada durante ejecución
        self.command_input.setEnabled(False)
        self.execute_button.setEnabled(False)
        
        # Actualizar estado
        self.status_label.setText(f"⚡ Ejecutando: {command}")
        
        # Ejecutar comando
        self.command_runner = CommandRunner(command)
        self.command_runner.output_ready.connect(self.handle_command_output)
        self.command_runner.finished_execution.connect(self.command_finished)
        self.command_runner.password_required.connect(self.handle_password_request)
        self.command_runner.start()
    
    def handle_password_request(self, command):
        """Manejar solicitud de contraseña para sudo"""
        password, ok = QInputDialog.getText(
            self, 
            "🔐 Autenticación requerida",
            f"Ingresa la contraseña para {os.getenv('USER', 'user')}:",
            QLineEdit.EchoMode.Password
        )
        
        if ok and password:
            # Crear nuevo runner con contraseña
            self.command_runner = CommandRunner(command, password)
            self.command_runner.output_ready.connect(self.handle_command_output)
            self.command_runner.finished_execution.connect(self.command_finished)
            self.command_runner.start()
        else:
            # Usuario canceló
            self.append_output("❌ Comando sudo cancelado por el usuario\n", "error")
            self.command_finished()
    
    def handle_command_output(self, text, output_type):
        """Manejar salida del comando"""
        if text == "CLEAR_TERMINAL":
            self.terminal_output.clear()
        else:
            self.append_output(text, output_type)
    
    def command_finished(self):
        """Comando terminado"""
        # Agregar línea en blanco al final para separación
        self.append_output("\n", "normal")
        
        # Rehabilitar entrada
        self.command_input.setEnabled(True)
        self.execute_button.setEnabled(True)
        self.command_input.setFocus()
        
        # Actualizar estado
        self.status_label.setText(f"▶️ Terminal listo - Directorio: {os.getcwd()}")
    
    def append_output(self, text, text_type='normal'):
        """Agregar texto al terminal"""
        if not text:
            return
        
        cursor = self.terminal_output.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        
        # Aplicar formato según el tipo
        theme = self.themes[self.current_theme]
        if text_type == 'error':
            color = theme['error_fg']
        elif text_type == 'success':
            color = theme['accent']
        elif text_type == 'command':
            color = theme['fg']
        else:
            color = theme['terminal_fg']
        
        # Procesar texto para mantener formato y saltos de línea
        # Escapar HTML pero preservar saltos de línea
        escaped_text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        # Convertir saltos de línea a <br> y espacios a &nbsp; para mantener formato
        formatted_text = escaped_text.replace('\n', '<br>').replace('  ', '&nbsp;&nbsp;')
        
        # Insertar texto con color y formato
        format_html = f'<span style="color: {color}; font-family: monospace; white-space: pre-wrap;">{formatted_text}</span>'
        cursor.insertHtml(format_html)
        
        # Hacer scroll al final
        self.terminal_output.setTextCursor(cursor)
        self.terminal_output.ensureCursorVisible()
    
    def animate_indicator(self):
        """Animar indicador de proceso"""
        theme = self.themes[self.current_theme]
        colors = [theme['accent'], theme['fg'], theme['text']]
        color = random.choice(colors)
        self.process_indicator.setStyleSheet(f"color: {color};")
    
    def closeEvent(self, event):
        """Manejar cierre de aplicación"""
        if self.command_runner and self.command_runner.isRunning():
            self.command_runner.terminate()
            self.command_runner.wait()
        event.accept()


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
