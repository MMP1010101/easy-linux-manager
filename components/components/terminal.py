#!/usr/bin/env python3
"""
Terminal widget para la aplicación Linux GUI
"""

import os
import subprocess
import random
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, 
    QPushButton, QLabel, QFrame, QInputDialog
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QTextCursor
from core.command_runner import CommandRunner
from styles.terminal_styles import get_terminal_text_colors


class TerminalWidget(QWidget):
    """Widget del terminal para usar dentro de MainWindow"""
    
    def __init__(self, theme_manager, current_theme, parent=None):
        super().__init__(parent)
        
        self.theme_manager = theme_manager
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
        self.setObjectName("terminalWidget")
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        # Título del terminal
        title_label = QLabel("🐧 TERMINAL ÉPICA")
        title_label.setObjectName("terminalTitle")
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
        terminal_frame.setObjectName("terminalFrame")
        terminal_frame.setFrameStyle(QFrame.Shape.Box)
        terminal_frame.setLineWidth(2)
        
        terminal_layout = QVBoxLayout(terminal_frame)
        terminal_layout.setContentsMargins(5, 5, 5, 5)
        
        # Área de texto del terminal
        self.terminal_output = QTextEdit()
        self.terminal_output.setObjectName("terminalOutput")
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
        prompt_label.setObjectName("promptLabel")
        prompt_label.setFont(self.terminal_font)
        input_layout.addWidget(prompt_label)
        
        # Campo de entrada
        self.command_input = QLineEdit()
        self.command_input.setObjectName("commandInput")
        self.command_input.setFont(self.terminal_font)
        self.command_input.returnPressed.connect(self.execute_command)
        self.command_input.setPlaceholderText("Escribe tu comando aquí...")
        input_layout.addWidget(self.command_input)
        
        # Botón ejecutar
        self.execute_button = QPushButton("EJECUTAR")
        self.execute_button.setObjectName("executeButton")
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
            button.setObjectName("quickButton")
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
        self.status_label.setObjectName("statusLabel")
        self.status_label.setFont(self.status_font)
        status_layout.addWidget(self.status_label)
        
        # Espaciador
        status_layout.addStretch()
        
        # Indicador de proceso
        self.process_indicator = QLabel("●")
        self.process_indicator.setObjectName("processIndicator")
        self.process_indicator.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        status_layout.addWidget(self.process_indicator)
        
        layout.addLayout(status_layout)
    
    def setup_timers(self):
        """Configurar timers y efectos"""
        # Timer para animar el indicador de proceso
        self.indicator_timer = QTimer()
        self.indicator_timer.timeout.connect(self.animate_indicator)
        # Solo animar cuando hay un proceso ejecutándose
        self.is_executing = False
    
    def apply_theme(self):
        """Aplicar el tema actual"""
        from styles.terminal_styles import get_terminal_styles
        theme = self.theme_manager.get_theme(self.current_theme)
        terminal_styles = get_terminal_styles(theme)
        self.setStyleSheet(terminal_styles)
    
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
        
        # Marcar como ejecutando e iniciar animación
        self.is_executing = True
        self.indicator_timer.start(800)
        
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
            # Marcar como ejecutando e iniciar animación
            self.is_executing = True
            self.indicator_timer.start(800)
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
        
        # Detener animación y marcar como no ejecutando
        self.is_executing = False
        self.indicator_timer.stop()
        
        # Rehabilitar entrada
        self.command_input.setEnabled(True)
        self.execute_button.setEnabled(True)
        self.command_input.setFocus()
        
        # Actualizar estado
        self.status_label.setText(f"▶️ Terminal listo - Directorio: {os.getcwd()}")
        
        # Limpiar referencia al command_runner
        if self.command_runner:
            self.command_runner.deleteLater()
            self.command_runner = None
    
    def append_output(self, text, text_type='normal'):
        """Agregar texto al terminal"""
        if not text:
            return
        
        cursor = self.terminal_output.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        
        # Aplicar formato según el tipo
        theme = self.theme_manager.get_theme(self.current_theme)
        text_colors = get_terminal_text_colors(theme)
        color = text_colors.get(text_type, text_colors['normal'])
        
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
        if not self.is_executing:
            # Si no se está ejecutando nada, mostrar indicador estático
            theme = self.theme_manager.get_theme(self.current_theme)
            self.process_indicator.setStyleSheet(f"color: {theme['fg']};")
            return
            
        theme = self.theme_manager.get_theme(self.current_theme)
        colors = [theme['accent'], theme['fg'], theme['text']]
        color = random.choice(colors)
        self.process_indicator.setStyleSheet(f"color: {color};")
    
    def closeEvent(self, event):
        """Manejar cierre de aplicación"""
        # Detener timer
        if hasattr(self, 'indicator_timer') and self.indicator_timer.isActive():
            self.indicator_timer.stop()
            
        # Terminar proceso si está ejecutándose
        if self.command_runner and self.command_runner.isRunning():
            self.command_runner.terminate_safely()
        event.accept()
