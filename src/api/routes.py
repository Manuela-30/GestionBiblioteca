"""
API REST para el Sistema de Biblioteca
=====================================

Endpoints optimizados con estructuras de datos eficientes:
- Búsquedas O(log n) usando árboles binarios
- Operaciones CRUD optimizadas
- Respuestas JSON estructuradas
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from src.services.library_service import LibraryService
import traceback

# Crear aplicación Flask
app = Flask(__name__)
CORS(app)  # Permitir requests desde el frontend

# Instancia global del servicio
library_service = LibraryService()

# ==================== UTILIDADES ====================

def success_response(data, message="Operación exitosa"):
    """Respuesta exitosa estándar"""
    return jsonify({
        'success': True,
        'message': message,
        'data': data
    })

def error_response(message, status_code=400):
    """Respuesta de error estándar"""
    return jsonify({
        'success': False,
        'message': message,
        'data': None
    }), status_code

def handle_exception(e):
    """Manejo centralizado de excepciones"""
    print(f"Error: {str(e)}")
    print(traceback.format_exc())
    return error_response("Error interno del servidor", 500)

# ==================== ENDPOINTS DE LIBROS ====================

@app.route('/api/books', methods=['GET'])
def get_books():
    """
    Obtener todos los libros
    Complejidad: O(n) - Recorrido in-order del BST
    """
    try:
        books = library_service.get_books_json()
        return success_response(books, f"Se encontraron {len(books)} libros")
    except Exception as e:
        return handle_exception(e)

@app.route('/api/books/search', methods=['GET'])
def search_books():
    """
    Buscar libros por título, autor o ISBN
    Complejidad: O(log n + k) usando índices múltiples
    """
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return error_response("Parámetro de búsqueda 'q' requerido")
        
        books = library_service.search_books_json(query)
        return success_response(books, f"Se encontraron {len(books)} libros para '{query}'")
    except Exception as e:
        return handle_exception(e)

@app.route('/api/books/popular', methods=['GET'])
def get_popular_books():
    """
    Obtener libros más populares
    Complejidad: O(n) - Recorrido ordenado del índice de popularidad
    """
    try:
        limit = int(request.args.get('limit', 10))
        popular_books = library_service.get_most_borrowed_books(limit)
        
        result = []
        for book, times_borrowed in popular_books:
            book_data = book.to_dict()
            book_data['times_borrowed'] = times_borrowed
            result.append(book_data)
        
        return success_response(result, f"Top {len(result)} libros más populares")
    except Exception as e:
        return handle_exception(e)

@app.route('/api/books/<isbn>', methods=['GET'])
def get_book(isbn):
    """
    Obtener libro por ISBN
    Complejidad: O(log n) - Búsqueda en BST
    """
    try:
        book = library_service.get_book(isbn)
        if book:
            return success_response(book.to_dict(), "Libro encontrado")
        else:
            return error_response("Libro no encontrado", 404)
    except Exception as e:
        return handle_exception(e)

@app.route('/api/books', methods=['POST'])
def add_book():
    """
    Agregar nuevo libro
    Complejidad: O(log n) - Inserción en BST e índices
    """
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['isbn', 'title', 'author', 'year']
        for field in required_fields:
            if field not in data:
                return error_response(f"Campo requerido: {field}")
        
        isbn = data['isbn']
        title = data['title']
        author = data['author']
        year = int(data['year'])
        copies = int(data.get('copies', 1))
        
        success = library_service.add_book(isbn, title, author, year, copies)
        
        if success:
            book = library_service.get_book(isbn)
            return success_response(book.to_dict(), "Libro agregado exitosamente")
        else:
            return error_response("Error al agregar libro")
    
    except ValueError as e:
        return error_response(f"Datos inválidos: {str(e)}")
    except Exception as e:
        return handle_exception(e)

@app.route('/api/books/<isbn>', methods=['DELETE'])
def delete_book(isbn):
    """
    Eliminar libro
    Complejidad: O(log n) - Búsqueda y eliminación en BST
    """
    try:
        success = library_service.remove_book(isbn)
        
        if success:
            return success_response(None, "Libro eliminado exitosamente")
        else:
            return error_response("No se puede eliminar el libro (puede tener copias prestadas)")
    except Exception as e:
        return handle_exception(e)

# ==================== ENDPOINTS DE USUARIOS ====================

@app.route('/api/users', methods=['GET'])
def get_users():
    """
    Obtener todos los usuarios
    Complejidad: O(n) - Recorrido in-order del BST
    """
    try:
        users = library_service.get_users_json()
        return success_response(users, f"Se encontraron {len(users)} usuarios")
    except Exception as e:
        return handle_exception(e)

@app.route('/api/users/search', methods=['GET'])
def search_users():
    """
    Buscar usuarios por nombre, email o ID
    Complejidad: O(log n + k) usando índices múltiples
    """
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return error_response("Parámetro de búsqueda 'q' requerido")
        
        users = library_service.search_users_json(query)
        return success_response(users, f"Se encontraron {len(users)} usuarios para '{query}'")
    except Exception as e:
        return handle_exception(e)

@app.route('/api/users/active', methods=['GET'])
def get_active_users():
    """
    Obtener usuarios más activos
    Complejidad: O(n) - Recorrido ordenado del índice de actividad
    """
    try:
        limit = int(request.args.get('limit', 10))
        active_users = library_service.get_most_active_users(limit)
        
        result = []
        for user, activity_score in active_users:
            user_data = user.to_dict()
            user_data['activity_score'] = activity_score
            result.append(user_data)
        
        return success_response(result, f"Top {len(result)} usuarios más activos")
    except Exception as e:
        return handle_exception(e)

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    Obtener usuario por ID
    Complejidad: O(log n) - Búsqueda en BST
    """
    try:
        user = library_service.get_user(user_id)
        if user:
            return success_response(user.to_dict(), "Usuario encontrado")
        else:
            return error_response("Usuario no encontrado", 404)
    except Exception as e:
        return handle_exception(e)

