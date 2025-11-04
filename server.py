#!/usr/bin/env python3
"""
Servidor de Desarrollo para el Sistema de Biblioteca
===================================================

Servidor Flask que integra el backend Python con el frontend React.
Optimizado con estructuras de datos avanzadas para máximo rendimiento.
"""

import sys
import os

# Agregar el directorio src al path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from api.routes import app

if __name__ == '__main__':
    print("🚀 Iniciando Sistema de Biblioteca Completo...")
    print("📊 Backend: Python + Flask + Estructuras de Datos Avanzadas")
    print("🎨 Frontend: React + TypeScript + Tailwind CSS")
    print("🌳 Optimización: Árboles Binarios para búsquedas O(log n)")
    print("=" * 60)
    print("🌐 Servidor disponible en: http://localhost:5000")
    print("📚 API endpoints disponibles en: http://localhost:5000/api/")
    print("💡 Documentación técnica incluida en comentarios del código")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)