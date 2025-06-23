#!/usr/bin/env python3
"""
Componente de explorador de archivos para la aplicación Linux GUI
Explorador de archivos independiente y reutil        # Icono de ubicación más prominente
        path_icon = QLabel("📍")
        path_icon.setFont(QFont("Arial", 14))
        path_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        path_container_layout.addWidget(path_icon)e
"""

import os
import shutil
from pathlib import Path
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QListWidget, QListWidgetItem, QPushButton, 
                           QInputDialog, QMessageBox, QSplitter,
                           QFrame, QTextEdit, QScrollArea, QGridLayout)
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
    """Widget del explorador de archivos independiente"""
    
    # Señales para comunicarse con la ventana principal
    file_selected = pyqtSignal(str)  # Emitida cuando se selecciona un archivo
    folder_opened = pyqtSignal(str)  # Emitida cuando se abre una carpeta
    
    def __init__(self, theme_manager, current_theme, start_path=None, parent=None):
        super().__init__(parent)
        
        self.theme_manager = theme_manager
        self.current_theme = current_theme
        self.current_path = Path(start_path) if start_path else Path.home()
        
        self.setup_fonts()
        self.setup_ui()
        self.load_directory()
        self.apply_theme()
        self.position_window_at_top()
    
    def setup_fonts(self):
        """Configurar fuentes personalizadas"""
        self.title_font = QFont("Roboto", 18, QFont.Weight.Bold)
        self.menu_font = QFont("Roboto", 12, QFont.Weight.Normal)
        self.path_font = QFont("JetBrains Mono", 10, QFont.Weight.Normal)
    
    def setup_ui(self):
        """Crear la interfaz de usuario del explorador"""
        self.setObjectName("fileExplorerWidget")
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)
        
        # Barra de navegación
        nav_frame = QFrame()
        nav_frame.setObjectName("navFrame")
        nav_frame.setFixedHeight(45)
        nav_layout = QHBoxLayout(nav_frame)
        nav_layout.setContentsMargins(8, 4, 8, 4)
        nav_layout.setSpacing(8)
        
        # Botones de navegación
        self.back_button = QPushButton("←")
        self.back_button.setObjectName("navButton")
        self.back_button.setFixedSize(32, 32)
        self.back_button.setToolTip("Directorio anterior")
        self.back_button.clicked.connect(self.go_back)
        nav_layout.addWidget(self.back_button)
        
        self.home_button = QPushButton("🏠")
        self.home_button.setObjectName("navButton")
        self.home_button.setFixedSize(32, 32)
        self.home_button.setToolTip("Directorio home")
        self.home_button.clicked.connect(self.go_home)
        nav_layout.addWidget(self.home_button)
        
        # Contenedor de ruta - CORREGIDO
        path_container = QFrame()
        path_container.setObjectName("pathContainer")
        path_container.setMinimumHeight(32)
        path_container_layout = QHBoxLayout(path_container)
        path_container_layout.setContentsMargins(15, 4, 15, 4)
        path_container_layout.setSpacing(10)
        
        # Icono de ubicación - CORREGIDO
        path_icon = QLabel("📍")
        path_icon.setFont(QFont("Arial", 16))
        path_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        path_container_layout.addWidget(path_icon)
        
        # Label de ruta - CORREGIDO
        self.path_label = QLabel()
        self.path_label.setObjectName("pathLabel")
        self.path_label.setFont(QFont("Roboto", 13, QFont.Weight.Bold))
        self.path_label.setWordWrap(False)
        self.path_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.path_label.setMinimumWidth(200)  # Asegurar espacio mínimo para la ruta
        path_container_layout.addWidget(self.path_label, 1)
        
        nav_layout.addWidget(path_container, 1)
        main_layout.addWidget(nav_frame)
        
        # Contenedor principal
        content_frame = QFrame()
        content_frame.setObjectName("contentFrame")
        content_layout = QVBoxLayout(content_frame)  # Cambiado a vertical para mejor organización
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(5)
        
        # Splitter para dividir lista de archivos y panel de acciones
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)
        
        # Lista de archivos
        files_container = QFrame()
        files_container.setObjectName("filesContainer")
        files_layout = QVBoxLayout(files_container)
        files_layout.setContentsMargins(10, 10, 10, 10)
        files_layout.setSpacing(5)
        
        files_title = QLabel("📂 Contenido")
        files_title.setFont(QFont("Roboto", 12, QFont.Weight.Bold))
        files_title.setObjectName("sectionTitle")
        files_layout.addWidget(files_title)
        
        self.file_list = QListWidget()
        self.file_list.setObjectName("fileList")
        self.file_list.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.file_list.itemClicked.connect(self.on_item_clicked)
        files_layout.addWidget(self.file_list)
        
        splitter.addWidget(files_container)
        
        # Panel de herramientas - REORGANIZADO
        actions_frame = QFrame()
        actions_frame.setObjectName("actionsFrame")
        actions_frame.setFixedWidth(210)
        actions_layout = QVBoxLayout(actions_frame)
        actions_layout.setContentsMargins(5, 5, 5, 5)
        actions_layout.setSpacing(10)  # Aumentado para mejor separación
        
        # Título
        actions_title = QLabel("🛠️ HERRAMIENTAS")
        actions_title.setObjectName("actionsTitle")
        actions_title.setFont(QFont("Roboto", 11, QFont.Weight.Bold))
        actions_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        actions_title.setFixedHeight(25)  # Aumentado para mejor visibilidad
        actions_layout.addWidget(actions_title)
        
        # Contenedor para botones - REORGANIZADO
        buttons_container = QFrame()
        buttons_container.setObjectName("buttonsContainer")
        buttons_grid = QGridLayout(buttons_container)
        buttons_grid.setSpacing(6)  # Aumentado para mejor separación
        buttons_grid.setContentsMargins(3, 3, 3, 3)
        
        # Botones - REORGANIZADOS para mejor visibilidad
        self.create_folder_btn = QPushButton("📁\nCarpeta")
        self.create_folder_btn.setObjectName("compactActionButton")
        self.create_folder_btn.setFixedSize(95, 55)
        self.create_folder_btn.clicked.connect(self.create_folder)
        buttons_grid.addWidget(self.create_folder_btn, 0, 0)
        
        self.create_file_btn = QPushButton("📄\nArchivo")
        self.create_file_btn.setObjectName("compactActionButton")
        self.create_file_btn.setFixedSize(95, 55)
        self.create_file_btn.clicked.connect(self.create_file)
        buttons_grid.addWidget(self.create_file_btn, 0, 1)
        
        self.open_file_btn = QPushButton("📝\nAbrir")
        self.open_file_btn.setObjectName("compactActionButton")
        self.open_file_btn.setFixedSize(95, 55)
        self.open_file_btn.clicked.connect(self.open_selected_file)
        self.open_file_btn.setEnabled(False)
        buttons_grid.addWidget(self.open_file_btn, 1, 0)
        
        self.rename_btn = QPushButton("✏️\nRenombrar")
        self.rename_btn.setObjectName("compactActionButton")
        self.rename_btn.setFixedSize(95, 55)
        self.rename_btn.clicked.connect(self.rename_selected)
        self.rename_btn.setEnabled(False)
        buttons_grid.addWidget(self.rename_btn, 1, 1)
        
        self.delete_btn = QPushButton("🗑️\nEliminar")
        self.delete_btn.setObjectName("compactDeleteButton")
        self.delete_btn.setFixedSize(95, 55)
        self.delete_btn.clicked.connect(self.delete_selected)
        self.delete_btn.setEnabled(False)
        buttons_grid.addWidget(self.delete_btn, 2, 0)
        
        self.refresh_btn = QPushButton("🔄\nActualizar")
        self.refresh_btn.setObjectName("compactActionButton")
        self.refresh_btn.setFixedSize(95, 55)
        self.refresh_btn.clicked.connect(self.load_directory)
        buttons_grid.addWidget(self.refresh_btn, 2, 1)
        
        actions_layout.addWidget(buttons_container)
        
        splitter.addWidget(actions_frame)
        splitter.setSizes([600, 210])  # Ajustado para mejor proporción
        
        content_layout.addWidget(splitter)
        main_layout.addWidget(content_frame)
    
    def load_directory(self):
        """Cargar el contenido del directorio actual"""
        self.file_list.clear()
        
        # Mostrar ruta de forma más atractiva
        path_str = str(self.current_path)
        if len(path_str) > 50:
            # Si la ruta es muy larga, mostrar solo las últimas partes
            parts = self.current_path.parts
            if len(parts) > 3:
                short_path = ".../" + "/".join(parts[-2:])
            else:
                short_path = path_str
        else:
            short_path = path_str
            
        self.path_label.setText(short_path)
        
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
        
        # Emitir señal de que se abrió una carpeta
        self.folder_opened.emit(str(self.current_path))
    
    def on_item_double_clicked(self, item):
        """Manejar doble clic en un item"""
        if isinstance(item, FileExplorerItem):
            if item.is_directory:
                self.current_path = Path(item.file_path)
                self.load_directory()
            else:
                # Si es un archivo, intentar abrirlo
                self.open_file(item.file_path)
    
    def on_item_clicked(self, item):
        """Manejar clic simple en un item"""
        if isinstance(item, FileExplorerItem):
            # Habilitar botones de acción
            self.delete_btn.setEnabled(True)
            self.rename_btn.setEnabled(True)
            
            # Habilitar botón de abrir archivo si es un archivo
            if not item.is_directory:
                self.open_file_btn.setEnabled(True)
            else:
                self.open_file_btn.setEnabled(False)
            
            # Emitir señal de que se seleccionó un archivo
            self.file_selected.emit(item.file_path)
    
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
        self.open_file_btn.setEnabled(False)
    
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
    
    def open_selected_file(self):
        """Abrir el archivo seleccionado"""
        current_item = self.file_list.currentItem()
        if isinstance(current_item, FileExplorerItem) and not current_item.is_directory:
            self.open_file(current_item.file_path)
    
    def open_file(self, file_path):
        """Abrir un archivo con la aplicación predeterminada o editor de texto"""
        try:
            import subprocess
            
            # Intentar abrir con xdg-open (Linux)
            subprocess.run(['xdg-open', file_path], check=True)
        except subprocess.CalledProcessError:
            # Si falla, mostrar mensaje informativo
            QMessageBox.information(self, "Abrir archivo", 
                                  f"No se pudo abrir automáticamente el archivo:\n{file_path}\n\n"
                                  "Puedes abrirlo manualmente con tu aplicación preferida.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al abrir archivo: {str(e)}")
    
    def is_in_user_directory(self):
        """Verificar si estamos dentro del directorio del usuario"""
        try:
            self.current_path.relative_to(Path.home())
            return True
        except ValueError:
            return False
    
    def set_path(self, path):
        """Establecer la ruta actual del explorador"""
        new_path = Path(path)
        if new_path.exists() and new_path.is_dir():
            self.current_path = new_path
            self.load_directory()
            self.clear_selection()
        else:
            QMessageBox.warning(self, "Error", f"La ruta no existe o no es un directorio: {path}")
    
    def get_current_path(self):
        """Obtener la ruta actual"""
        return str(self.current_path)
    
    def get_selected_item_path(self):
        """Obtener la ruta del item seleccionado"""
        current_item = self.file_list.currentItem()
        if isinstance(current_item, FileExplorerItem):
            return current_item.file_path
        return None
    
    def apply_theme(self):
        """Aplicar tema al widget"""
        try:
            from styles.mode_styles import get_file_explorer_styles
            theme = self.theme_manager.get_theme(self.current_theme)
            explorer_styles = get_file_explorer_styles(theme)
            self.setStyleSheet(explorer_styles)
        except ImportError:
            # Fallback si no existe el estilo específico
            from styles.mode_styles import get_mode_styles
            theme = self.theme_manager.get_theme(self.current_theme)
            mode_styles = get_mode_styles(theme, "easy")
            self.setStyleSheet(mode_styles)
    
    def change_theme(self, theme_name):
        """Cambiar tema del widget"""
        self.current_theme = theme_name
        self.apply_theme()
    
    def position_window_at_top(self):
        """Posicionar la ventana en la parte superior de la pantalla"""
        # Si este widget está dentro de una ventana principal, posicionarla arriba
        if self.window() and hasattr(self.window(), 'move'):
            # Obtener el tamaño de la pantalla
            from PyQt6.QtGui import QGuiApplication
            screen = QGuiApplication.primaryScreen()
            if screen:
                screen_geometry = screen.availableGeometry()
                # Posicionar en la parte superior centrada horizontalmente
                x = (screen_geometry.width() - self.window().width()) // 2
                y = screen_geometry.y()  # Parte superior de la pantalla
                self.window().move(x, y)
