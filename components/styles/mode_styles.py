"""
Estilos CSS para diferentes modos (Easy, Dependencies, etc.)
"""


def get_mode_styles(theme, mode_name="default"):
    """Generar estilos CSS para diferentes modos"""
    base_styles = f"""
    /* Estilos base para modos */
    QWidget#modeWidget {{
        background-color: {theme['bg']};
        color: {theme['text']};
    }}
    
    /* Títulos de los modos */
    QLabel#modeTitle {{
        color: {theme['text']};
        font-size: 18px;
        font-weight: bold;
        background-color: transparent;
        padding: 20px;
    }}
    
    /* Información de los modos */
    QLabel#modeInfo {{
        color: {theme['status_fg']};
        font-size: 14px;
        background-color: transparent;
        padding: 10px;
    }}
    
    /* Botones específicos de modo */
    QPushButton#modeButton {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                   stop:0 {theme['button_grad_1']},
                                   stop:1 {theme['button_grad_3']});
        color: {theme['button_fg']};
        border: none;
        border-radius: 8px;
        padding: 12px 20px;
        font-weight: bold;
        font-size: 12px;
        margin: 5px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    
    QPushButton#modeButton:hover {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                  stop:0 {theme['hover_grad_1']},
                                  stop:1 {theme['hover_grad_3']});
        border: 1px solid rgba(255, 255, 255, 0.3);
    }}
    
    QPushButton#modeButton:pressed {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                  stop:0 {theme['pressed_grad_1']},
                                  stop:1 {theme['pressed_grad_2']});
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    
    /* Contenedores de modo */
    QWidget#modeContainer {{
        background-color: {theme['bg']};
        border: 1px solid {theme['border_color']};
        border-radius: 10px;
        padding: 15px;
        margin: 10px;
    }}
    """
    
    # Estilos específicos por modo
    if mode_name == "easy":
        mode_specific = f"""
        /* Estilos específicos para Easy Mode - Explorador de Archivos Moderno */
        QLabel#easyTitle {{
            color: {theme['accent']};
            font-size: 28px;
            font-weight: bold;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                       stop:0 transparent,
                                       stop:0.5 {theme['accent']},
                                       stop:1 transparent);
            padding: 20px;
            border-radius: 15px;
            margin: 10px;
            text-align: center;
        }}
        
        /* Marco de navegación moderno */
        QFrame#navFrame {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                       stop:0 {theme['button_bg']},
                                       stop:1 {theme['terminal_bg']});
            border: 2px solid {theme['accent']};
            border-radius: 15px;
            padding: 15px;
            margin: 5px;
        }}
        
        /* Etiqueta de ruta mejorada con CONTRASTE EXTREMO */
        QLabel#pathLabel {{
            color: #FFFFFF;  /* Blanco puro para máximo contraste */
            background-color: transparent;  
            padding: 10px 15px;
            font-family: "JetBrains Mono", monospace;
            font-weight: bold;
            font-size: 16px;  /* Tamaño aumentado para mejor visibilidad */
            letter-spacing: 1.2px;  /* Mejor separación entre caracteres */
        }}
        
        /* Contenedor de ruta con CONTRASTE MÁXIMO */
        QFrame#pathContainer {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                       stop:0 #FF0000,
                                       stop:0.05 #000000,
                                       stop:1 {theme['bg']});
            border: 3px solid #FF0000;  /* Borde rojo brillante */
            border-radius: 12px;
            padding: 5px;
            margin: 5px 15px;
            min-height: 60px;  /* Altura aumentada */
        }}
        
        /* Lista de archivos - Solo estilos de contenedor, los items se manejan internamente */
        QListWidget#fileList {{
            background: transparent;
            border: none;
            outline: none;
        }}
        
        /* Botones de navegación del explorador */
        QPushButton#navButton {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                       stop:0 {theme['button_bg']},
                                       stop:1 {theme['button_grad_2']});
            color: {theme['button_fg']};
            border: 1px solid {theme['border_color']};
            border-radius: 8px;
            padding: 10px 15px;
            font-weight: bold;
            font-size: 12px;
            margin: 2px;
            min-width: 80px;
        }}
        
        QPushButton#navButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                       stop:0 {theme['hover_grad_1']},
                                       stop:1 {theme['hover_grad_2']});
            border: 1px solid {theme['accent']};
            color: {theme['text']};
        }}
        
        QPushButton#navButton:pressed {{
            background: {theme['accent']};
            color: white;
        }}
        
        /* Panel de acciones futurista */
        QFrame#actionsFrame {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                       stop:0 {theme['bg']},
                                       stop:0.3 {theme['terminal_bg']},
                                       stop:1 {theme['bg']});
            border: 3px solid {theme['accent']};
            border-radius: 20px;
            padding: 20px;
            margin: 5px;
        }}
        
        QLabel#actionsTitle {{
            color: {theme['accent']};
            font-size: 18px;
            font-weight: bold;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                       stop:0 transparent,
                                       stop:0.5 {theme['accent']},
                                       stop:1 transparent);
            padding: 12px;
            border-radius: 10px;
            margin-bottom: 15px;
            text-align: center;
        }}
        
        /* Área de información con estilo */
        QTextEdit#itemInfo {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                       stop:0 {theme['terminal_bg']},
                                       stop:1 {theme['bg']});
            color: {theme['text']};
            border: 2px solid {theme['border_color']};
            border-radius: 10px;
            padding: 12px;
            font-size: 11px;
            font-family: "JetBrains Mono", monospace;
        }}
        
        /* Botones de acción con efectos */
        QPushButton#easyActionButton {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                       stop:0 {theme['accent']},
                                       stop:0.5 {theme['fg']},
                                       stop:1 {theme['accent']});
            color: {theme['bg']};
            border: 2px solid {theme['fg']};
            border-radius: 12px;
            padding: 15px 25px;
            font-weight: bold;
            font-size: 13px;
            margin: 8px 5px;
        }}
        
        QPushButton#easyActionButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                       stop:0 {theme['fg']},
                                       stop:0.5 #ffffff,
                                       stop:1 {theme['fg']});
            border: 2px solid {theme['accent']};
            color: {theme['bg']};
        }}
        
        QPushButton#easyActionButton:pressed {{
            background: {theme['selection_bg']};
            border: 2px solid {theme['text']};
        }}
        
        /* Botón de eliminar llamativo */
        QPushButton#deleteButton {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                       stop:0 #ff4757,
                                       stop:0.5 #ff6b7a,
                                       stop:1 #ff4757);
            color: white;
            border: 2px solid #c44569;
            border-radius: 12px;
            padding: 15px 25px;
            font-weight: bold;
            font-size: 13px;
            margin: 8px 5px;
        }}
        
        QPushButton#deleteButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                       stop:0 #ff6b7a,
                                       stop:0.5 #ffffff,
                                       stop:1 #ff6b7a);
            border: 2px solid #ff4757;
        }}
        
        QPushButton#deleteButton:pressed {{
            background: #c44569;
            border: 2px solid #a0325a;
        }}
        
        QPushButton#deleteButton:disabled {{
            background: {theme['border_color']};
            color: {theme['status_fg']};
            border: 1px solid {theme['status_fg']};
        }}
        
        /* Texto de ayuda con estilo */
        QLabel#helpText {{
            color: {theme['text']};
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                       stop:0 {theme['terminal_bg']},
                                       stop:1 {theme['bg']});
            font-size: 11px;
            padding: 15px;
            border: 2px solid {theme['border_color']};
            border-radius: 12px;
            margin: 10px 0px;
            font-weight: 500;
        }}
        
        /* Estilos adicionales para la interfaz mejorada */
        QFrame#titleFrame {{
            background: qradialgradient(cx:0.5, cy:0.5, fx:0.5, fy:0.5,
                                       radius: 1.2,
                                       stop:0 {theme['accent']},
                                       stop:1 {theme['bg']});
            border: 2px solid {theme['fg']};
            border-radius: 20px;
            margin: 10px;
        }}
        
        QLabel#subtitle {{
            color: {theme['status_fg']};
            font-style: italic;
            background-color: transparent;
        }}
        
        QFrame#contentFrame {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                       stop:0 {theme['bg']},
                                       stop:1 {theme['terminal_bg']});
            border: 1px solid {theme['border_color']};
            border-radius: 15px;
            padding: 10px;
        }}
        
        QFrame#filesContainer {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                       stop:0 {theme['terminal_bg']},
                                       stop:1 {theme['bg']});
            border: 2px solid {theme['accent']};
            border-radius: 15px;
            padding: 10px;
        }}
        
        QLabel#sectionTitle {{
            color: {theme['fg']};
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                       stop:0 transparent,
                                       stop:0.5 {theme['accent']},
                                       stop:1 transparent);
            padding: 8px;
            border-radius: 8px;
            margin-bottom: 10px;
        }}
        
        QLabel#infoLabel, QLabel#actionsLabel, QLabel#helpTitle {{
            color: {theme['accent']};
            background-color: transparent;
            font-weight: bold;
            padding: 5px 0px;
        }}
        """
    
    elif mode_name == "dependencies":
        mode_specific = f"""
        /* Estilos específicos para Dependencies Mode */
        QLabel#depsTitle {{
            color: {theme['fg']};
            font-size: 24px;
            font-weight: bold;
        }}
        
        QPushButton#installButton {{
            background-color: {theme['fg']};
            color: {theme['bg']};
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: bold;
        }}
        
        QPushButton#installButton:hover {{
            background-color: {theme['accent']};
        }}
        
        /* Lista de dependencias */
        QListWidget {{
            background-color: {theme['terminal_bg']};
            color: {theme['text']};
            border: 2px solid {theme['border_color']};
            border-radius: 5px;
            padding: 5px;
        }}
        
        QListWidget::item {{
            padding: 8px;
            border-bottom: 1px solid {theme['border_color']};
        }}
        
        QListWidget::item:selected {{
            background-color: {theme['selection_bg']};
        }}
        
        QListWidget::item:hover {{
            background-color: {theme['accent']};
            color: {theme['bg']};
        }}
        """
    
    else:
        mode_specific = ""
    
    return base_styles + mode_specific


