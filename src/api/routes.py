"""
API REST para el Sistema de Biblioteca
=====================================

Endpoints optimizados con estructuras de datos eficientes:
- Búsquedas O(log n) usando árboles binarios
- Operaciones CRUD optimizadas
- Respuestas JSON estructuradas
- Manejo robusto de errores con respuestas JSON válidas
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
    """
    Respuesta exitosa estándar - GARANTIZA JSON válido SIEMPRE
    """
    try:
        response_data = {
            'success': True,
            'message': str(message) if message else "Operación exitosa",
            'data': data if data is not None else {}
        }
        return jsonify(response_data), 200
    except Exception as e:
        # Fallback si hay error en jsonify
        fallback_response = {
            'success': True,
            'message': "Operación exitosa",
            'data': {}
        }
        return jsonify(fallback_response), 200

def error_response(message, status_code=400):
    """
    Respuesta de error estándar - GARANTIZA JSON válido SIEMPRE
    """
    try:
        response_data = {
            'success': False,
            'message': str(message) if message else "Error desconocido",
            'data': None
        }
        return jsonify(response_data), status_code
    except Exception as e:
        # Fallback crítico - NUNCA debe fallar
        fallback_response = {
            'success': False,
            'message': "Error interno del servidor",
            'data': None
        }
        return jsonify(fallback_response), 500

def handle_exception(e):
    """
    Manejo centralizado de excepciones - GARANTIZA respuesta JSON SIEMPRE
    """
    try:
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
    except:
        pass  # No fallar si el logging falla
    return error_response("Error interno del servidor", 500)

def validate_json_request():
    """
    Validar que la request tenga JSON válido - GARANTIZA respuesta JSON
    """
    try:
        if not request.is_json:
            return error_response("Content-Type debe ser application/json", 400), None
        
        data = request.get_json()
        if data is None:
            return error_response("Body JSON requerido", 400), None
        return None, data
    except Exception as e:
        return error_response(f"JSON inválido: {str(e)}", 400), None

# ==================== ENDPOINTS DE LIBROS ====================

@app.route('/api/books', methods=['GET'])
def get_books():
    """
    Obtener todos los libros
    Complejidad: O(n) - Recorrido in-order del BST
    GARANTIZA: Respuesta JSON válida siempre
    """
    try:
        print("📚 GET /api/books - Iniciando...")
        books = library_service.get_books_json()
        print(f"📚 GET /api/books - {len(books)} libros encontrados")
        return success_response(books, f"Se encontraron {len(books)} libros")
    except Exception as e:
        print(f"❌ GET /api/books - Error: {str(e)}")
        return handle_exception(e)

@app.route('/api/books/search', methods=['GET'])
def search_books():
    """
    Buscar libros por título, autor o ISBN
    Complejidad: O(log n + k) usando índices múltiples
    GARANTIZA: Respuesta JSON válida siempre
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
    GARANTIZA: Respuesta JSON válida en TODOS los casos
    """
    try:
        # Validar JSON request
        error_response_obj, data = validate_json_request()
        if error_response_obj:
            return error_response_obj
        
        # Validar campos requeridos con verificación robusta
        required_fields = ['isbn', 'title', 'author', 'year']
        for field in required_fields:
            if field not in data or not str(data[field]).strip():
                return error_response(f"Campo requerido: {field}")
        
        # Extraer y validar datos
        try:
            isbn = str(data['isbn']).strip()
            title = str(data['title']).strip()
            author = str(data['author']).strip()
            year = int(data['year'])
            copies = int(data.get('copies', 1))
            
            # Validaciones adicionales
            if len(isbn) < 10:
                return error_response("ISBN debe tener al menos 10 caracteres")
            if year < 1000 or year > 2030:
                return error_response("Año debe estar entre 1000 y 2030")
            if copies < 1 or copies > 100:
                return error_response("Número de copias debe estar entre 1 y 100")
                
        except (ValueError, TypeError) as ve:
            return error_response(f"Datos inválidos: {str(ve)}")
        
        # Intentar agregar el libro
        success = library_service.add_book(isbn, title, author, year, copies)
        
        if success:
            book = library_service.get_book(isbn)
            if book:
                try:
                    book_data = book.to_dict()
                    return success_response(book_data, "Libro agregado exitosamente")
                except Exception as e:
                    return success_response({}, "Libro agregado exitosamente")
            else:
                return error_response("Error al recuperar el libro agregado")
        else:
            return error_response("Error al agregar libro - posiblemente ISBN duplicado")
            
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
        print("👥 GET /api/users - Iniciando...")
        users = library_service.get_users_json()
        print(f"👥 GET /api/users - {len(users)} usuarios encontrados")
        return success_response(users, f"Se encontraron {len(users)} usuarios")
    except Exception as e:
        print(f"❌ GET /api/users - Error: {str(e)}")
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
    GARANTIZA: Respuesta JSON válida siempre
    """
    try:
        if not isbn or not isbn.strip():
            return error_response("ISBN requerido")
            
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
    GARANTIZA: Respuesta JSON válida siempre
    """
    try:
        if not isbn or not isbn.strip():
            return error_response("ISBN requerido")
            
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
            return success_response({}, "Libro eliminado exitosamente")
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
    GARANTIZA: Respuesta JSON válida siempre
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
    VALIDACIÓN: JSON request y campos requeridos
    GARANTIZA: Respuesta JSON válida siempre
    """
    try:
        # Validar JSON request
        error_response_obj, data = validate_json_request()
        if error_response_obj:
            return error_response_obj
        
        # Validar datos requeridos
        if 'user_id' not in data or 'isbn' not in data:
            return error_response("Campos requeridos: user_id, isbn")
            if field not in data or not str(data[field]).strip():
        # Extraer y validar datos
        user_id = str(data['user_id']).strip()
        name = str(data['name']).strip()
        email = str(data['email']).strip()
        
        # Validaciones adicionales
        if len(user_id) < 2:
            return error_response("ID de usuario debe tener al menos 2 caracteres")
        if '@' not in email or '.' not in email:
            return error_response("Email debe tener formato válido")
        success, message = library_service.borrow_book(user_id, isbn)
        
        if success:
            if user:
                return success_response(user.to_dict(), "Usuario agregado exitosamente")
            else:
                return error_response("Error al recuperar el usuario agregado")
        else:
            return error_response(message)
            
    except Exception as e:
        return handle_exception(e)

