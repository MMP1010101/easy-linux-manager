# Linux GUI Application for Terminal Management

Este proyecto es una aplicación de interfaz gráfica (GUI) diseñada para simplificar la gestión de sistemas Linux proporcionando una terminal completamente funcional a través de una interfaz familiar. La aplicación está disponible en múltiples versiones para máxima compatibilidad.

## Características

- Terminal completamente funcional (no simulador)
- Ejecución de comandos Bash con salida en tiempo real
- Interfaz de usuario intuitiva y moderna
- Soporte para navegación de directorios
- Múltiples versiones disponibles (Electron, Web, Python)

## Versiones Disponibles

### 1. Aplicación de Escritorio (Python + Tkinter) - **RECOMENDADA**
La versión más estable y compatible, usando Python nativo.

### 2. Aplicación Web
Versión basada en navegador con terminal xterm.js completamente funcional.

### 3. Aplicación Electron (Experimental)
Versión de escritorio usando Electron (puede tener problemas en entornos virtualizados).

## Estructura del Proyecto

```
linux-gui-app
├── src
│   ├── main.js              # Punto de entrada de Electron
│   ├── renderer.js          # Lógica del renderizador Electron
│   ├── components
│   │   └── CommandExecutor.js # (Legacy) Ejecutor de comandos
│   └── utils
│       └── bashRunner.js    # (Legacy) Utilidad para Bash
├── terminal_gui.py          # Aplicación de escritorio Python
├── server.js                # Servidor web para versión web
├── web.html                 # Interfaz web
├── index.html               # Interfaz Electron
├── package.json             # Configuración npm
└── README.md                # Documentación
```

## Instalación

1. Clonar el repositorio:
   ```bash
   git clone <repository-url>
   cd linux-gui-app
   ```

2. Instalar dependencias:
   ```bash
   npm install
   ```

## Uso

### Aplicación de Escritorio (Python) - RECOMENDADA

```bash
npm run start-python
# o directamente:
python3 terminal_gui.py
```

### Versión Web

```bash
npm run web
```
Luego abre tu navegador en `http://localhost:3000`

### Aplicación Electron

```bash
npm start
```

## Funcionalidades de la Terminal

- **Comandos estándar**: `ls`, `ps`, `df`, `whoami`, etc.
- **Navegación**: `cd` para cambiar directorios
- **Gestión de archivos**: `mkdir`, `rm`, `cp`, `mv`, etc.
- **Monitoreo del sistema**: `top`, `htop`, `free`, etc.
- **Comandos especiales**:
  - `clear`: Limpiar terminal
  - `exit`: Cerrar aplicación

## Ejemplos de Comandos

```bash
ls -la                    # Listar archivos detalladamente
ps aux                    # Mostrar procesos
df -h                     # Espacio en disco
free -h                   # Memoria disponible
whoami                    # Usuario actual
date                      # Fecha y hora
uptime                    # Tiempo de actividad
lscpu                     # Información del CPU
```

## Características Técnicas

- **Terminal Real**: No es un simulador, ejecuta comandos reales del sistema
- **Multiplataforma**: Funciona en cualquier distribución de Linux
- **Seguro**: Ejecuta comandos con los permisos del usuario actual
- **Responsive**: Interfaz adaptable y moderna

## Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu característica
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Ver el archivo LICENSE para detalles.