"""
Estilos CSS para el menú principal
"""


def get_menu_styles(theme):
    """Generar estilos CSS para el menú principal"""
    return f"""
    /* Estilo principal para la página del menú */
    QWidget#menuPageWidget {{
        background-color: {theme['bg']};
        border: none;
    }}
    
    /* Estilo para el área de botones */
    QWidget#buttonsArea {{
        background-color: {theme['bg']};
        border: none;
    }}
    
    /* Estilos para botones del menú principal */
    QPushButton#menuButton {{
        background-color: {theme['button_bg']} !important;
        color: white !important;
        border: 2px solid {theme['accent']} !important;
        border-radius: 20px;
        text-align: left;
        padding-left: 25px;
        font-size: 18px;
        font-weight: bold;
        min-height: 90px;
        max-width: 450px;
    }}
    
    QPushButton#menuButton:hover {{
        background-color: {theme['accent']} !important;
        padding-left: 35px;
        border: 2px solid {theme['fg']} !important;
    }}
    
    QPushButton#menuButton:pressed {{
        background-color: {theme['selection_bg']} !important;
        padding-left: 25px;
    }}
    
    /* Estilo para el área del logo */
    QLabel#logoLabel {{
        background-color: transparent;
        border: none;
        padding: 0px;
        margin: 0px;
        border-radius: 15px;
        box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.1);
    }}
    
    /* Títulos del menú */
    QLabel#menuTitle {{
        color: {theme['text']};
        font-size: 24px;
        font-weight: bold;
        background-color: transparent;
        padding: 10px 0px;
        border-bottom: 2px solid {theme['accent']};
        margin-bottom: 20px;
        letter-spacing: 1px;
    }}
    
    /* Área de botones del menú */
    QWidget#buttonsArea {{
        background-color: {theme['bg']};
        border: none;
        border-radius: 20px;
        padding: 15px;
    }}
    
    /* Botón de regreso */
    QPushButton#backButton {{
        background: qradialgradient(cx:0.5, cy:0.5, fx:0.5, fy:0.5,
                                    radius: 1, stop:0 {theme['button_bg']}, stop:1 {theme['accent']});
        color: {theme['button_fg']};
        border: none;
        border-radius: 12px;
        padding: 12px 20px;
        font-weight: bold;
        font-size: 16px;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.2);
        transition: all 0.2s ease;
    }}
    
    QPushButton#backButton:hover {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {theme['accent']}, stop:1 #8B66E5);
        box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.2);
        transform: translateY(-2px) scale(1.02);
    }}
    
    QPushButton#backButton:pressed {{
        background: {theme['selection_bg']};
        box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
        transform: translateY(1px);
    }}
    """


def get_general_menu_styles(theme):
    """Estilos generales para elementos del menú"""
    return f"""
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
    
    QComboBox {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {theme['button_bg']}, stop:1 {theme['selection_bg']});
        color: {theme['button_fg']};
        border: 2px solid {theme['border_color']};
        border-radius: 10px;
        padding: 8px 15px;
        min-height: 25px;
        font-weight: 500;
        selection-background-color: {theme['accent']};
        box-shadow: 0px 3px 8px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
    }}
    
    QComboBox:hover {{
        border-color: {theme['accent']};
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {theme['button_bg']}, stop:1 {theme['accent']});
        box-shadow: 0px 5px 12px rgba(0, 0, 0, 0.15);
    }}
    
    QComboBox::drop-down {{
        border: none;
        width: 30px;
    }}
    
    QComboBox::down-arrow {{
        image: url(:/icons/arrow_down.png);
        width: 12px;
        height: 12px;
        margin-right: 15px;
    }}
    
    QComboBox QAbstractItemView {{
        background-color: {theme['bg']};
        border: 2px solid {theme['border_color']};
        border-radius: 8px;
        selection-background-color: {theme['accent']};
        selection-color: white;
        outline: none;
        padding: 5px;
    }}
    
    /* Scrollbar personalizado */
    QScrollBar:vertical {{
        border: none;
        background: {theme['bg']};
        width: 10px;
        margin: 0px;
        border-radius: 5px;
    }}

    QScrollBar::handle:vertical {{
        background: {theme['accent']};
        min-height: 30px;
        border-radius: 5px;
    }}

    QScrollBar::handle:vertical:hover {{
        background: #8B66E5;
    }}

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    QScrollBar:horizontal {{
        border: none;
        background: {theme['bg']};
        height: 10px;
        margin: 0px;
        border-radius: 5px;
    }}

    QScrollBar::handle:horizontal {{
        background: {theme['accent']};
        min-width: 30px;
        border-radius: 5px;
    }}

    QScrollBar::handle:horizontal:hover {{
        background: #8B66E5;
    }}

    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}
    
    /* Estilos para tooltips */
    QToolTip {{
        background-color: #333;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 5px;
        opacity: 200;
        font-weight: bold;
    }}
    
    /* Estilo para mensajes de estado */
    QStatusBar {{
        background-color: {theme['bg']};
        color: {theme['text']};
        border-top: 1px solid {theme['border_color']};
    }}
"""
