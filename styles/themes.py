#!/usr/bin/env python3
"""
Temas y estilos para la aplicación Linux GUI
Contiene las definiciones de colores y estilos para diferentes modos
"""


class ThemeManager:
    """Manejador de temas para la aplicación"""
    
    def __init__(self):
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
                "border_color": "#30363d",
                # Nuevos colores para gradientes de botones
                "button_grad_1": "#1D976C",
                "button_grad_2": "#2EB62C", 
                "button_grad_3": "#238636",
                "button_grad_4": "#13663E",
                "hover_grad_1": "#2EB62C",
                "hover_grad_2": "#3DDC5F",
                "hover_grad_3": "#1D976C",
                "pressed_grad_1": "#13663E",
                "pressed_grad_2": "#238636"
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
                "border_color": "#00aa00",
                # Nuevos colores para gradientes de botones
                "button_grad_1": "#003300",
                "button_grad_2": "#008800",
                "button_grad_3": "#00AA00", 
                "button_grad_4": "#00DD00",
                "hover_grad_1": "#00BB00",
                "hover_grad_2": "#00FF00",
                "hover_grad_3": "#00AA00",
                "pressed_grad_1": "#003300",
                "pressed_grad_2": "#008800"
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
                "border_color": "#414868",
                # Nuevos colores para gradientes de botones
                "button_grad_1": "#7f5af0",
                "button_grad_2": "#6865f3", 
                "button_grad_3": "#5065f5",
                "button_grad_4": "#3b82f6",
                "hover_grad_1": "#9580ff",
                "hover_grad_2": "#7f5af0",
                "hover_grad_3": "#5065f5",
                "pressed_grad_1": "#6865f3",
                "pressed_grad_2": "#3b82f6"
            }
        }
    
    def get_theme(self, theme_name):
        """Obtener un tema específico"""
        return self.themes.get(theme_name, self.themes["dark_cyberpunk"])
    
    def get_theme_names(self):
        """Obtener lista de nombres de temas disponibles"""
        return list(self.themes.keys())
