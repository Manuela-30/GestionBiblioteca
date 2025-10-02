# Sistema de Gestión de Biblioteca - Consola Interactiva

Un sistema completo de gestión de biblioteca desarrollado en Python que funciona completamente desde la consola con menús interactivos.

## 🚀 Características

### Gestión de Libros
- ✅ Agregar nuevos libros con ISBN, título, autor, año y número de copias
- ✅ Buscar libros por título, autor o ISBN
- ✅ Ver todos los libros disponibles
- ✅ Eliminar libros (solo si no están prestados)
- ✅ Control de inventario con copias disponibles/prestadas

### Gestión de Usuarios
- ✅ Registrar nuevos usuarios con ID único, nombre y email
- ✅ Ver lista completa de usuarios
- ✅ Eliminar usuarios (solo si no tienen préstamos activos)
- ✅ Ver historial de libros prestados por usuario

### Gestión de Préstamos
- ✅ Prestar libros a usuarios registrados
- ✅ Devolver libros prestados
- ✅ Ver todos los préstamos activos
- ✅ Control automático de disponibilidad
- ✅ Validaciones completas (usuario existe, libro disponible, etc.)

### Reportes y Estadísticas
- ✅ Libros más prestados
- ✅ Usuarios más activos
- ✅ Estadísticas generales del sistema
- ✅ Tasa de utilización de la biblioteca

## 🏗️ Arquitectura

El sistema está organizado en una arquitectura modular y limpia:

```
src/
├── models/          # Modelos de datos (Book, User)
├── services/        # Lógica de negocio (LibraryService)
└── ui/             # Interfaz de usuario (ConsoleUI)
```

### Modelos
- **Book**: Representa un libro con ISBN, título, autor, año y control de copias
- **User**: Representa un usuario con ID, nombre, email y libros prestados

### Servicios
- **LibraryService**: Maneja toda la lógica de negocio del sistema

### Interfaz de Usuario
- **ConsoleUI**: Proporciona una interfaz de consola interactiva y amigable

## 🎮 Cómo Usar

### Ejecutar el Sistema
```bash
python main.py
```

### Navegación
- Usa los números del menú para navegar
- Sigue las instrucciones en pantalla
- Presiona Enter para continuar después de cada operación
- Usa Ctrl+C para salir en cualquier momento

### Datos de Ejemplo
El sistema viene precargado con:
- 5 libros de ejemplo
- 3 usuarios de ejemplo
- Listo para hacer préstamos inmediatamente

## 📋 Funcionalidades Detalladas

### Menú Principal
1. **Gestión de Libros** - Administrar el catálogo de libros
2. **Gestión de Usuarios** - Administrar usuarios registrados
3. **Gestión de Préstamos** - Manejar préstamos y devoluciones
4. **Reportes** - Ver estadísticas y reportes del sistema
5. **Salir** - Cerrar la aplicación

### Validaciones Implementadas
- ✅ No se pueden prestar libros sin copias disponibles
- ✅ Un usuario no puede tener el mismo libro prestado dos veces
- ✅ No se pueden eliminar libros con copias prestadas
- ✅ No se pueden eliminar usuarios con préstamos activos
- ✅ Validación de entrada de datos (números, campos requeridos)

### Características de la Interfaz
- 🎨 Interfaz limpia y organizada
- 📱 Menús intuitivos y fáciles de navegar
- 🔍 Búsqueda flexible por múltiples criterios
- 📊 Reportes detallados y estadísticas útiles
- ⚡ Respuestas rápidas y confirmaciones claras

## 🛠️ Requisitos Técnicos

- Python 3.6 o superior
- No requiere librerías externas
- Compatible con Windows, macOS y Linux
- Funciona completamente en la terminal/consola

## 🎯 Casos de Uso

### Para Bibliotecarios
- Gestionar el inventario completo de libros
- Registrar nuevos usuarios
- Procesar préstamos y devoluciones
- Generar reportes de actividad

### Para Administradores
- Ver estadísticas de uso del sistema
- Identificar libros más populares
- Monitorear usuarios más activos
- Controlar la utilización de recursos

## 🔧 Extensibilidad

El sistema está diseñado para ser fácilmente extensible:
- Agregar nuevos tipos de reportes
- Implementar fechas de vencimiento
- Añadir categorías de libros
- Integrar con bases de datos
- Agregar notificaciones por email

¡Disfruta usando el Sistema de Gestión de Biblioteca! 📚