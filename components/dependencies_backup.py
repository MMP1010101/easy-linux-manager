#!/usr/bin/env python3
"""
App Store widget para la aplicación Linux GUI
Permite instalar aplicaciones populares con un solo clic
"""

import os
import base64
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QScrollArea, QFrame, QPushButton, QGridLayout,
                           QLineEdit, QComboBox, QMessageBox, QProgressBar,
                           QSplitter, QTextEdit, QInputDialog)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QPixmap, QIcon
import subprocess


class AppInstaller(QThread):
    """Hilo para instalar aplicaciones sin bloquear la interfaz"""
    progress_update = pyqtSignal(str)
    installation_finished = pyqtSignal(bool, str)
    password_required = pyqtSignal()
    
    def __init__(self, app_data, password=None):
        super().__init__()
        self.app_data = app_data
        self.password = password
        
    def run(self):
        try:
            # Emitir progreso
            self.progress_update.emit(f"🔄 Iniciando instalación de {self.app_data['name']}...")
            
            # Ejecutar comando de instalación
            if self.app_data['install_method'] == 'apt':
                command = f"echo '{self.password}' | sudo -S apt update && echo '{self.password}' | sudo -S apt install -y {self.app_data['package']}"
            elif self.app_data['install_method'] == 'snap':
                # Verificar si snap está disponible, si no, instalar primero
                command = f"echo '{self.password}' | sudo -S apt install -y snapd && echo '{self.password}' | sudo -S snap install {self.app_data['package']}"
            elif self.app_data['install_method'] == 'flatpak':
                # Verificar si flatpak está disponible, si no, instalar primero
                command = f"echo '{self.password}' | sudo -S apt install -y flatpak && flatpak install -y {self.app_data['package']}"
            elif self.app_data['install_method'] == 'custom_command':
                # Para comandos personalizados, agregar la contraseña al principio
                command = f"echo '{self.password}' | sudo -S " + self.app_data['custom_command'].replace('sudo ', '')
            else:
                command = self.app_data.get('custom_command', f"echo '{self.password}' | sudo -S apt install -y {self.app_data.get('package', '')}")
            
            self.progress_update.emit(f"📥 Descargando e instalando {self.app_data['name']}...")
            self.progress_update.emit(f"🔧 Comando: {command.replace(self.password, '***')}")
            
            # Ejecutar comando
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                env=dict(os.environ, DEBIAN_FRONTEND="noninteractive")
            )
            
            # Leer salida línea por línea
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output and output.strip():
                    # Filtrar líneas que contengan la contraseña
                    if self.password not in output:
                        self.progress_update.emit(output.strip())
            
            # Verificar resultado
            return_code = process.wait()
            if return_code == 0:
                self.installation_finished.emit(True, f"✅ {self.app_data['name']} instalado correctamente")
            else:
                self.installation_finished.emit(False, f"❌ Error instalando {self.app_data['name']} (código: {return_code})")
                
        except Exception as e:
            self.installation_finished.emit(False, f"❌ Error: {str(e)}")


