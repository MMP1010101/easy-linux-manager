#!/usr/bin/env python3
"""
Easy Mode widget para la aplicación Linux GUI
Menú con opciones: Files, Scripts, Play
"""

import os
import shutil
from pathlib import Path
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QListWidget, QListWidgetItem, QPushButton, 
                           QInputDialog, QMessageBox, QSplitter,
                           QFrame, QTextEdit, QScrollArea, QStackedWidget,
                           QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QPixmap


class FileExplorerItem(QListWidgetItem):
    """Item personalizado para el explorador de archivos con mejor visualización"""
    
    def __init__(self, name, path, is_directory=False):
        super().__init__()
        self.file_name = name
        self.file_path = path
        self.is_directory = is_directory
        
        # Configurar icono y texto con mejor formato
        if is_directory:
            self.setText(f"📁  {name}")
        else:
            # Detectar tipo de archivo para mejor iconografía
            extension = Path(name).suffix.lower()
            if extension in ['.txt', '.md', '.readme']:
                icon = "📄"
            elif extension in ['.py', '.js', '.html', '.css', '.json']:
                icon = "💻"
            elif extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
                icon = "🖼️"
            elif extension in ['.mp3', '.wav', '.flac', '.ogg']:
                icon = "🎵"
            elif extension in ['.mp4', '.avi', '.mkv', '.mov']:
                icon = "🎬"
            elif extension in ['.zip', '.tar', '.gz', '.rar']:
                icon = "📦"
            elif extension in ['.pdf']:
                icon = "📋"
            else:
                icon = "📄"
            
            self.setText(f"{icon}  {name}")
        
        # Tooltip con información detallada del archivo
        size_info = self._get_size_info(Path(path))
        self.setToolTip(f"📍 Ruta: {path}\n🔖 Tipo: {'Carpeta' if is_directory else 'Archivo'}\n📏 {size_info}")
    
    def _get_size_info(self, path):
        """Obtener información de tamaño del archivo"""
        try:
            if path.is_file():
                size = path.stat().st_size
                if size < 1024:
                    return f"Tamaño: {size} bytes"
                elif size < 1024 * 1024:
                    return f"Tamaño: {size / 1024:.1f} KB"
                else:
                    return f"Tamaño: {size / (1024 * 1024):.1f} MB"
            else:
                return "Tamaño: Carpeta"
        except:
            return "Tamaño: No disponible"


