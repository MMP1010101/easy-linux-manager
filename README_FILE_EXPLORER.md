# 📁 Explorador de Archivos - Modo Easy

## ✨ Características Principales

El **Modo Easy** ahora incluye un explorador de archivos visual y fácil de usar que permite a los usuarios gestionar sus archivos y carpetas de manera intuitiva.

### 🎯 Funcionalidades

#### 📍 Navegación
- **Visualización de carpetas y archivos**: Se muestran con iconos distintivos (📁 para carpetas, 📄 para archivos)
- **Navegación por doble clic**: Haz doble clic en cualquier carpeta para entrar en ella
- **Botón "Atrás"**: Navega al directorio padre
- **Botón "Inicio"**: Regresa rápidamente a tu carpeta personal
- **Barra de ruta**: Muestra la ubicación actual en todo momento

#### ⚡ Acciones Disponibles
1. **📁 Nueva Carpeta**: Crea una nueva carpeta en la ubicación actual
2. **📄 Nuevo Archivo**: Crea un nuevo archivo vacío
3. **🗑️ Eliminar**: Elimina el archivo o carpeta seleccionada (con confirmación)
4. **✏️ Renombrar**: Cambia el nombre del elemento seleccionado

#### 🔍 Información Detallada
- **Panel de información**: Muestra detalles del archivo/carpeta seleccionada
- **Tamaño de archivos**: Formato legible (bytes, KB, MB)
- **Tipo de elemento**: Identifica si es archivo o carpeta
- **Ruta completa**: Muestra la ubicación exacta del elemento

### 🔒 Restricciones de Seguridad

Por seguridad, **solo puedes realizar modificaciones dentro de tu directorio personal**:
- ✅ **Permitido**: Crear, eliminar, renombrar en `/home/usuario/`
- ❌ **Restringido**: Modificaciones en carpetas del sistema

### 🎨 Interfaz de Usuario

#### Diseño Dividido
- **Panel izquierdo**: Lista de archivos y carpetas
- **Panel derecho**: Acciones y información detallada

#### Controles Intuitivos
- **Clic simple**: Seleccionar elemento
- **Doble clic**: Abrir carpeta
- **Botones grandes**: Fácil identificación de acciones
- **Colores distintivos**: El botón eliminar es rojo para mayor claridad

### 💡 Consejos de Uso

1. **Selecciona antes de actuar**: Haz clic en un archivo/carpeta antes de usar los botones de acción
2. **Confirmación de eliminación**: Siempre se pide confirmación antes de eliminar
3. **Navegación segura**: Solo se permite navegar y modificar archivos en tu carpeta personal
4. **Información útil**: Revisa el panel de información para conocer detalles del elemento seleccionado

### 🚨 Mensajes de Ayuda

El panel derecho incluye consejos útiles:
- 💡 Haz doble clic en una carpeta para abrirla
- 🔍 Haz clic simple para seleccionar
- ⚠️ Solo se pueden modificar archivos en tu carpeta personal

### 🎯 Casos de Uso Comunes

1. **Organizar documentos**: Crear carpetas para diferentes tipos de archivos
2. **Limpiar descargas**: Eliminar archivos innecesarios de la carpeta Downloads
3. **Crear estructura de proyectos**: Organizar archivos de trabajo en carpetas específicas
4. **Renombrar archivos**: Dar nombres más descriptivos a tus archivos

---

## 🛠️ Aspectos Técnicos

### Tecnologías Utilizadas
- **PyQt6**: Framework de interfaz gráfica
- **pathlib**: Manejo moderno de rutas de archivos
- **shutil**: Operaciones avanzadas de archivos

### Seguridad Implementada
- Verificación de permisos antes de cada operación
- Restricción a directorios del usuario
- Confirmación de acciones destructivas
- Manejo de errores con mensajes informativos

Este explorador de archivos convierte el modo Easy en una herramienta poderosa pero segura para la gestión básica de archivos, ideal para usuarios que prefieren interfaces gráficas sobre la línea de comandos.
