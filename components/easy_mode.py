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
                           QSizePolicy, QLineEdit)
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
    """Widget para la sección Scripts - Permite ejecutar scripts de la carpeta scripts"""
    
    # Señal para actualizar el terminal con la salida del script
    script_output_ready = pyqtSignal(str, str)
    
    def __init__(self, theme_manager, current_theme, parent=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.current_theme = current_theme
        self.scripts_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
        self.setup_ui()
        self.load_scripts()
    
    def setup_ui(self):
        """Crear la interfaz de Scripts"""
        self.setObjectName("modeWidget")
        
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Título con estilo mejorado
        title_frame = QFrame()
        title_frame.setObjectName("titleFrame")
        title_layout = QVBoxLayout(title_frame)
        title_layout.setContentsMargins(20, 15, 20, 15)
        
        title = QLabel("📜 EJECUTOR DE SCRIPTS")
        title.setObjectName("easyTitle")
        title.setFont(QFont("Roboto", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(title)
        
        subtitle = QLabel("Selecciona y ejecuta los scripts disponibles en el sistema")
        subtitle.setObjectName("subtitle")
        subtitle.setFont(QFont("Roboto", 12, QFont.Weight.Normal))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(f"color: {self.theme_manager.get_theme(self.current_theme)['status_fg']}; margin-top: 5px;")
        title_layout.addWidget(subtitle)
        
        layout.addWidget(title_frame)
        
        # Contenedor principal dividido
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        content_splitter.setChildrenCollapsible(False)
        
        # Panel de lista de scripts
        scripts_panel = QFrame()
        scripts_panel.setObjectName("scriptsPanel")
        scripts_layout = QVBoxLayout(scripts_panel)
        scripts_layout.setContentsMargins(15, 15, 15, 15)
        
        # Título de la lista
        list_title = QLabel("🧩 Scripts Disponibles")
        list_title.setFont(QFont("Roboto", 14, QFont.Weight.Bold))
        list_title.setObjectName("sectionTitle")
        scripts_layout.addWidget(list_title)
        
        # Lista de scripts
        self.scripts_list = QListWidget()
        self.scripts_list.setObjectName("scriptsList")
        self.scripts_list.setFont(QFont("JetBrains Mono", 12))
        self.scripts_list.itemClicked.connect(self.on_script_selected)
        scripts_layout.addWidget(self.scripts_list)
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        self.refresh_button = QPushButton("🔄 Refrescar")
        self.refresh_button.setObjectName("actionButton")
        self.refresh_button.setFont(QFont("Roboto", 12, QFont.Weight.Bold))
        self.refresh_button.clicked.connect(self.load_scripts)
        buttons_layout.addWidget(self.refresh_button)
        
        self.execute_button = QPushButton("▶️ Ejecutar")
        self.execute_button.setObjectName("primaryButton")
        self.execute_button.setFont(QFont("Roboto", 12, QFont.Weight.Bold))
        self.execute_button.clicked.connect(self.execute_selected_script)
        self.execute_button.setEnabled(False)
        buttons_layout.addWidget(self.execute_button)
        
        scripts_layout.addLayout(buttons_layout)
        
        # Agregar panel de scripts al splitter
        content_splitter.addWidget(scripts_panel)
        
        # Panel de información y salida del script
        info_panel = QFrame()
        info_panel.setObjectName("infoPanel")
        info_layout = QVBoxLayout(info_panel)
        info_layout.setContentsMargins(15, 15, 15, 15)
        
        # Título del panel de información
        info_title = QLabel("📋 Información del Script")
        info_title.setFont(QFont("Roboto", 14, QFont.Weight.Bold))
        info_title.setObjectName("sectionTitle")
        info_layout.addWidget(info_title)
        
        # Información del script
        self.script_info = QLabel("Selecciona un script para ver su información.")
        self.script_info.setFont(QFont("JetBrains Mono", 12))
        self.script_info.setObjectName("scriptInfo")
        self.script_info.setWordWrap(True)
        info_layout.addWidget(self.script_info)
        
        # Título del panel de salida
        output_title = QLabel("📤 Salida del Script")
        output_title.setFont(QFont("Roboto", 14, QFont.Weight.Bold))
        output_title.setObjectName("sectionTitle")
        output_title.setContentsMargins(0, 15, 0, 0)
        info_layout.addWidget(output_title)
        
        # Salida del script
        self.output_area = QTextEdit()
        self.output_area.setObjectName("outputArea")
        self.output_area.setFont(QFont("JetBrains Mono", 12))
        self.output_area.setReadOnly(True)
        self.output_area.setMinimumHeight(200)
        info_layout.addWidget(self.output_area)
        
        # Agregar panel de información al splitter
        content_splitter.addWidget(info_panel)
        
        # Establecer tamaños relativos de los paneles (40% lista, 60% info)
        content_splitter.setSizes([400, 600])
        
        # Agregar splitter al layout principal
        layout.addWidget(content_splitter)
        
        # Aplicar estilos según el tema
        self.apply_theme()
    
    def apply_theme(self):
        """Aplicar estilos según el tema seleccionado"""
        theme = self.theme_manager.get_theme(self.current_theme)
        
        # Estilos para el panel de scripts
        self.setStyleSheet(f"""
            #modeWidget {{
                background-color: {theme['bg']};
                color: {theme['fg']};
            }}
            #titleFrame, #scriptsPanel, #infoPanel {{
                background-color: {theme['terminal_bg']};
                color: {theme['fg']};
                border-radius: 10px;
                border: 1px solid {theme['border_color']};
            }}
            #easyTitle {{
                color: {theme['accent']};
            }}
            #scriptsList {{
                background-color: {theme['terminal_bg']};
                color: {theme['fg']};
                border-radius: 5px;
                padding: 10px;
                border: 1px solid {theme['border_color']};
            }}
            #scriptsList::item {{
                padding: 8px;
                border-bottom: 1px solid {theme['border_color']};
            }}
            #scriptsList::item:selected {{
                background-color: {theme['selection_bg']};
                color: {theme['text']};
            }}
            #outputArea {{
                background-color: {theme['terminal_bg']};
                color: {theme['fg']};
                border-radius: 5px;
                padding: 10px;
                border: 1px solid {theme['border_color']};
            }}
            #actionButton, #primaryButton {{
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }}
            #actionButton {{
                background-color: {theme['button_bg']};
                color: {theme['button_fg']};
                border: 1px solid {theme['border_color']};
            }}
            #actionButton:hover {{
                background-color: {theme['button_grad_2']};
            }}
            #primaryButton {{
                background-color: {theme['accent']};
                color: {theme['button_fg']};
            }}
            #primaryButton:hover {{
                background-color: {theme['button_grad_1']};
            }}
            #primaryButton:disabled {{
                background-color: #555555;
                color: #aaaaaa;
            }}
        """)
    
    def load_scripts(self):
        """Cargar la lista de scripts disponibles"""
        # Limpiar lista
        self.scripts_list.clear()
        self.output_area.clear()
        self.script_info.setText("Selecciona un script para ver su información.")
        self.execute_button.setEnabled(False)
        
        # Verificar si el directorio existe
        if not os.path.exists(self.scripts_path):
            try:
                os.makedirs(self.scripts_path)
                self.scripts_list.addItem("¡No hay scripts disponibles!")
                return
            except Exception as e:
                self.scripts_list.addItem(f"Error: No se pudo crear el directorio de scripts: {e}")
                return
        
        # Listar scripts
        try:
            scripts = [f for f in os.listdir(self.scripts_path) if os.path.isfile(os.path.join(self.scripts_path, f)) and f.endswith(".sh")]
            
            if not scripts:
                self.scripts_list.addItem("¡No hay scripts disponibles!")
                return
            
            # Agregar scripts a la lista
            for script in sorted(scripts):
                item = QListWidgetItem(f"📜 {script}")
                item.script_path = os.path.join(self.scripts_path, script)
                self.scripts_list.addItem(item)
            
        except Exception as e:
            self.scripts_list.addItem(f"Error: {str(e)}")
    
    def on_script_selected(self, item):
        """Cuando se selecciona un script de la lista"""
        if hasattr(item, 'script_path') and os.path.exists(item.script_path):
            # Mostrar información del script
            try:
                script_name = os.path.basename(item.script_path)
                script_size = os.path.getsize(item.script_path)
                script_size_str = self._format_size(script_size)
                
                # Leer las primeras líneas del script para mostrar descripción
                with open(item.script_path, 'r') as f:
                    lines = [line.strip() for line in f.readlines()[:10]]
                
                # Buscar descripción o comentarios en las primeras líneas
                description = "Sin descripción disponible"
                for line in lines:
                    if line.startswith('#') and len(line) > 2:
                        description = line[1:].strip()
                        break
                
                info_text = f"""<b>Nombre:</b> {script_name}
<b>Ruta:</b> {item.script_path}
<b>Tamaño:</b> {script_size_str}
<b>Descripción:</b> {description}

<i>Haz clic en 'Ejecutar' para iniciar este script.</i>"""
                
                self.script_info.setText(info_text)
                self.execute_button.setEnabled(True)
            except Exception as e:
                self.script_info.setText(f"Error al leer información del script: {str(e)}")
                self.execute_button.setEnabled(False)
        else:
            self.script_info.setText("Información no disponible para este elemento.")
            self.execute_button.setEnabled(False)
    
    def _format_size(self, size):
        """Formatear tamaño de archivo para mostrar"""
        if size < 1024:
            return f"{size} bytes"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.1f} MB"
    
    def execute_selected_script(self):
        """Ejecutar el script seleccionado"""
        selected_items = self.scripts_list.selectedItems()
        if not selected_items:
            return
        
        item = selected_items[0]
        if not hasattr(item, 'script_path'):
            return
        
        script_path = item.script_path
        if not os.path.exists(script_path):
            self.output_area.setText("Error: El script seleccionado no existe.")
            return
        
        # Verificar permisos de ejecución
        if not os.access(script_path, os.X_OK):
            try:
                # Intenta dar permisos de ejecución
                os.chmod(script_path, os.stat(script_path).st_mode | 0o111)
                self.output_area.append("Se han dado permisos de ejecución al script.\n")
            except Exception as e:
                self.output_area.setText(f"Error: No se pueden establecer permisos de ejecución: {str(e)}")
                return
        
        # Verificar si el script usa sudo (comprobando el contenido)
        requires_sudo = False
        try:
            with open(script_path, 'r') as f:
                content = f.read()
                if 'sudo ' in content:
                    requires_sudo = True
        except:
            pass
        
        # Si requiere sudo, solicitar contraseña
        if requires_sudo:
            password, ok = QInputDialog.getText(
                self, 
                "Contraseña requerida", 
                "Este script requiere permisos de superusuario.\nIngresa tu contraseña:",
                QLineEdit.EchoMode.Password
            )
            
            if not ok or not password:
                self.output_area.setText("Ejecución cancelada: Se requiere contraseña para ejecutar este script.")
                return
            
            # Crear un script temporal para enviar la contraseña a sudo
            self.output_area.clear()
            self.output_area.append(f"⏳ Ejecutando: {os.path.basename(script_path)} con permisos de superusuario...\n")
            
            # Crear y ejecutar el runner con contraseña
            from core.command_runner import CommandRunner
            # Ejecutar con echo y pipe para enviar la contraseña
            self.runner = CommandRunner(f"echo '{password}' | sudo -S {script_path}")
            self.runner.output_ready.connect(self.handle_script_output)
            self.runner.finished_execution.connect(self.handle_script_finished)
            self.runner.start()
        else:
            # Limpiar área de salida
            self.output_area.clear()
            self.output_area.append(f"⏳ Ejecutando: {os.path.basename(script_path)}...\n")
            
            # Crear y ejecutar el runner
            from core.command_runner import CommandRunner
            self.runner = CommandRunner(script_path)
            self.runner.output_ready.connect(self.handle_script_output)
            self.runner.finished_execution.connect(self.handle_script_finished)
            self.runner.start()
    
    def handle_script_output(self, text, output_type):
        """Manejar la salida del script en ejecución"""
        if output_type == "error":
            self.output_area.append(f"<span style='color:red;'>{text}</span>")
        elif output_type == "success":
            self.output_area.append(f"<span style='color:#00cc00;'>{text}</span>")
        else:
            self.output_area.append(text)
        
        # Auto-scroll
        cursor = self.output_area.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.output_area.setTextCursor(cursor)
    
    def handle_script_finished(self):
        """Cuando el script termina de ejecutarse"""
        self.output_area.append("\n✅ Ejecución completada.")


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