class AppCard(QFrame):
    """Tarjeta de aplicación individual"""
    install_requested = pyqtSignal(dict)
    
    def __init__(self, app_data, theme):
        super().__init__()
        self.app_data = app_data
        self.theme = theme
        self.setup_ui()
        
    def setup_ui(self):
        """Crear la interfaz de la tarjeta"""
        self.setObjectName("appCard")
        self.setFixedSize(280, 350)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Icono de la aplicación
        icon_label = QLabel()
        icon_label.setObjectName("appIcon")
        icon_label.setText(self.app_data['icon'])
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setFont(QFont("Arial", 48))
        icon_label.setFixedHeight(80)
        layout.addWidget(icon_label)
        
        # Nombre de la aplicación
        name_label = QLabel(self.app_data['name'])
        name_label.setObjectName("appName")
        name_label.setFont(QFont("Roboto", 14, QFont.Weight.Bold))
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setWordWrap(True)
        layout.addWidget(name_label)
        
        # Categoría
        category_label = QLabel(f"📂 {self.app_data['category']}")
        category_label.setObjectName("appCategory")
        category_label.setFont(QFont("Roboto", 10))
        category_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(category_label)
        
        # Descripción
        desc_label = QLabel(self.app_data['description'])
        desc_label.setObjectName("appDescription")
        desc_label.setFont(QFont("Roboto", 10))
        desc_label.setWordWrap(True)
        desc_label.setMaximumHeight(60)
        layout.addWidget(desc_label)
        
        # Tamaño y método de instalación
        info_label = QLabel(f"📦 {self.app_data['install_method'].upper()} • {self.app_data['size']}")
        info_label.setObjectName("appInfo")
        info_label.setFont(QFont("JetBrains Mono", 9))
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)
        
        # Botón de instalación
        install_btn = QPushButton("⬇️ INSTALAR")
        install_btn.setObjectName("installButton")
        install_btn.setFont(QFont("Roboto", 12, QFont.Weight.Bold))
        install_btn.setFixedHeight(40)
        install_btn.clicked.connect(lambda: self.install_requested.emit(self.app_data))
        layout.addWidget(install_btn)
        
        # Aplicar estilos
        self.apply_styles()
        
    def apply_styles(self):
        """Aplicar estilos a la tarjeta"""
        self.setStyleSheet(f"""
            #appCard {{
                background-color: {self.theme['terminal_bg']};
                border: 2px solid {self.theme['border_color']};
                border-radius: 15px;
            }}
            #appCard:hover {{
                border-color: {self.theme['accent']};
                background-color: {self.theme['bg']};
            }}
            #appName {{
                color: {self.theme['accent']};
            }}
            #appCategory {{
                color: {self.theme['status_fg']};
            }}
            #appDescription {{
                color: {self.theme['fg']};
            }}
            #appInfo {{
                color: {self.theme['status_fg']};
            }}
            #installButton {{
                background-color: {self.theme['button_bg']};
                color: {self.theme['button_fg']};
                border: none;
                border-radius: 8px;
                padding: 8px;
            }}
            #installButton:hover {{
                background-color: {self.theme['accent']};
            }}
            #installButton:pressed {{
                background-color: {self.theme['button_grad_1']};
            }}
        """)