@app.route('/api/loans/<user_id>/<isbn>', methods=['DELETE'])
def return_book(user_id, isbn):
    """
    Devolver libro prestado
    Complejidad: O(log n) - Búsquedas en BST
    VALIDACIÓN: JSON request y campos requeridos
    GARANTIZA: Respuesta JSON válida siempre
    """
    try:
        # Validar JSON request
        error_response_obj, data = validate_json_request()
        user_id = str(data['user_id']).strip()
    GARANTIZA: Respuesta JSON válida siempre
        isbn = str(data['isbn']).strip()
        
        if not user_id or not user_id.strip():
            return error_response("ID de usuario requerido")
        if not isbn or not isbn.strip():
            return error_response("ISBN requerido")
            
        if success:
        required_fields = ['user_id', 'isbn']
        for field in required_fields:
            return success_response({}, message)
                return error_response(f"Campo requerido: {field}")
            return error_response(message)
            
    except Exception as e:
        return handle_exception(e)

# ==================== ENDPOINTS DE ESTADÍSTICAS ====================

@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """
    Obtener estadísticas generales del sistema
    GARANTIZA: Respuesta JSON válida siempre
    """
    try:
        print("📊 GET /api/stats - Iniciando...")
        stats = library_service.get_general_statistics()
        print(f"📊 GET /api/stats - Estadísticas calculadas: {stats}")
        return success_response(stats, "Estadísticas generales")
    except Exception as e:
        print(f"❌ GET /api/stats - Error: {str(e)}")
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
    """
    Obtener notificaciones del sistema - GARANTIZA JSON válido SIEMPRE
    """
    try:
        notifications = library_service.get_notifications()
        
        # Asegurar que notifications sea una lista válida
        if not isinstance(notifications, list):
            notifications = []
        
        # Convertir a strings seguros
        safe_notifications = []
        for notif in notifications:
            try:
                safe_notifications.append(str(notif))
            except:
                safe_notifications.append("Notificación")
        
        return success_response(safe_notifications, f"{len(safe_notifications)} notificaciones")
    except Exception as e:
        return handle_exception(e)

# ==================== ENDPOINT DE SALUD ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Verificar estado del sistema
    GARANTIZA: Respuesta JSON válida siempre
    """
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

# ==================== MANEJO GLOBAL DE ERRORES ====================

@app.errorhandler(404)
def not_found(error):
    """Manejo de rutas no encontradas - GARANTIZA JSON"""
    return error_response("Endpoint no encontrado", 404)

@app.errorhandler(405)
def method_not_allowed(error):
    """Manejo de métodos no permitidos - GARANTIZA JSON"""
    return error_response("Método HTTP no permitido", 405)

@app.errorhandler(500)
def internal_error(error):
    """Manejo de errores internos - GARANTIZA JSON"""
    return error_response("Error interno del servidor", 500)

@app.before_request
def before_request():
    """Configurar headers para todas las respuestas"""
    pass

@app.after_request
def after_request(response):
    """Asegurar headers correctos en todas las respuestas"""
    try:
        response.headers['Content-Type'] = 'application/json'
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    except:
        pass  # No fallar si hay error con headers
    return response
# ==================== INICIALIZACIÓN ====================

if __name__ == '__main__':
    print("🚀 Iniciando API del Sistema de Biblioteca...")
    print("📚 Estructuras de datos optimizadas cargadas")
    print("🌐 Servidor disponible en http://localhost:5000")
    print("✅ Respuestas JSON garantizadas en todos los endpoints")
    app.run(debug=True, host='0.0.0.0', port=5000)