def get_form_styles(theme):
    """Estilos para formularios y controles de entrada"""
    return f"""
    /* Campos de entrada */
    QLineEdit {{
        background-color: {theme['terminal_bg']};
        color: {theme['text']};
        border: 2px solid {theme['border_color']};
        border-radius: 5px;
        padding: 8px;
        font-size: 12px;
    }}
    
    QLineEdit:focus {{
        border-color: {theme['accent']};
    }}
    
    /* Áreas de texto */
    QTextEdit {{
        background-color: {theme['terminal_bg']};
        color: {theme['text']};
        border: 2px solid {theme['border_color']};
        border-radius: 5px;
        padding: 8px;
        font-size: 12px;
    }}
    
    /* Checkboxes */
    QCheckBox {{
        color: {theme['text']};
        spacing: 8px;
    }}
    
    QCheckBox::indicator {{
        width: 16px;
        height: 16px;
        border: 2px solid {theme['border_color']};
        border-radius: 3px;
        background-color: {theme['terminal_bg']};
    }}
    
    QCheckBox::indicator:checked {{
        background-color: {theme['accent']};
        border-color: {theme['accent']};
    }}
    
    /* Radio buttons */
    QRadioButton {{
        color: {theme['text']};
        spacing: 8px;
    }}
    
    QRadioButton::indicator {{
        width: 16px;
        height: 16px;
        border: 2px solid {theme['border_color']};
        border-radius: 8px;
        background-color: {theme['terminal_bg']};
    }}
    
    QRadioButton::indicator:checked {{
        background-color: {theme['accent']};
        border-color: {theme['accent']};
    }}
    
    /* Progress bars */
    QProgressBar {{
        background-color: {theme['terminal_bg']};
        border: 2px solid {theme['border_color']};
        border-radius: 5px;
        text-align: center;
        color: {theme['text']};
    }}
    
    QProgressBar::chunk {{
        background-color: {theme['accent']};
        border-radius: 3px;
    }}
    """