class DependenciesWidget(QWidget):
    """Widget para la App Store"""
    
    def __init__(self, theme_manager, current_theme, parent=None):
        super().__init__(parent)
        
        self.theme_manager = theme_manager
        self.current_theme = current_theme
        self.installer_thread = None
        
        # Base de datos de aplicaciones
        self.apps_database = self.create_apps_database()
        
        self.setup_fonts()
        self.setup_ui()
        self.apply_theme()
        self.load_apps()
    
    def setup_fonts(self):
        """Configurar fuentes personalizadas"""
        self.title_font = QFont("Roboto", 20, QFont.Weight.Bold)
        self.subtitle_font = QFont("Roboto", 14, QFont.Weight.Normal)
    
    def create_apps_database(self):
        """Crear base de datos de aplicaciones disponibles"""
        return {
            # Navegadores Web
            "firefox": {
                "name": "Firefox",
                "category": "Navegadores",
                "description": "Navegador web rápido, privado y seguro de Mozilla",
                "icon": "🦊",
                "package": "firefox",
                "install_method": "apt",
                "size": "~280 MB"
            },
            "google-chrome": {
                "name": "Google Chrome",
                "category": "Navegadores", 
                "description": "Navegador web de Google con sincronización",
                "icon": "🌐",
                "install_method": "custom_command",
                "custom_command": "wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && sh -c 'echo \"deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main\" >> /etc/apt/sources.list.d/google.list' && apt update && apt install -y google-chrome-stable",
                "size": "~90 MB"
            },
            "brave": {
                "name": "Brave Browser",
                "category": "Navegadores", 
                "description": "Navegador enfocado en privacidad con bloqueador de anuncios",
                "icon": "🦁",
                "install_method": "custom_command",
                "custom_command": "apt install -y apt-transport-https curl && curl -s https://brave-browser-apt-release.s3.brave.com/brave-core.asc | apt-key --keyring /etc/apt/trusted.gpg.d/brave-browser-release.gpg add - && echo 'deb [arch=amd64] https://brave-browser-apt-release.s3.brave.com/ stable main' | tee /etc/apt/sources.list.d/brave-browser-release.list && apt update && apt install -y brave-browser",
                "size": "~80 MB"
            },
            "chromium": {
                "name": "Chromium",
                "category": "Navegadores", 
                "description": "Versión de código abierto de Chrome",
                "icon": "🧩",
                "package": "chromium-browser",
                "install_method": "apt",
                "size": "~80 MB"
            },
            
            # Editores de Código
            "vscode": {
                "name": "Visual Studio Code",
                "category": "Desarrollo",
                "description": "Editor de código potente y gratuito de Microsoft",
                "icon": "💻",
                "install_method": "custom_command",
                "custom_command": "wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg && install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/ && sh -c 'echo \"deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main\" > /etc/apt/sources.list.d/vscode.list' && apt update && apt install -y code",
                "size": "~170 MB"
            },
            "sublime": {
                "name": "Sublime Text",
                "category": "Desarrollo",
                "description": "Editor de texto sofisticado para código y marcado",
                "icon": "✨",
                "install_method": "custom_command",
                "custom_command": "wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | apt-key add - && echo 'deb https://download.sublimetext.com/ apt/stable/' | tee /etc/apt/sources.list.d/sublime-text.list && apt update && apt install -y sublime-text",
                "size": "~25 MB"
            },
            "nano": {
                "name": "Nano Editor",
                "category": "Desarrollo",
                "description": "Editor de texto simple y fácil de usar para terminal",
                "icon": "📝",
                "package": "nano",
                "install_method": "apt",
                "size": "~500 KB"
            },
            "vim": {
                "name": "Vim",
                "category": "Desarrollo",
                "description": "Editor de texto avanzado y potente",
                "icon": "⚡",
                "package": "vim",
                "install_method": "apt",
                "size": "~3 MB"
            },
            "git": {
                "name": "Git",
                "category": "Desarrollo",
                "description": "Sistema de control de versiones distribuido",
                "icon": "🐙",
                "package": "git",
                "install_method": "apt",
                "size": "~30 MB"
            },
            
            # Multimedia
            "vlc": {
                "name": "VLC Media Player",
                "category": "Multimedia",
                "description": "Reproductor multimedia gratuito y de código abierto",
                "icon": "🎬",
                "package": "vlc",
                "install_method": "apt",
                "size": "~50 MB"
            },
            "gimp": {
                "name": "GIMP",
                "category": "Multimedia",
                "description": "Editor de imágenes profesional y gratuito",
                "icon": "🎨",
                "package": "gimp",
                "install_method": "apt",
                "size": "~200 MB"
            },
            "spotify": {
                "name": "Spotify",
                "category": "Multimedia", 
                "description": "Plataforma de música en streaming",
                "icon": "🎵",
                "install_method": "custom_command",
                "custom_command": "curl -sS https://download.spotify.com/debian/pubkey_5E3C45D7B312C643.gpg | apt-key add - && echo 'deb http://repository.spotify.com stable non-free' | tee /etc/apt/sources.list.d/spotify.list && apt update && apt install -y spotify-client",
                "size": "~170 MB"
            },
            "obs-studio": {
                "name": "OBS Studio",
                "category": "Multimedia",
                "description": "Software para grabación y streaming",
                "icon": "🎥",
                "package": "obs-studio",
                "install_method": "apt",
                "size": "~120 MB"
            },
            "audacity": {
                "name": "Audacity",
                "category": "Multimedia",
                "description": "Editor de audio multipista",
                "icon": "🔊",
                "package": "audacity",
                "install_method": "apt",
                "size": "~30 MB"
            },
            
            # Herramientas del Sistema
            "htop": {
                "name": "htop",
                "category": "Sistema",
                "description": "Monitor de procesos interactivo para terminal",
                "icon": "📊",
                "package": "htop",
                "install_method": "apt",
                "size": "~500 KB"
            },
            "curl": {
                "name": "cURL",
                "category": "Sistema",
                "description": "Herramienta para transferir datos desde servidores",
                "icon": "🌍",
                "package": "curl",
                "install_method": "apt",
                "size": "~500 KB"
            },
            "flameshot": {
                "name": "Flameshot",
                "category": "Sistema",
                "description": "Herramienta de captura de pantalla potente",
                "icon": "📸",
                "package": "flameshot",
                "install_method": "apt",
                "size": "~1.5 MB"
            },
            "neofetch": {
                "name": "Neofetch",
                "category": "Sistema",
                "description": "Herramienta para mostrar información del sistema de forma atractiva",
                "icon": "🖥️",
                "package": "neofetch",
                "install_method": "apt",
                "size": "~500 KB"
            },
            "tree": {
                "name": "Tree",
                "category": "Sistema",
                "description": "Comando para mostrar directorios en forma de árbol",
                "icon": "🌳",
                "package": "tree",
                "install_method": "apt",
                "size": "~100 KB"
            },
            
            # Comunicación
            "discord": {
                "name": "Discord",
                "category": "Comunicación",
                "description": "Plataforma de comunicación para comunidades",
                "icon": "💬",
                "install_method": "custom_command",
                "custom_command": "wget -O /tmp/discord.deb 'https://discordapp.com/api/download?platform=linux&format=deb' && apt install -y /tmp/discord.deb",
                "size": "~150 MB"
            },
            "telegram": {
                "name": "Telegram",
                "category": "Comunicación",
                "description": "Aplicación de mensajería rápida y segura",
                "icon": "✈️",
                "package": "telegram-desktop",
                "install_method": "apt",
                "size": "~50 MB"
            },
            "thunderbird": {
                "name": "Thunderbird",
                "category": "Comunicación",
                "description": "Cliente de correo electrónico de Mozilla",
                "icon": "📧",
                "package": "thunderbird",
                "install_method": "apt",
                "size": "~100 MB"
            },
            
            # Juegos
            "steam": {
                "name": "Steam",
                "category": "Juegos",
                "description": "Plataforma de distribución digital de videojuegos",
                "icon": "🎮",
                "package": "steam",
                "install_method": "apt",
                "size": "~300 MB"
            },
            
            # Oficina
            "libreoffice": {
                "name": "LibreOffice",
                "category": "Oficina",
                "description": "Suite ofimática completa y de código abierto",
                "icon": "📝",
                "package": "libreoffice",
                "install_method": "apt",
                "size": "~350 MB"
            }
        }
    
    def setup_ui(self):
        """Crear la interfaz de usuario de la App Store"""
        self.setObjectName("modeWidget")
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Título
        title_frame = QFrame()
        title_frame.setObjectName("titleFrame")
        title_layout = QVBoxLayout(title_frame)
        title_layout.setContentsMargins(20, 15, 20, 15)
        
        title = QLabel("🏪 APP STORE")
        title.setObjectName("storeTitle")
        title.setFont(self.title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(title)
        
        subtitle = QLabel("Instala aplicaciones populares con un solo clic")
        subtitle.setObjectName("storeSubtitle")
        subtitle.setFont(self.subtitle_font)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(subtitle)
        
        main_layout.addWidget(title_frame)
        
        # Barra de búsqueda y filtros
        search_frame = QFrame()
        search_frame.setObjectName("searchFrame")
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(15, 10, 15, 10)
        
        # Campo de búsqueda
        search_label = QLabel("🔍")
        search_label.setFont(QFont("Arial", 16))
        search_layout.addWidget(search_label)
        
        self.search_field = QLineEdit()
        self.search_field.setObjectName("searchField")
        self.search_field.setPlaceholderText("Buscar aplicaciones...")
        self.search_field.setFont(QFont("Roboto", 12))
        self.search_field.textChanged.connect(self.filter_apps)
        search_layout.addWidget(self.search_field)
        
        # Filtro por categoría
        category_label = QLabel("📂")
        category_label.setFont(QFont("Arial", 16))
        search_layout.addWidget(category_label)
        
        self.category_filter = QComboBox()
        self.category_filter.setObjectName("categoryFilter")
        self.category_filter.setFont(QFont("Roboto", 12))
        self.category_filter.addItems(["Todas las categorías", "Navegadores", "Desarrollo", "Multimedia", "Sistema", "Comunicación", "Juegos", "Oficina"])
        self.category_filter.currentTextChanged.connect(self.filter_apps)
        search_layout.addWidget(self.category_filter)
        
        main_layout.addWidget(search_frame)
        
        # Área de aplicaciones
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Panel de aplicaciones
        apps_scroll = QScrollArea()
        apps_scroll.setObjectName("appsScroll")
        apps_scroll.setWidgetResizable(True)
        apps_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        apps_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.apps_container = QWidget()
        self.apps_layout = QGridLayout(self.apps_container)
        self.apps_layout.setSpacing(20)
        self.apps_layout.setContentsMargins(20, 20, 20, 20)
        
        apps_scroll.setWidget(self.apps_container)
        content_splitter.addWidget(apps_scroll)
        
        # Panel de información de instalación
        info_panel = QFrame()
        info_panel.setObjectName("infoPanel")
        info_panel.setFixedWidth(350)
        info_layout = QVBoxLayout(info_panel)
        info_layout.setContentsMargins(15, 15, 15, 15)
        
        info_title = QLabel("📋 Estado de Instalación")
        info_title.setFont(QFont("Roboto", 14, QFont.Weight.Bold))
        info_title.setObjectName("infoTitle")
        info_layout.addWidget(info_title)
        
        # Área de progreso
        self.progress_area = QTextEdit()
        self.progress_area.setObjectName("progressArea")
        self.progress_area.setFont(QFont("JetBrains Mono", 10))
        self.progress_area.setReadOnly(True)
        self.progress_area.setMaximumHeight(200)
        info_layout.addWidget(self.progress_area)
        
        # Botón para limpiar log
        clear_btn = QPushButton("🗑️ Limpiar Log")
        clear_btn.setObjectName("clearButton")
        clear_btn.clicked.connect(self.progress_area.clear)
        info_layout.addWidget(clear_btn)
        
        info_layout.addStretch()
        content_splitter.addWidget(info_panel)
        
        # Establecer tamaños relativos (70% apps, 30% info)
        content_splitter.setSizes([700, 300])
        
        main_layout.addWidget(content_splitter)
    
    def load_apps(self):
        """Cargar las aplicaciones en la interfaz"""
        # Limpiar layout
        for i in reversed(range(self.apps_layout.count())): 
            self.apps_layout.itemAt(i).widget().setParent(None)
        
        # Obtener lista filtrada
        filtered_apps = self.get_filtered_apps()
        
        # Agregar aplicaciones en grid
        row, col = 0, 0
        max_cols = 3
        
        theme = self.theme_manager.get_theme(self.current_theme)
        
        for app_id, app_data in filtered_apps.items():
            card = AppCard(app_data, theme)
            card.install_requested.connect(self.install_app)
            
            self.apps_layout.addWidget(card, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    def get_filtered_apps(self):
        """Obtener aplicaciones filtradas por búsqueda y categoría"""
        search_text = self.search_field.text().lower()
        selected_category = self.category_filter.currentText()
        
        filtered = {}
        for app_id, app_data in self.apps_database.items():
            # Filtrar por búsqueda
            if search_text and search_text not in app_data['name'].lower() and search_text not in app_data['description'].lower():
                continue
                
            # Filtrar por categoría
            if selected_category != "Todas las categorías" and app_data['category'] != selected_category:
                continue
                
            filtered[app_id] = app_data
        
        return filtered
    
    def filter_apps(self):
        """Filtrar aplicaciones según criterios de búsqueda"""
        self.load_apps()
    
    def install_app(self, app_data):
        """Instalar una aplicación"""
        # Solicitar contraseña
        password, ok = QInputDialog.getText(
            self, 
            "Contraseña requerida", 
            f"Para instalar {app_data['name']} se requieren permisos de administrador.\nIngresa tu contraseña:",
            QLineEdit.EchoMode.Password
        )
        
        if not ok or not password:
            self.progress_area.append("❌ Instalación cancelada por el usuario.\n")
            return
        
        # Limpiar área de progreso
        self.progress_area.clear()
        self.progress_area.append(f"🚀 Iniciando instalación de {app_data['name']}...\n")
        
        # Crear e iniciar hilo de instalación
        self.installer_thread = AppInstaller(app_data, password)
        self.installer_thread.progress_update.connect(self.update_progress)
        self.installer_thread.installation_finished.connect(self.installation_finished)
        self.installer_thread.start()
    
    def update_progress(self, message):
        """Actualizar el progreso de instalación"""
        self.progress_area.append(message)
        # Auto-scroll
        cursor = self.progress_area.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.progress_area.setTextCursor(cursor)
    
    def installation_finished(self, success, message):
        """Manejar finalización de instalación"""
        self.progress_area.append(f"\n{message}\n")
        
        if success:
            QMessageBox.information(self, "Instalación Completada", message)
        else:
            QMessageBox.warning(self, "Error de Instalación", message)
    
    def apply_theme(self):
        """Aplicar tema al widget"""
        theme = self.theme_manager.get_theme(self.current_theme)
        
        self.setStyleSheet(f"""
            #modeWidget {{
                background-color: {theme['bg']};
                color: {theme['fg']};
            }}
            #titleFrame, #searchFrame, #infoPanel {{
                background-color: {theme['terminal_bg']};
                border: 1px solid {theme['border_color']};
                border-radius: 10px;
            }}
            #storeTitle {{
                color: {theme['accent']};
            }}
            #storeSubtitle {{
                color: {theme['status_fg']};
            }}
            #searchField, #categoryFilter {{
                background-color: {theme['bg']};
                color: {theme['fg']};
                border: 1px solid {theme['border_color']};
                border-radius: 5px;
                padding: 8px;
            }}
            #appsScroll {{
                background-color: {theme['bg']};
                border: none;
            }}
            #progressArea {{
                background-color: {theme['terminal_bg']};
                color: {theme['fg']};
                border: 1px solid {theme['border_color']};
                border-radius: 5px;
            }}
            #clearButton {{
                background-color: {theme['button_bg']};
                color: {theme['button_fg']};
                border: none;
                border-radius: 5px;
                padding: 8px;
            }}
            #clearButton:hover {{
                background-color: {theme['accent']};
            }}
        """)
    
    def change_theme(self, theme_name):
        """Cambiar tema del widget"""
        self.current_theme = theme_name
        self.apply_theme()
        self.load_apps()  # Recargar para aplicar tema a las tarjetas
