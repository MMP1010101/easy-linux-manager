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
        /* Estilos específicos para Easy Mode */
        QLabel#easyTitle {{
            color: {theme['accent']};
            font-size: 24px;
            font-weight: bold;
        }}
        
        QPushButton#easyActionButton {{
            background-color: {theme['accent']};
            color: {theme['bg']};
            border: none;
            border-radius: 12px;
            padding: 15px 25px;
            font-weight: bold;
            font-size: 14px;
        }}
        
        QPushButton#easyActionButton:hover {{
            background-color: {theme['fg']};
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
