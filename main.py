#!/usr/bin/env python3
"""
Sistema de Gestión de Biblioteca - Aplicación de Consola
========================================================

Este es un sistema completo de gestión de biblioteca que permite:
- Gestionar libros (agregar, eliminar, buscar)
- Gestionar usuarios (registrar, eliminar)
- Gestionar préstamos (prestar, devolver)
- Generar reportes y estadísticas

Autor: Sistema de Gestión de Biblioteca
Versión: 1.0
"""

from src.ui.console_ui import ConsoleUI

def main():
    """Función principal que inicia la aplicación"""
    try:
        app = ConsoleUI()
        app.run()
    except KeyboardInterrupt:
        print("\n\n¡Aplicación cerrada por el usuario!")
    except Exception as e:
        print(f"\nError inesperado: {e}")
        print("Por favor, contacta al administrador del sistema.")

if __name__ == "__main__":
    main()