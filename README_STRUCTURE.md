# Linux GUI - Estructura Modular

## Descripción
Terminal GUI épico usando PyQt6 con arquitectura modular organizada por secciones y estilos.

## Estructura del Proyecto

```
linux-gui-app/
├── app.py                      # Aplicación principal
├── main_window.py              # Ventana principal
├── logo.png                    # Logo de la aplicación
├── README_STRUCTURE.md         # Este archivo
├── terminal_gui_pyqt6.py       # Archivo original (mantenido como respaldo)
│
├── components/                 # Componentes de la interfaz
│   ├── __init__.py
│   ├── menu.py                 # Widget del menú principal
│   ├── terminal.py             # Widget del terminal
│   ├── easy_mode.py            # Widget del modo Easy
│   └── dependencies.py         # Widget de dependencias
│
├── core/                       # Lógica de negocio
│   ├── __init__.py
│   └── command_runner.py       # Ejecutor de comandos
│
└── styles/                     # Estilos y temas
    ├── __init__.py
    ├── themes.py               # Definición de temas
    ├── menu_styles.py          # Estilos del menú
    ├── terminal_styles.py      # Estilos del terminal
    └── mode_styles.py          # Estilos de los modos
```

## Organización por Secciones

### 1. **Menú Principal** (`components/menu.py`)
- Widget independiente para el menú principal
- Manejo del logo y botones de navegación
- Estilos específicos en `styles/menu_styles.py`

### 2. **Terminal** (`components/terminal.py`)
- Widget completo del terminal
- Integración con `CommandRunner` para ejecución de comandos
- Estilos específicos en `styles/terminal_styles.py`

### 3. **Modos Adicionales**
- **Easy Mode** (`components/easy_mode.py`): Modo simplificado
- **Dependencies** (`components/dependencies.py`): Instalación de dependencias
- Estilos específicos en `styles/mode_styles.py`

## Organización por Estilos

### 1. **Temas** (`styles/themes.py`)
- Definición centralizada de todos los temas
- Clase `ThemeManager` para gestión de temas

### 2. **Estilos del Menú** (`styles/menu_styles.py`)
- `get_menu_styles()`: Estilos específicos del menú
- `get_general_menu_styles()`: Estilos generales

### 3. **Estilos del Terminal** (`styles/terminal_styles.py`)
- `get_terminal_styles()`: Estilos del área del terminal
- `get_terminal_text_colors()`: Colores para diferentes tipos de texto

### 4. **Estilos de Modos** (`styles/mode_styles.py`)
- `get_mode_styles()`: Estilos para diferentes modos
- `get_form_styles()`: Estilos para formularios

## Características

### ✨ **Arquitectura Modular**
- Separación clara de responsabilidades
- Fácil mantenimiento y extensión
- Código reutilizable

### 🎨 **Sistema de Temas**
- Temas centralizados y reutilizables
- Fácil cambio de tema en tiempo real
- Estilos consistentes en toda la aplicación

### 🚀 **Rendimiento**
- Ejecución de comandos en hilos separados
- Interfaz responsiva
- Gestión eficiente de memoria

## Uso

### Ejecutar la aplicación:
```bash
python app.py
```

### Agregar nuevos temas:
1. Editar `styles/themes.py`
2. Agregar nueva definición en el diccionario `themes`

### Agregar nuevos modos:
1. Crear nuevo archivo en `components/`
2. Agregar estilos en `styles/mode_styles.py`
3. Integrar en `main_window.py`

## Beneficios de la Nueva Estructura

1. **Mantenibilidad**: Cada componente tiene su propio archivo
2. **Escalabilidad**: Fácil agregar nuevas funcionalidades
3. **Reutilización**: Componentes y estilos reutilizables
4. **Organización**: Código limpio y bien estructurado
5. **Debugging**: Fácil localización de problemas

## Archivos Principales

- `app.py`: Punto de entrada de la aplicación
- `main_window.py`: Ventana principal y navegación
- `components/`: Todos los widgets de la interfaz
- `styles/`: Sistema completo de temas y estilos
- `core/`: Lógica de negocio y utilidades
