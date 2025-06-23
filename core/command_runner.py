#!/usr/bin/env python3
"""
CommandRunner - Hilo para ejecutar comandos sin bloquear la interfaz
"""

import os
import subprocess
from PyQt6.QtCore import QThread, pyqtSignal


class CommandRunner(QThread):
    """Hilo para ejecutar comandos sin bloquear la interfaz"""
    output_ready = pyqtSignal(str, str)  # texto, tipo
    finished_execution = pyqtSignal()
    password_required = pyqtSignal(str)  # comando que requiere contraseña
    
    def __init__(self, command, password=None):
        super().__init__()
        self.command = command
        self.password = password
        self.process = None
        # Timeout más largo para comandos de instalación
        self.timeout = 300 if any(keyword in command.lower() for keyword in ['install', 'upgrade', 'update']) else 30
    
    def run(self):
        try:
            if self.command.strip() == "clear":
                self.output_ready.emit("CLEAR_TERMINAL", "clear")
                return
            
            if self.command.startswith("cd "):
                path = self.command[3:].strip()
                try:
                    os.chdir(os.path.expanduser(path))
                    self.output_ready.emit(f"📂 Directorio cambiado a: {os.getcwd()}\n", "success")
                except Exception as e:
                    self.output_ready.emit(f"❌ Error: {str(e)}\n", "error")
                return
            
            # Manejar comandos sudo
            if self.command.strip().startswith("sudo "):
                self._run_sudo_command()
                return
            
            # Ejecutar comando normal con salida en tiempo real
            self._run_command_realtime()
                
        except subprocess.TimeoutExpired:
            if self.process:
                self.process.kill()
                self.process.wait()  # Asegurar que el proceso termine
            self.output_ready.emit("⏰ Comando cancelado por timeout (30s)\n", "error")
        except Exception as e:
            self.output_ready.emit(f"❌ Error ejecutando comando: {str(e)}\n", "error")
        finally:
            # Asegurar que el proceso se limpie correctamente
            if self.process:
                try:
                    if self.process.poll() is None:  # Si aún está ejecutándose
                        self.process.terminate()
                        self.process.wait(timeout=3)  # Esperar máximo 3 segundos
                except subprocess.TimeoutExpired:
                    # Si no responde, forzar cierre
                    self.process.kill()
                    self.process.wait()
                except Exception:
                    pass  # Ignorar errores de limpieza
                finally:
                    self.process = None
            
            self.finished_execution.emit()
    
    def _run_command_realtime(self):
        """Ejecutar comando con salida en tiempo real"""
        try:
            self.process = subprocess.Popen(
                self.command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # Combinar stderr con stdout
                text=True,
                bufsize=1,  # Línea por línea
                universal_newlines=True,
                cwd=os.getcwd(),
                preexec_fn=os.setsid  # Crear nuevo grupo de procesos
            )
            
            # Leer salida línea por línea
            while True:
                output = self.process.stdout.readline()
                if output == '' and self.process.poll() is not None:
                    break
                if output:
                    self.output_ready.emit(output, "normal")
            
            # Esperar a que termine y obtener código de retorno
            return_code = self.process.wait()
            if return_code != 0:
                self.output_ready.emit(f"❌ Comando terminó con código de error: {return_code}\n", "error")
                
        except Exception as e:
            self.output_ready.emit(f"❌ Error ejecutando comando: {str(e)}\n", "error")
        finally:
            # Asegurar limpieza del proceso
            if self.process:
                try:
                    self.process.stdout.close()
                except:
                    pass
    
    def _run_sudo_command(self):
        """Ejecutar comando sudo con contraseña y salida en tiempo real"""
        try:
            if not self.password:
                self.password_required.emit(self.command)
                return
            
            # Ejecutar comando sudo con contraseña
            self.process = subprocess.Popen(
                ['sudo', '-S'] + self.command.split()[1:],  # -S lee contraseña desde stdin
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # Combinar stderr con stdout
                text=True,
                bufsize=1,  # Línea por línea
                universal_newlines=True,
                cwd=os.getcwd(),
                preexec_fn=os.setsid  # Crear nuevo grupo de procesos
            )
            
            # Enviar contraseña
            self.process.stdin.write(self.password + '\n')
            self.process.stdin.flush()
            self.process.stdin.close()
            
            # Leer salida línea por línea
            while True:
                output = self.process.stdout.readline()
                if output == '' and self.process.poll() is not None:
                    break
                if output and "password" not in output.lower():
                    self.output_ready.emit(output, "normal")
            
            # Verificar código de retorno
            return_code = self.process.wait()
            if return_code == 0:
                self.output_ready.emit("✅ Comando sudo ejecutado exitosamente\n", "success")
            else:
                self.output_ready.emit(f"❌ Error en comando sudo (código: {return_code})\n", "error")
                
        except subprocess.TimeoutExpired:
            if self.process:
                self.process.kill()
                self.process.wait()
            self.output_ready.emit("⏰ Comando sudo cancelado por timeout\n", "error")
        except Exception as e:
            self.output_ready.emit(f"❌ Error ejecutando sudo: {str(e)}\n", "error")
        finally:
            # Asegurar limpieza del proceso
            if self.process:
                try:
                    if self.process.stdin:
                        self.process.stdin.close()
                    if self.process.stdout:
                        self.process.stdout.close()
                except:
                    pass
    
    def terminate_safely(self):
        """Terminar de forma segura el comando en ejecución"""
        if self.process:
            try:
                # Intentar terminar de forma suave primero
                if self.process.poll() is None:  # Si aún está ejecutándose
                    self.process.terminate()
                    
                    # Esperar un poco para que termine
                    try:
                        self.process.wait(timeout=3)
                    except subprocess.TimeoutExpired:
                        # Si no responde, forzar cierre
                        self.process.kill()
                        self.process.wait()
                        
            except Exception:
                pass  # Ignorar errores de limpieza
            finally:
                self.process = None
        
        # Terminar el hilo
        if self.isRunning():
            self.quit()
            self.wait(3000)  # Esperar máximo 3 segundos
