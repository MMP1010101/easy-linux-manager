"""
Estilos CSS para el terminal
"""


def get_terminal_styles(theme):
    """Generar estilos CSS para el terminal"""
    return f"""
    /* Contenedor principal del terminal */
    QWidget#terminalWidget {{
        background-color: {theme['bg']};
        color: {theme['text']};
    }}
    
    /* Área de salida del terminal */
    QTextEdit#terminalOutput {{
        background-color: {theme['terminal_bg']};
        color: {theme['terminal_fg']};
        border: 2px solid {theme['border_color']};
        border-radius: 5px;
        padding: 10px;
        font-family: "JetBrains Mono", "Consolas", "Monaco", monospace;
        font-size: 11px;
        line-height: 1.2;
        selection-background-color: {theme['selection_bg']};
    }}
    
    /* Campo de entrada de comandos */
    QLineEdit#commandInput {{
        background-color: {theme['terminal_bg']};
        color: {theme['text']};
        border: 2px solid {theme['border_color']};
        border-radius: 5px;
        padding: 8px;
        font-family: "JetBrains Mono", "Consolas", "Monaco", monospace;
        font-size: 11px;
    }}
    
    QLineEdit#commandInput:focus {{
        border-color: {theme['accent']};
        background-color: {theme['terminal_bg']};
    }}
    
    /* Botón ejecutar */
    QPushButton#executeButton {{
        background-color: {theme['button_bg']};
        color: {theme['button_fg']};
        border: none;
        border-radius: 5px;
        padding: 8px 16px;
        font-weight: bold;
        font-size: 12px;
    }}
    
    QPushButton#executeButton:hover {{
        background-color: {theme['accent']};
    }}
    
    QPushButton#executeButton:pressed {{
        background-color: {theme['selection_bg']};
    }}
    
    QPushButton#executeButton:disabled {{
        background-color: {theme['border_color']};
        color: {theme['status_fg']};
    }}
    
    /* Botones de comandos rápidos */
    QPushButton#quickButton {{
        background-color: {theme['button_bg']};
        color: {theme['button_fg']};
        border: none;
        border-radius: 5px;
        padding: 8px 12px;
        font-weight: bold;
        font-size: 10px;
        min-height: 35px;
    }}
    
    QPushButton#quickButton:hover {{
        background-color: {theme['accent']};
    }}
    
    QPushButton#quickButton:pressed {{
        background-color: {theme['selection_bg']};
    }}
    
    /* Marco del terminal */
    QFrame#terminalFrame {{
        border: 2px solid {theme['border_color']};
        border-radius: 5px;
        background-color: {theme['terminal_bg']};
    }}
    
    /* Separador horizontal */
    QFrame[frameShape="4"] {{
        background-color: {theme['accent']};
        border: none;
        max-height: 2px;
    }}
    
    /* Etiqueta del prompt */
    QLabel#promptLabel {{
        color: {theme['accent']};
        background-color: transparent;
        font-family: "JetBrains Mono", "Consolas", "Monaco", monospace;
        font-size: 11px;
        font-weight: bold;
    }}
    
    /* Título del terminal */
    QLabel#terminalTitle {{
        color: {theme['text']};
        font-size: 14px;
        font-weight: bold;
        background-color: transparent;
    }}
    
    /* Barra de estado */
    QLabel#statusLabel {{
        color: {theme['status_fg']};
        background-color: transparent;
        font-size: 9px;
    }}
    
    /* Indicador de proceso */
    QLabel#processIndicator {{
        color: {theme['accent']};
        background-color: transparent;
        font-size: 10px;
        font-weight: bold;
    }}
    """


def get_terminal_text_colors(theme):
    """Obtener colores para diferentes tipos de texto en el terminal"""
    return {
        'normal': theme['terminal_fg'],
        'error': theme['error_fg'],
        'success': theme['accent'],
        'command': theme['fg'],
        'status': theme['status_fg']
    }