def get_file_explorer_styles(theme):
    """Generar estilos específicos para el explorador de archivos"""
    
    # Estilos básicos del widget y título
    basic_styles = f"""
    /* Estilos básicos del explorador */
    QWidget#fileExplorerWidget {{
        background-color: {theme['bg']};
        color: {theme['text']};
    }}
    
    /* Título del explorador */
    QLabel#explorerTitle {{
        color: {theme['accent']};
        font-size: 24px;
        font-weight: bold;
        padding: 15px;
        border-radius: 12px;
    }}
    
    QLabel#explorerSubtitle {{
        color: {theme['status_fg']};
        font-size: 12px;
        background-color: transparent;
        padding: 5px;
        text-align: center;
    }}
    """
    
    # Frames y contenedores
    frame_styles = f"""
    /* Frames y contenedores */
    QFrame#titleFrame {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                   stop:0 {theme['button_grad_1']},
                                   stop:1 {theme['terminal_bg']});
        border: 2px solid {theme['accent']};
        border-radius: 15px;
        margin: 5px;
    }}
    
    QFrame#navFrame {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                   stop:0 {theme['button_grad_1']},
                                   stop:1 {theme['terminal_bg']});
        border: 2px solid {theme['accent']};
        border-radius: 15px;
        padding: 10px;
        margin: 5px;
    }}
    
    QFrame#pathContainer {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                   stop:0 {theme['terminal_bg']},
                                   stop:1 {theme['bg']});
        border: 1px solid {theme['accent']};
        border-radius: 12px;
        padding: 8px;
    }}
    
    QLabel#pathLabel {{
        color: {theme['accent']};
        font-family: "JetBrains Mono", monospace;
        font-weight: bold;
        font-size: 12px;
        background-color: transparent;
    }}
    
    QFrame#filesContainer {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                   stop:0 {theme['bg']},
                                   stop:1 {theme['terminal_bg']});
        border: 2px solid {theme['accent']};
        border-radius: 15px;
        padding: 15px;
    }}
    
    QFrame#actionsFrame {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                   stop:0 {theme['bg']},
                                   stop:1 {theme['button_bg']});
        border: 2px solid {theme['accent']};
        border-radius: 15px;
        padding: 20px;
    }}
    """
    
    # Navegación y botones
    button_styles = f"""
    /* Botones de navegación */
    QPushButton#navButton {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                   stop:0 {theme['button_grad_1']},
                                   stop:1 {theme['button_grad_3']});
        color: {theme['button_fg']};
        border: none;
        border-radius: 10px;
        padding: 12px 18px;
        font-weight: bold;
        font-size: 13px;
        min-width: 100px;
    }}
    
    QPushButton#navButton:hover {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                   stop:0 {theme['hover_grad_1']},
                                   stop:1 {theme['hover_grad_3']});
        border: 1px solid {theme['accent']};
    }}
    
    QPushButton#navButton:pressed {{
        background: {theme['accent']};
        color: white;
    }}
    
    /* Botones de acción */
    QPushButton#explorerActionButton {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                   stop:0 {theme['button_grad_1']},
                                   stop:1 {theme['button_grad_3']});
        color: white;
        border: none;
        border-radius: 12px;
        padding: 15px 20px;
        font-weight: bold;
        font-size: 13px;
        min-height: 25px;
        margin: 5px 0;
    }}
    
    QPushButton#explorerActionButton:hover {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                   stop:0 {theme['hover_grad_1']},
                                   stop:1 {theme['hover_grad_3']});
        border: 1px solid white;
    }}
    
    QPushButton#explorerActionButton:pressed {{
        background: {theme['accent']};
    }}
    
    QPushButton#explorerActionButton:disabled {{
        background: {theme['terminal_bg']};
        color: {theme['border_color']};
    }}
    
    /* Botón eliminar */
    QPushButton#deleteButton {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                   stop:0 #ff4757,
                                   stop:1 #ff6b81);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 15px 20px;
        font-weight: bold;
        font-size: 13px;
        min-height: 25px;
        margin: 5px 0;
    }}
    
    QPushButton#deleteButton:hover {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                   stop:0 #ff6b81,
                                   stop:1 #ff4757);
        border: 1px solid white;
    }}
    
    QPushButton#deleteButton:pressed {{
        background: #ff4757;
    }}
    
    QPushButton#deleteButton:disabled {{
        background: {theme['terminal_bg']};
        color: {theme['border_color']};
    }}
    """
    
    # Lista de archivos
    file_list_styles = f"""
    /* Lista de archivos */
    QListWidget#fileList {{
        background-color: {theme['terminal_bg']};
        border: 2px solid {theme['accent']};
        border-radius: 10px;
        padding: 15px;
        outline: none;
    }}
    
    QListWidget#fileList::item {{
        height: 45px;
        padding: 10px 15px;
        margin: 8px 2px;
        border: 2px solid {theme['border_color']};
        border-radius: 8px;
        background-color: {theme['bg']};
        color: {theme['text']};
        font-size: 14px;
        font-weight: bold;
    }}
    
    /* Estilos específicos para carpetas */
    QListWidget#fileList::item[type="folder"] {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                  stop:0 {theme['bg']},
                                  stop:1 {theme['button_grad_1']});
        border: 2px solid {theme['accent']};
        color: {theme['accent']};
        font-weight: bold;
    }}
    
    QListWidget#fileList::item[type="folder"]:hover {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                  stop:0 {theme['selection_bg']},
                                  stop:1 {theme['button_grad_2']});
        border-color: {theme['fg']};
    }}
    
    QListWidget#fileList::item[type="folder"]:selected {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                  stop:0 {theme['accent']},
                                  stop:1 {theme['fg']});
        color: white;
    }}
    
    QListWidget#fileList::item:hover {{
        background-color: {theme['selection_bg']};
        border-color: {theme['accent']};
    }}
    
    QListWidget#fileList::item:selected {{
        background-color: {theme['accent']};
        border-color: {theme['fg']};
        color: white;
    }}
    """
    
    # Elementos de información y títulos
    info_styles = f"""
    /* Área de información y títulos */
    QTextEdit#itemInfo {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                   stop:0 {theme['terminal_bg']},
                                   stop:1 {theme['bg']});
        color: {theme['text']};
        border: 2px solid {theme['accent']};
        border-radius: 10px;
        padding: 12px;
        font-family: "JetBrains Mono", monospace;
        font-size: 12px;
        font-weight: bold;
    }}
    
    /* Títulos de sección */
    QLabel#sectionTitle, QLabel#infoLabel, QLabel#actionsLabel, QLabel#helpTitle {{
        color: {theme['accent']};
        font-size: 14px;
        font-weight: bold;
        padding: 5px 0;
        margin: 5px 0;
    }}
    
    QLabel#actionsTitle {{
        color: white;
        background: {theme['accent']};
        font-size: 16px;
        font-weight: bold;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
    }}
    
    /* Texto de ayuda */
    QLabel#helpText {{
        color: {theme['text']};
        background: {theme['terminal_bg']};
        border: 1px solid {theme['border_color']};
        border-radius: 8px;
        padding: 12px;
        font-size: 12px;
    }}
    """
    
    # Combinar todos los estilos
    return basic_styles + frame_styles + button_styles + file_list_styles + info_styles