@app.route('/api/users', methods=['POST'])
def add_user():
    """
    Agregar nuevo usuario
    Complejidad: O(log n) - Inserción en BST e índices
    """
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['user_id', 'name', 'email']
        for field in required_fields:
            if field not in data:
                return error_response(f"Campo requerido: {field}")
        
        user_id = data['user_id']
        name = data['name']
        email = data['email']
        
        success = library_service.add_user(user_id, name, email)
        
        if success:
            user = library_service.get_user(user_id)
            return success_response(user.to_dict(), "Usuario agregado exitosamente")
        else:
            return error_response("Error al agregar usuario (ID ya existe)")
    
    except Exception as e:
        return handle_exception(e)

@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Eliminar usuario
    Complejidad: O(log n) - Búsqueda y eliminación en BST
    """
    try:
        success = library_service.remove_user(user_id)
        
        if success:
            return success_response(None, "Usuario eliminado exitosamente")
        else:
            return error_response("No se puede eliminar el usuario (tiene libros prestados)")
    except Exception as e:
        return handle_exception(e)

@app.route('/api/users/<user_id>/books', methods=['GET'])
def get_user_books(user_id):
    """
    Obtener libros prestados por usuario
    Complejidad: O(log n + k) donde k es número de libros prestados
    """
    try:
        books = library_service.get_user_borrowed_books(user_id)
        books_data = [book.to_dict() for book in books]
        return success_response(books_data, f"Usuario tiene {len(books)} libros prestados")
    except Exception as e:
        return handle_exception(e)

# ==================== ENDPOINTS DE PRÉSTAMOS ====================

@app.route('/api/loans', methods=['GET'])
def get_loans():
    """Obtener todos los préstamos activos"""
    try:
        loans = library_service.get_active_loans()
        return success_response(loans, f"Se encontraron {len(loans)} préstamos activos")
    except Exception as e:
        return handle_exception(e)

@app.route('/api/loans', methods=['POST'])
def borrow_book():
    """
    Prestar libro a usuario
    Complejidad: O(log n) - Búsquedas en BST
    """
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if 'user_id' not in data or 'isbn' not in data:
            return error_response("Campos requeridos: user_id, isbn")
        
        user_id = data['user_id']
        isbn = data['isbn']
        
        success, message = library_service.borrow_book(user_id, isbn)
        
        if success:
            return success_response(None, message)
        else:
            return error_response(message)
    
    except Exception as e:
        return handle_exception(e)

@app.route('/api/loans/<user_id>/<isbn>', methods=['DELETE'])
def return_book(user_id, isbn):
    """
    Devolver libro prestado
    Complejidad: O(log n) - Búsquedas en BST
    """
    try:
        success, message = library_service.return_book(user_id, isbn)
        
        if success:
            return success_response(None, message)
        else:
            return error_response(message)
    
    except Exception as e:
        return handle_exception(e)

# ==================== ENDPOINTS DE ESTADÍSTICAS ====================

@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """Obtener estadísticas generales del sistema"""
    try:
        stats = library_service.get_general_statistics()
        return success_response(stats, "Estadísticas generales")
    except Exception as e:
        return handle_exception(e)

@app.route('/api/history', methods=['GET'])
def get_history():
    """Obtener historial de operaciones"""
    try:
        limit = int(request.args.get('limit', 20))
        history = library_service.get_operation_history(limit)
        return success_response(history, f"Últimas {len(history)} operaciones")
    except Exception as e:
        return handle_exception(e)

@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    """Obtener notificaciones del sistema"""
    try:
        notifications = library_service.get_notifications()
        return success_response(notifications, f"{len(notifications)} notificaciones")
    except Exception as e:
        return handle_exception(e)

# ==================== ENDPOINT DE SALUD ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verificar estado del sistema"""
    try:
        stats = library_service.get_general_statistics()
        return success_response({
            'status': 'healthy',
            'books_count': stats.get('total_books', 0),
            'users_count': stats.get('total_users', 0),
            'active_loans': stats.get('borrowed_copies', 0)
        }, "Sistema funcionando correctamente")
    except Exception as e:
        return handle_exception(e)

# ==================== INICIALIZACIÓN ====================

if __name__ == '__main__':
    print("🚀 Iniciando API del Sistema de Biblioteca...")
    print("📚 Estructuras de datos optimizadas cargadas")
    print("🌐 Servidor disponible en http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)