class FileExplorerWidget(QWidget):
    """Widget del explorador de archivos"""
    
    def __init__(self, theme_manager, current_theme, parent=None):
        super().__init__(parent)
        
        self.theme_manager = theme_manager
        self.current_theme = current_theme
        self.current_path = Path.home()  # Comenzar en el directorio home del usuario
        
        self.setup_fonts()
        self.setup_ui()
        self.load_directory()
    
    def setup_fonts(self):
        """Configurar fuentes personalizadas"""
        self.title_font = QFont("Roboto", 18, QFont.Weight.Bold)
        self.menu_font = QFont("Roboto", 12, QFont.Weight.Normal)
        self.path_font = QFont("JetBrains Mono", 12, QFont.Weight.Bold)  # Aumentado de 10 a 12
    
    def setup_ui(self):
        """Crear la interfaz de usuario del explorador"""
        self.setObjectName("modeWidget")
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)
        
        # Título con estilo mejorado
        title_frame = QFrame()
        title_frame.setObjectName("titleFrame")
        title_layout = QVBoxLayout(title_frame)
        title_layout.setContentsMargins(20, 15, 20, 15)
        
        title = QLabel("📁 EXPLORADOR DE ARCHIVOS")
        title.setObjectName("easyTitle")
        title.setFont(self.title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(title)
        
        subtitle = QLabel("Gestiona tus archivos de forma visual e intuitiva")
        subtitle.setObjectName("subtitle")
        subtitle.setFont(QFont("Roboto", 12, QFont.Weight.Normal))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(f"color: {self.theme_manager.get_theme(self.current_theme)['status_fg']}; margin-top: 5px;")
        title_layout.addWidget(subtitle)
        
        main_layout.addWidget(title_frame)
        
        # Barra de navegación mejorada
        nav_frame = QFrame()
        nav_frame.setObjectName("navFrame")
        nav_layout = QHBoxLayout(nav_frame)
        nav_layout.setContentsMargins(20, 15, 20, 15)
        nav_layout.setSpacing(15)
        
        # Botón atrás con mejor estilo
        self.back_button = QPushButton("⬅️")
        self.back_button.setObjectName("navButton")
        self.back_button.setFixedSize(50, 50)
        self.back_button.clicked.connect(self.go_back)
        nav_layout.addWidget(self.back_button)
        
        # Ruta actual con MUCHO mejor presentación
        path_container = QFrame()
        path_container.setObjectName("pathContainer")
        path_container_layout = QHBoxLayout(path_container)
        path_container_layout.setContentsMargins(15, 10, 15, 10)
        
        path_icon = QLabel("📍")
        path_icon.setFont(QFont("Arial", 18))  # Aumentado aún más
        path_container_layout.addWidget(path_icon)
        
        self.path_label = QLabel()
        self.path_label.setObjectName("pathLabel")
        self.path_label.setFont(QFont("JetBrains Mono", 14, QFont.Weight.Bold))  # Aumentado a 14
        self.path_label.setWordWrap(True)
        self.path_label.setMinimumHeight(50)  # Aumentar altura mínima
        self.path_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)  # Alinear verticalmente
        path_container_layout.addWidget(self.path_label, 1)
        
        nav_layout.addWidget(path_container, 1)
        
        # Botón home con mejor estilo
        self.home_button = QPushButton("🏠")
        self.home_button.setObjectName("navButton")
        self.home_button.setFixedSize(50, 50)
        self.home_button.clicked.connect(self.go_home)
        nav_layout.addWidget(self.home_button)
        
        main_layout.addWidget(nav_frame)
        
        # Contenedor principal con splitter
        content_frame = QFrame()
        content_frame.setObjectName("contentFrame")
        content_layout = QHBoxLayout(content_frame)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(20)
        
        # Splitter para dividir lista de archivos y panel de acciones
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)
        
        # Lista de archivos y carpetas con mejor diseño
        files_container = QFrame()
        files_container.setObjectName("filesContainer")
        files_layout = QVBoxLayout(files_container)
        files_layout.setContentsMargins(15, 15, 15, 15)
        
        files_title = QLabel("📂 Contenido del directorio")
        files_title.setFont(QFont("Roboto", 14, QFont.Weight.Bold))
        files_title.setObjectName("sectionTitle")
        files_layout.addWidget(files_title)
        
        self.file_list = QListWidget()
        self.file_list.setObjectName("fileList")
        self.file_list.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.file_list.itemClicked.connect(self.on_item_clicked)
        files_layout.addWidget(self.file_list)
        
        splitter.addWidget(files_container)
        
        # Panel de acciones mejorado - Botones como calculadora
        actions_frame = QFrame()
        actions_frame.setObjectName("actionsFrame")
        actions_frame.setFixedWidth(300)
        actions_layout = QVBoxLayout(actions_frame)
        actions_layout.setContentsMargins(20, 20, 20, 20)
        actions_layout.setSpacing(15)
        
        # Título del panel
        actions_title = QLabel("⚡ ACCIONES")
        actions_title.setObjectName("actionsTitle")
        actions_title.setFont(QFont("Roboto", 16, QFont.Weight.Bold))
        actions_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        actions_layout.addWidget(actions_title)
        
        # Información del item seleccionado
        info_label = QLabel("📊 Información del elemento")
        info_label.setFont(QFont("Roboto", 12, QFont.Weight.Bold))
        info_label.setObjectName("infoLabel")
        actions_layout.addWidget(info_label)
        
        self.item_info = QTextEdit()
        self.item_info.setObjectName("itemInfo")
        self.item_info.setMaximumHeight(120)
        self.item_info.setReadOnly(True)
        self.item_info.setPlainText("Selecciona un archivo o carpeta para ver información detallada")
        actions_layout.addWidget(self.item_info)
        
        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        actions_layout.addWidget(separator)
        
        # Botones de acción organizados en GRID como calculadora
        actions_label = QLabel("🛠️ Herramientas")
        actions_label.setFont(QFont("Roboto", 12, QFont.Weight.Bold))
        actions_label.setObjectName("actionsLabel")
        actions_layout.addWidget(actions_label)
        
        # Grid layout para los botones
        buttons_grid = QFrame()
        grid_layout = QGridLayout(buttons_grid)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setSpacing(8)  # Espacio reducido entre botones
        
        # Crear nueva carpeta - Posición 0,0
        self.create_folder_btn = QPushButton("📁\nCarpeta")
        self.create_folder_btn.setObjectName("calcButton")
        self.create_folder_btn.setFixedSize(120, 80)
        self.create_folder_btn.clicked.connect(self.create_folder)
        grid_layout.addWidget(self.create_folder_btn, 0, 0)
        
        # Crear nuevo archivo - Posición 0,1
        self.create_file_btn = QPushButton("📄\nArchivo")
        self.create_file_btn.setObjectName("calcButton")
        self.create_file_btn.setFixedSize(120, 80)
        self.create_file_btn.clicked.connect(self.create_file)
        grid_layout.addWidget(self.create_file_btn, 0, 1)
        
        # Renombrar - Posición 1,0
        self.rename_btn = QPushButton("✏️\nRenombrar")
        self.rename_btn.setObjectName("calcButton")
        self.rename_btn.setFixedSize(120, 80)
        self.rename_btn.clicked.connect(self.rename_selected)
        self.rename_btn.setEnabled(False)
        grid_layout.addWidget(self.rename_btn, 1, 0)
        
        # Eliminar seleccionado - Posición 1,1
        self.delete_btn = QPushButton("🗑️\nEliminar")
        self.delete_btn.setObjectName("deleteCalcButton")
        self.delete_btn.setFixedSize(120, 80)
        self.delete_btn.clicked.connect(self.delete_selected)
        self.delete_btn.setEnabled(False)
        grid_layout.addWidget(self.delete_btn, 1, 1)
        
        # Añadir el grid al layout principal
        actions_layout.addWidget(buttons_grid)
        
        splitter.addWidget(actions_frame)
        splitter.setSizes([500, 300])
        
        content_layout.addWidget(splitter)
        main_layout.addWidget(content_frame)
    
    def load_directory(self):
        """Cargar el contenido del directorio actual"""
        self.file_list.clear()
        
        # MEJOR VISUALIZACIÓN DE LA RUTA - usando colores y formato más visible
        path_str = str(self.current_path)
        home_dir = str(Path.home())
        
        # Aplicar formato extremadamente visible a la ruta
        if path_str.startswith(home_dir):
            rel_path = path_str[len(home_dir):]
            if not rel_path:
                # Si estamos en Home, mostrar de forma muy clara
                formatted_path = "🏠 CARPETA PERSONAL"
            else:
                # Formatear ruta relativa con separadores muy visibles
                path_parts = rel_path.strip('/').split('/')
                formatted_path = "🏠 " + " ➡️ ".join(['INICIO'] + path_parts)
        else:
            # Para rutas absolutas, formato claro con separadores visibles
            path_parts = path_str.strip('/').split('/')
            formatted_path = "/ " + " / ".join(path_parts)
            
        # Usar HTML para mejorar la visualización con colores
        html_path = f"<b style='color: white; font-size: 16px;'>{formatted_path}</b>"
        self.path_label.setText(html_path)
        self.path_label.setTextFormat(Qt.TextFormat.RichText)
        
        try:
            # Obtener lista de archivos y carpetas
            items = []
            
            # Agregar carpetas primero
            for item in self.current_path.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    items.append((item.name, item, True))
            
            # Luego agregar archivos
            for item in self.current_path.iterdir():
                if item.is_file() and not item.name.startswith('.'):
                    items.append((item.name, item, False))
            
            # Ordenar por nombre
            items.sort(key=lambda x: x[0].lower())
            
            # Agregar a la lista
            for name, path, is_dir in items:
                list_item = FileExplorerItem(name, str(path), is_dir)
                self.file_list.addItem(list_item)
                
        except PermissionError:
            QMessageBox.warning(self, "Sin permisos", 
                              "No tienes permisos para acceder a esta carpeta.")
            self.go_back()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar directorio: {str(e)}")
    
    def on_item_double_clicked(self, item):
        """Manejar doble clic en un item"""
        if isinstance(item, FileExplorerItem) and item.is_directory:
            self.current_path = Path(item.file_path)
            self.load_directory()
    
    def on_item_clicked(self, item):
        """Manejar clic simple en un item"""
        if isinstance(item, FileExplorerItem):
            # Habilitar botones de acción
            self.delete_btn.setEnabled(True)
            self.rename_btn.setEnabled(True)
            
            # Mostrar información del item
            path = Path(item.file_path)
            info = f"Nombre: {item.file_name}\n"
            info += f"Tipo: {'Carpeta' if item.is_directory else 'Archivo'}\n"
            
            try:
                stat = path.stat()
                size = stat.st_size
                if size < 1024:
                    size_str = f"{size} bytes"
                elif size < 1024 * 1024:
                    size_str = f"{size / 1024:.1f} KB"
                else:
                    size_str = f"{size / (1024 * 1024):.1f} MB"
                info += f"Tamaño: {size_str}\n"
            except:
                info += "Tamaño: No disponible\n"
            
            info += f"Ruta: {item.file_path}"
            self.item_info.setPlainText(info)
    
    def go_back(self):
        """Ir al directorio padre"""
        if self.current_path != self.current_path.parent:
            self.current_path = self.current_path.parent
            self.load_directory()
            self.clear_selection()
    
    def go_home(self):
        """Ir al directorio home"""
        self.current_path = Path.home()
        self.load_directory()
        self.clear_selection()
    
    def clear_selection(self):
        """Limpiar selección"""
        self.file_list.clearSelection()
        self.delete_btn.setEnabled(False)
        self.rename_btn.setEnabled(False)
        self.item_info.setPlainText("Selecciona un archivo o carpeta para ver información")
    
    def create_folder(self):
        """Crear nueva carpeta"""
        if not self.is_in_user_directory():
            QMessageBox.warning(self, "Ubicación no permitida", 
                              "Solo puedes crear carpetas dentro de tu directorio personal.")
            return
        
        name, ok = QInputDialog.getText(self, "Nueva Carpeta", "Nombre de la carpeta:")
        if ok and name:
            try:
                new_folder = self.current_path / name
                new_folder.mkdir(exist_ok=False)
                self.load_directory()
                QMessageBox.information(self, "Éxito", f"Carpeta '{name}' creada correctamente.")
            except FileExistsError:
                QMessageBox.warning(self, "Error", "Ya existe una carpeta con ese nombre.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al crear carpeta: {str(e)}")
    
    def create_file(self):
        """Crear nuevo archivo"""
        if not self.is_in_user_directory():
            QMessageBox.warning(self, "Ubicación no permitida", 
                              "Solo puedes crear archivos dentro de tu directorio personal.")
            return
        
        name, ok = QInputDialog.getText(self, "Nuevo Archivo", "Nombre del archivo:")
        if ok and name:
            try:
                new_file = self.current_path / name
                new_file.touch(exist_ok=False)
                self.load_directory()
                QMessageBox.information(self, "Éxito", f"Archivo '{name}' creado correctamente.")
            except FileExistsError:
                QMessageBox.warning(self, "Error", "Ya existe un archivo con ese nombre.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al crear archivo: {str(e)}")
    
    def delete_selected(self):
        """Eliminar el item seleccionado"""
        current_item = self.file_list.currentItem()
        if not isinstance(current_item, FileExplorerItem):
            return
        
        if not self.is_in_user_directory():
            QMessageBox.warning(self, "Ubicación no permitida", 
                              "Solo puedes eliminar archivos dentro de tu directorio personal.")
            return
        
        # Confirmar eliminación
        reply = QMessageBox.question(self, "Confirmar eliminación", 
                                   f"¿Estás seguro de que quieres eliminar '{current_item.file_name}'?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                   QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                path = Path(current_item.file_path)
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
                
                self.load_directory()
                self.clear_selection()
                QMessageBox.information(self, "Éxito", f"'{current_item.file_name}' eliminado correctamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar: {str(e)}")
    
    def rename_selected(self):
        """Renombrar el item seleccionado"""
        current_item = self.file_list.currentItem()
        if not isinstance(current_item, FileExplorerItem):
            return
        
        if not self.is_in_user_directory():
            QMessageBox.warning(self, "Ubicación no permitida", 
                              "Solo puedes renombrar archivos dentro de tu directorio personal.")
            return
        
        new_name, ok = QInputDialog.getText(self, "Renombrar", 
                                          f"Nuevo nombre para '{current_item.file_name}':",
                                          text=current_item.file_name)
        if ok and new_name and new_name != current_item.file_name:
            try:
                old_path = Path(current_item.file_path)
                new_path = old_path.parent / new_name
                old_path.rename(new_path)
                
                self.load_directory()
                self.clear_selection()
                QMessageBox.information(self, "Éxito", f"Renombrado a '{new_name}' correctamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al renombrar: {str(e)}")
    
    def is_in_user_directory(self):
        """Verificar si estamos dentro del directorio del usuario"""
        try:
            self.current_path.relative_to(Path.home())
            return True
        except ValueError:
            return False
    
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


class ScriptsWidget(QWidget):
    """Widget para la sección Scripts"""
    
    def __init__(self, theme_manager, current_theme, parent=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.current_theme = current_theme
        self.setup_ui()
    
    def setup_ui(self):
        """Crear la interfaz de Scripts"""
        self.setObjectName("modeWidget")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        
        title = QLabel("📜 SCRIPTS")
        title.setObjectName("easyTitle")
        title.setFont(QFont("Roboto", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        info = QLabel("Funcionalidad de Scripts estará disponible próximamente...")
        info.setObjectName("modeInfo")
        info.setFont(QFont("Roboto", 14, QFont.Weight.Normal))
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)
        
        layout.addStretch()


class PlayWidget(QWidget):
    """Widget para la sección Play"""
    
    def __init__(self, theme_manager, current_theme, parent=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.current_theme = current_theme
        self.setup_ui()
    
    def setup_ui(self):
        """Crear la interfaz de Play"""
        self.setObjectName("modeWidget")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        
        title = QLabel("🎮 PLAY")
        title.setObjectName("easyTitle")
        title.setFont(QFont("Roboto", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        info = QLabel("Funcionalidad de Juegos estará disponible próximamente...")
        info.setObjectName("modeInfo")
        info.setFont(QFont("Roboto", 14, QFont.Weight.Normal))
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)
        
        layout.addStretch()


class EasyWidget(QWidget):
    """Widget principal para el modo Easy con menú"""
    
    def __init__(self, theme_manager, current_theme, parent=None):
        super().__init__(parent)
        
        self.theme_manager = theme_manager
        self.current_theme = current_theme
        self.parent_window = parent
        
        self.setup_fonts()
        self.setup_ui()
        self.apply_theme()
    
    def setup_fonts(self):
        """Configurar fuentes personalizadas"""
        self.menu_font = QFont("Roboto", 14, QFont.Weight.Bold)
    
    def setup_ui(self):
        """Crear la interfaz de usuario del menú Easy"""
        # Layout principal horizontal
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Set object name for theme styling
        self.setObjectName("menuPageWidget")
        
        # Área para los botones en el lado izquierdo (opuesto al menú principal)
        self.create_buttons_area(layout)
        
        # Área para la imagen del logo en el lado derecho
        self.create_logo_area(layout)
    
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
        
        # Título del menú Easy
        title_label = QLabel("✨ EASY MODE")
        title_label.setObjectName("menuTitle")
        title_label.setFont(QFont("Roboto", 20, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        buttons_layout.addWidget(title_label)
        
        # Botón Files
        files_button = QPushButton("📁 files")
        files_button.setObjectName("menuButton")
        files_button.setFont(self.menu_font)
        files_button.setFixedSize(400, 80)
        files_button.clicked.connect(self.show_files)
        buttons_layout.addWidget(files_button)
        
        # Botón Scripts
        scripts_button = QPushButton("📜 scripts")
        scripts_button.setObjectName("menuButton")
        scripts_button.setFont(self.menu_font)
        scripts_button.setFixedSize(400, 80)
        scripts_button.clicked.connect(self.show_scripts)
        buttons_layout.addWidget(scripts_button)
        
        # Botón Play
        play_button = QPushButton("🎮 play")
        play_button.setObjectName("menuButton")
        play_button.setFont(self.menu_font)
        play_button.setFixedSize(400, 80)
        play_button.clicked.connect(self.show_play)
        buttons_layout.addWidget(play_button)
        
        # Botón para regresar al menú principal
        back_button = QPushButton("⬅️ Regresar")
        back_button.setObjectName("backButton")
        back_button.setFont(self.menu_font)
        back_button.setFixedSize(200, 50)
        if self.parent_window:
            back_button.clicked.connect(self.parent_window.show_menu)
        buttons_layout.addWidget(back_button)
        
        layout.addWidget(buttons_area, 1)
    
    def create_logo_area(self, layout):
        """Crear área del logo (lado derecho)"""
        logo_area = QWidget()
        logo_area.setMinimumWidth(550)  # Forzar un ancho mínimo grande
        logo_area.setObjectName("logoArea")
        logo_layout = QVBoxLayout(logo_area)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setSpacing(0)
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Logo alternativo para Easy Mode (puede ser diferente al principal)
        eye_logo = QLabel()
        eye_logo.setObjectName("logoLabel")
        # Llenar todo el espacio disponible
        eye_logo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logo.png")
        eye_pixmap = QPixmap(logo_path)
        
        if eye_pixmap.isNull():
            # Logo de fallback para Easy Mode
            eye_logo.setText("✨🎯")
            eye_logo.setFont(QFont("Arial", 180, QFont.Weight.Bold))
            eye_logo.setStyleSheet("color: white; background-color: #0d1117;")
            print(f"⚠️ No se pudo cargar la imagen del logo desde: {logo_path}")
        else:
            print(f"✅ Logo cargado correctamente para Easy Mode desde: {logo_path}")
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
    
    def show_files(self):
        """Mostrar el explorador de archivos"""
        if self.parent_window:
            self.parent_window.show_easy_files()
    
    def show_scripts(self):
        """Mostrar la sección de scripts"""
        if self.parent_window:
            self.parent_window.show_easy_scripts()
    
    def show_play(self):
        """Mostrar la sección de juegos"""
        if self.parent_window:
            self.parent_window.show_easy_play()
    
    def apply_theme(self):
        """Aplicar tema al widget"""
        from styles.menu_styles import get_menu_styles
        theme = self.theme_manager.get_theme(self.current_theme)
        menu_styles = get_menu_styles(theme)
        self.setStyleSheet(menu_styles)
    
    def change_theme(self, theme_name):
        """Cambiar tema del widget"""
        self.current_theme = theme_name
        self.apply_theme()
