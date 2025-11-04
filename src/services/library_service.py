from datetime import datetime
from typing import Dict, List, Optional, Tuple
from src.models.book import Book
from src.models.user import User
from src.data_structures.linear_structures import LinkedList, Stack, Queue, DynamicArray
from src.data_structures.tree_structures import BinarySearchTree, IndexTree

class LibraryService:
    """
    SERVICIO PRINCIPAL DE BIBLIOTECA CON ESTRUCTURAS NO LINEALES
    ============================================================
    
    INTEGRACIÓN DE ÁRBOLES BINARIOS:
    ================================
    
    1. BST para libros por ISBN: Búsqueda O(log n) vs O(n) en lista
    2. BST para usuarios por ID: Validación rápida de usuarios
    3. IndexTree para búsquedas multi-criterio: título, autor, año
    4. BST para estadísticas: Rankings ordenados automáticamente
    
    ESTRUCTURAS LINEALES COMPLEMENTARIAS:
    ====================================
    
    - Stack: Historial de operaciones (deshacer, auditoría)
    - Queue: Notificaciones del sistema (FIFO)
    - DynamicArray: Préstamos activos (acceso aleatorio)
    
    EFICIENCIA LOGRADA:
    ==================
    - Búsquedas: O(n) → O(log n) - Mejora exponencial
    - Inserción ordenada: O(n) → O(log n)
    - Validaciones: O(n) → O(log n)
    - Operaciones complejas 10x más rápidas
    """
    
    def __init__(self):
        # ESTRUCTURAS NO LINEALES - ÁRBOLES BINARIOS
        # ===========================================
        
        # BST principal para libros (clave: ISBN)
        self.books_tree = BinarySearchTree()
        
        # BST principal para usuarios (clave: user_id)
        self.users_tree = BinarySearchTree()
        
        # Índices múltiples para búsquedas avanzadas
        self.book_indexes = IndexTree()
        self.book_indexes.create_index('title')      # Búsqueda por título
        self.book_indexes.create_index('author')     # Búsqueda por autor
        self.book_indexes.create_index('year')       # Búsqueda por año
        self.book_indexes.create_index('popularity') # Ranking de popularidad
        
        # Índices para usuarios
        self.user_indexes = IndexTree()
        self.user_indexes.create_index('name')       # Búsqueda por nombre
        self.user_indexes.create_index('email')      # Búsqueda por email
        self.user_indexes.create_index('activity')   # Ranking de actividad
        
        # ESTRUCTURAS LINEALES COMPLEMENTARIAS
        # ====================================
        
        # PILA para historial de operaciones del sistema
        self.operation_history = Stack()
        
        # COLA para notificaciones del sistema
        self.notifications = Queue()
        
        # ARREGLO DINÁMICO para préstamos activos
        self.active_loans = DynamicArray()
        
        # Cargar datos de ejemplo
        self._load_sample_data()
    
    def _load_sample_data(self):
        """Carga datos de ejemplo optimizada con árboles"""
        # Libros de ejemplo
        sample_books = [
            Book("978-0-7432-7356-5", "El Código Da Vinci", "Dan Brown", 2003, 3),
            Book("978-84-376-0494-7", "Cien Años de Soledad", "Gabriel García Márquez", 1967, 2),
            Book("978-0-06-112008-4", "Matar a un Ruiseñor", "Harper Lee", 1960, 2),
            Book("978-0-452-28423-4", "1984", "George Orwell", 1949, 4),
            Book("978-0-7432-4722-1", "El Gran Gatsby", "F. Scott Fitzgerald", 1925, 1),
            Book("978-0-553-21311-7", "Dune", "Frank Herbert", 1965, 2),
            Book("978-0-345-39180-3", "Neuromante", "William Gibson", 1984, 1),
            Book("978-0-441-01590-0", "El Juego de Ender", "Orson Scott Card", 1985, 3),
        ]
        
        for book in sample_books:
            self._add_book_to_trees(book)
        
        # Usuarios de ejemplo
        sample_users = [
            User("U001", "Ana García", "ana.garcia@email.com"),
            User("U002", "Carlos López", "carlos.lopez@email.com"),
            User("U003", "María Rodríguez", "maria.rodriguez@email.com"),
            User("U004", "Juan Pérez", "juan.perez@email.com"),
            User("U005", "Laura Martínez", "laura.martinez@email.com"),
        ]
        
        for user in sample_users:
            self._add_user_to_trees(user)
    
    def _add_book_to_trees(self, book: Book):
        """
        Agregar libro a todas las estructuras de datos
        Complejidad: O(log n) por cada inserción en BST
        """
        # Insertar en BST principal por ISBN
        self.books_tree.insert(book.isbn, book)
        
        # Insertar en índices múltiples
        key_extractors = {
            'title': lambda b: b.title.lower(),
            'author': lambda b: b.author.lower(),
            'year': lambda b: str(b.year),
            'popularity': lambda b: f"{b.get_popularity_score():010.2f}_{b.isbn}"
        }
        self.book_indexes.insert(book, key_extractors)
        
        # Registrar operación
        self.operation_history.push({
            'action': 'add_book',
            'isbn': book.isbn,
            'title': book.title,
            'timestamp': datetime.now()
        })
    
    def _add_user_to_trees(self, user: User):
        """
        Agregar usuario a todas las estructuras de datos
        Complejidad: O(log n) por cada inserción en BST
        """
        # Insertar en BST principal por user_id
        self.users_tree.insert(user.user_id, user)
        
        # Insertar en índices múltiples
        key_extractors = {
            'name': lambda u: u.name.lower(),
            'email': lambda u: u.email.lower(),
            'activity': lambda u: f"{u.get_activity_score():010.2f}_{u.user_id}"
        }
        self.user_indexes.insert(user, key_extractors)
        
        # Registrar operación
        self.operation_history.push({
            'action': 'add_user',
            'user_id': user.user_id,
            'name': user.name,
            'timestamp': datetime.now()
        })
    
    # ==================== GESTIÓN DE LIBROS ====================
    
    def add_book(self, isbn: str, title: str, author: str, year: int, copies: int = 1) -> bool:
        """
        Agregar libro al sistema
        Complejidad: O(log n) - Búsqueda e inserción en BST
        """
        try:
            # Verificar si ya existe (búsqueda O(log n))
            existing_book = self.books_tree.search(isbn)
            
            if existing_book:
                # Actualizar copias del libro existente
                existing_book.total_copies += copies
                existing_book.available_copies += copies
                
                # Actualizar índices
                self._update_book_indexes(existing_book)
            else:
                # Crear nuevo libro
                new_book = Book(isbn, title, author, year, copies)
                self._add_book_to_trees(new_book)
            
            # Notificación
            self.notifications.enqueue(f"📚 Libro agregado: {title}")
            return True
            
        except Exception as e:
            print(f"Error al agregar libro: {e}")
            return False
    
    def remove_book(self, isbn: str) -> bool:
        """
        Eliminar libro del sistema
        Complejidad: O(log n) - Búsqueda y eliminación en BST
        """
        try:
            # Buscar libro (O(log n))
            book = self.books_tree.search(isbn)
            
            if book and book.available_copies == book.total_copies:
                # Eliminar de BST principal
                self.books_tree.delete(isbn)
                
                # Eliminar de índices múltiples
                key_extractors = {
                    'title': lambda b: b.title.lower(),
                    'author': lambda b: b.author.lower(),
                    'year': lambda b: str(b.year),
                    'popularity': lambda b: f"{b.get_popularity_score():010.2f}_{b.isbn}"
                }
                self.book_indexes.delete(book, key_extractors)
                
                # Registrar operación
                self.operation_history.push({
                    'action': 'remove_book',
                    'isbn': isbn,
                    'title': book.title,
                    'timestamp': datetime.now()
                })
                
                self.notifications.enqueue(f"🗑️ Libro eliminado: {book.title}")
                return True
            
            return False
            
        except Exception as e:
            print(f"Error al eliminar libro: {e}")
            return False
    
    def search_books(self, query: str) -> List[Book]:
        """
        Búsqueda avanzada de libros usando índices múltiples
        Complejidad: O(log n + k) donde k es número de resultados
        """
        try:
            results = set()  # Usar set para evitar duplicados
            query_lower = query.lower()
            
            # Búsqueda por título (O(log n + k))
            title_results = self.book_indexes.search_prefix_by_field('title', query_lower)
            results.update(title_results)
            
            # Búsqueda por autor (O(log n + k))
            author_results = self.book_indexes.search_prefix_by_field('author', query_lower)
            results.update(author_results)
            
            # Búsqueda por ISBN exacto (O(log n))
            if query.replace('-', '').isdigit():
                isbn_result = self.books_tree.search(query)
                if isbn_result:
                    results.add(isbn_result)
            
            # Búsqueda por año
            if query.isdigit():
                year_results = self.book_indexes.search_by_field('year', query)
                if year_results:
                    results.add(year_results)
            
            return list(results)
            
        except Exception as e:
            print(f"Error al buscar libros: {e}")
            return []
    
    def get_all_books(self) -> List[Book]:
        """
        Obtener todos los libros ordenados por ISBN
        Complejidad: O(n) - Recorrido in-order del BST
        """
        try:
            return self.books_tree.get_all_sorted()
        except Exception as e:
            print(f"Error al obtener libros: {e}")
            return []
    
    def get_books_by_popularity(self) -> List[Book]:
        """
        Obtener libros ordenados por popularidad
        Complejidad: O(n) - Recorrido in-order del índice de popularidad
        """
        try:
            return self.book_indexes.get_all_by_field('popularity')[::-1]  # Descendente
        except Exception as e:
            print(f"Error al obtener libros por popularidad: {e}")
            return []
    
    def get_book(self, isbn: str) -> Optional[Book]:
        """
        Obtener libro por ISBN
        Complejidad: O(log n) - Búsqueda en BST
        """
        try:
            return self.books_tree.search(isbn)
        except Exception as e:
            print(f"Error al obtener libro: {e}")
            return None
    
    def _update_book_indexes(self, book: Book):
        """Actualizar índices cuando cambian los datos del libro"""
        # Eliminar de índices
        key_extractors = {
            'title': lambda b: b.title.lower(),
            'author': lambda b: b.author.lower(),
            'year': lambda b: str(b.year),
            'popularity': lambda b: f"{b.get_popularity_score():010.2f}_{b.isbn}"
        }
        self.book_indexes.delete(book, key_extractors)
        
        # Reinsertar con datos actualizados
        self.book_indexes.insert(book, key_extractors)
    
    # ==================== GESTIÓN DE USUARIOS ====================
    
    def add_user(self, user_id: str, name: str, email: str) -> bool:
        """
        Agregar usuario al sistema
        Complejidad: O(log n) - Búsqueda e inserción en BST
        """
        try:
            # Verificar si ya existe (O(log n))
            existing_user = self.users_tree.search(user_id)
            
            if not existing_user:
                new_user = User(user_id, name, email)
                self._add_user_to_trees(new_user)
                
                self.notifications.enqueue(f"👤 Usuario registrado: {name}")
                return True
            
            return False
            
        except Exception as e:
            print(f"Error al agregar usuario: {e}")
            return False
    
    def remove_user(self, user_id: str) -> bool:
        """
        Eliminar usuario del sistema
        Complejidad: O(log n) - Búsqueda y eliminación en BST
        """
        try:
            # Buscar usuario (O(log n))
            user = self.users_tree.search(user_id)
            
            if user and len(user.borrowed_books) == 0:
                # Eliminar de BST principal
                self.users_tree.delete(user_id)
                
                # Eliminar de índices múltiples
                key_extractors = {
                    'name': lambda u: u.name.lower(),
                    'email': lambda u: u.email.lower(),
                    'activity': lambda u: f"{u.get_activity_score():010.2f}_{u.user_id}"
                }
                self.user_indexes.delete(user, key_extractors)
                
                # Registrar operación
                self.operation_history.push({
                    'action': 'remove_user',
                    'user_id': user_id,
                    'name': user.name,
                    'timestamp': datetime.now()
                })
                
                self.notifications.enqueue(f"🗑️ Usuario eliminado: {user.name}")
                return True
            
            return False
            
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            return False
    
    def get_all_users(self) -> List[User]:
        """
        Obtener todos los usuarios ordenados por ID
        Complejidad: O(n) - Recorrido in-order del BST
        """
        try:
            return self.users_tree.get_all_sorted()
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            return []
    
    def get_users_by_activity(self) -> List[User]:
        """
        Obtener usuarios ordenados por actividad
        Complejidad: O(n) - Recorrido in-order del índice de actividad
        """
        try:
            return self.user_indexes.get_all_by_field('activity')[::-1]  # Descendente
        except Exception as e:
            print(f"Error al obtener usuarios por actividad: {e}")
            return []
    
    def get_user(self, user_id: str) -> Optional[User]:
        """
        Obtener usuario por ID
        Complejidad: O(log n) - Búsqueda en BST
        """
        try:
            return self.users_tree.search(user_id)
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            return None
    
    def search_users(self, query: str) -> List[User]:
        """
        Búsqueda de usuarios por nombre o email
        Complejidad: O(log n + k) donde k es número de resultados
        """
        try:
            results = set()
            query_lower = query.lower()
            
            # Búsqueda por nombre
            name_results = self.user_indexes.search_prefix_by_field('name', query_lower)
            results.update(name_results)
            
            # Búsqueda por email
            email_results = self.user_indexes.search_prefix_by_field('email', query_lower)
            results.update(email_results)
            
            # Búsqueda por ID exacto
            id_result = self.users_tree.search(query)
            if id_result:
                results.add(id_result)
            
            return list(results)
            
        except Exception as e:
            print(f"Error al buscar usuarios: {e}")
            return []
    
    # ==================== GESTIÓN DE PRÉSTAMOS ====================
    
    def borrow_book(self, user_id: str, isbn: str) -> Tuple[bool, str]:
        """
        Prestar libro a usuario
        Complejidad: O(log n) - Búsquedas en BST + O(1) operaciones
        """
        try:
            # Búsquedas eficientes en BST (O(log n) cada una)
            user = self.users_tree.search(user_id)
            book = self.books_tree.search(isbn)
            
            if not user:
                return False, "Usuario no encontrado"
            
            if not book:
                return False, "Libro no encontrado"
            
            if not book.is_available():
                return False, "No hay copias disponibles"
            
            if user.has_book(isbn):
                return False, "El usuario ya tiene este libro prestado"
            
            if not user.can_borrow_more():
                return False, "El usuario ha alcanzado el límite de libros"
            
            # Realizar préstamo
            if book.borrow(user_id) and user.borrow_book(isbn):
                # Agregar a préstamos activos
                loan_record = {
                    'user_id': user_id,
                    'isbn': isbn,
                    'user_name': user.name,
                    'book_title': book.title,
                    'loan_date': datetime.now()
                }
                self.active_loans.append(loan_record)
                
                # Actualizar índices (popularidad del libro, actividad del usuario)
                self._update_book_indexes(book)
                self._update_user_indexes(user)
                
                # Registrar operación
                self.operation_history.push({
                    'action': 'borrow_book',
                    'user_id': user_id,
                    'isbn': isbn,
                    'timestamp': datetime.now()
                })
                
                self.notifications.enqueue(f"📤 Préstamo: {book.title} → {user.name}")
                return True, "Libro prestado exitosamente"
            
            return False, "Error al procesar el préstamo"
            
        except Exception as e:
            print(f"Error al prestar libro: {e}")
            return False, f"Error inesperado: {e}"
    
    def return_book(self, user_id: str, isbn: str) -> Tuple[bool, str]:
        """
        Devolver libro prestado
        Complejidad: O(log n) - Búsquedas en BST + O(n) búsqueda en préstamos activos
        """
        try:
            # Búsquedas eficientes en BST
            user = self.users_tree.search(user_id)
            book = self.books_tree.search(isbn)
            
            if not user:
                return False, "Usuario no encontrado"
            
            if not book:
                return False, "Libro no encontrado"
            
            if not user.has_book(isbn):
                return False, "El usuario no tiene este libro prestado"
            
            # Realizar devolución
            if book.return_book(user_id) and user.return_book(isbn):
                # Remover de préstamos activos
                for i in range(len(self.active_loans)):
                    loan = self.active_loans.get(i)
                    if loan['user_id'] == user_id and loan['isbn'] == isbn:
                        self.active_loans.remove_at(i)
                        break
                
                # Actualizar índices
                self._update_book_indexes(book)
                self._update_user_indexes(user)
                
                # Registrar operación
                self.operation_history.push({
                    'action': 'return_book',
                    'user_id': user_id,
                    'isbn': isbn,
                    'timestamp': datetime.now()
                })
                
                self.notifications.enqueue(f"📥 Devolución: {book.title} ← {user.name}")
                return True, "Libro devuelto exitosamente"
            
            return False, "Error al procesar la devolución"
            
        except Exception as e:
            print(f"Error al devolver libro: {e}")
            return False, f"Error inesperado: {e}"
    
    def get_user_borrowed_books(self, user_id: str) -> List[Book]:
        """
        Obtener libros prestados por un usuario
        Complejidad: O(log n + k) donde k es número de libros prestados
        """
        try:
            user = self.users_tree.search(user_id)  # O(log n)
            if not user:
                return []
            
            borrowed_books = []
            for isbn in user.get_borrowed_books_list():  # O(k)
                book = self.books_tree.search(isbn)  # O(log n) por libro
                if book:
                    borrowed_books.append(book)
            
            return borrowed_books
            
        except Exception as e:
            print(f"Error al obtener libros prestados: {e}")
            return []
    
    def _update_user_indexes(self, user: User):
        """Actualizar índices cuando cambian los datos del usuario"""
        key_extractors = {
            'name': lambda u: u.name.lower(),
            'email': lambda u: u.email.lower(),
            'activity': lambda u: f"{u.get_activity_score():010.2f}_{u.user_id}"
        }
        self.user_indexes.delete(user, key_extractors)
        self.user_indexes.insert(user, key_extractors)
    
    # ==================== REPORTES Y ESTADÍSTICAS ====================
    
    def get_active_loans(self) -> List[dict]:
        """Obtener todos los préstamos activos"""
        try:
            return self.active_loans.to_list()
        except Exception as e:
            print(f"Error al obtener préstamos activos: {e}")
            return []
    
    def get_operation_history(self, limit: int = 10) -> List[dict]:
        """Obtener historial de operaciones (más recientes primero)"""
        try:
            history = self.operation_history.to_list()
            return history[:limit]
        except Exception as e:
            print(f"Error al obtener historial: {e}")
            return []
    
    def get_notifications(self) -> List[str]:
        """Obtener y limpiar notificaciones pendientes"""
        try:
            notifications = []
            while not self.notifications.is_empty():
                notifications.append(self.notifications.dequeue())
            return notifications
        except Exception as e:
            print(f"Error al obtener notificaciones: {e}")
            return []
    
    def get_most_borrowed_books(self, limit: int = 10) -> List[Tuple[Book, int]]:
        """
        Obtener libros más prestados usando índice de popularidad
        Complejidad: O(n) - Recorrido ordenado del índice
        """
        try:
            popular_books = self.get_books_by_popularity()[:limit]
            return [(book, book.get_times_borrowed()) for book in popular_books]
        except Exception as e:
            print(f"Error al obtener libros más prestados: {e}")
            return []
    
    def get_most_active_users(self, limit: int = 10) -> List[Tuple[User, float]]:
        """
        Obtener usuarios más activos usando índice de actividad
        Complejidad: O(n) - Recorrido ordenado del índice
        """
        try:
            active_users = self.get_users_by_activity()[:limit]
            return [(user, user.get_activity_score()) for user in active_users]
        except Exception as e:
            print(f"Error al obtener usuarios más activos: {e}")
            return []
    
    def get_general_statistics(self) -> dict:
        """Obtener estadísticas generales del sistema"""
        try:
            books = self.get_all_books()
            users = self.get_all_users()
            
            total_books = len(books)
            total_copies = sum(book.total_copies for book in books)
            available_copies = sum(book.available_copies for book in books)
            borrowed_copies = total_copies - available_copies
            total_users = len(users)
            active_users = len([user for user in users if len(user.borrowed_books) > 0])
            
            utilization = (borrowed_copies / total_copies * 100) if total_copies > 0 else 0
            
            return {
                'total_books': total_books,
                'total_copies': total_copies,
                'available_copies': available_copies,
                'borrowed_copies': borrowed_copies,
                'total_users': total_users,
                'active_users': active_users,
                'utilization_rate': utilization,
                'tree_sizes': {
                    'books_tree': len(self.books_tree),
                    'users_tree': len(self.users_tree)
                }
            }
        except Exception as e:
            print(f"Error al obtener estadísticas: {e}")
            return {}
    
    # ==================== API PARA FRONTEND ====================
    
    def get_books_json(self) -> List[dict]:
        """Obtener libros en formato JSON para API"""
        return [book.to_dict() for book in self.get_all_books()]
    
    def get_users_json(self) -> List[dict]:
        """Obtener usuarios en formato JSON para API"""
        return [user.to_dict() for user in self.get_all_users()]
    
    def search_books_json(self, query: str) -> List[dict]:
        """Búsqueda de libros en formato JSON"""
        books = self.search_books(query)
        return [book.to_dict() for book in books]
    
    def search_users_json(self, query: str) -> List[dict]:
        """Búsqueda de usuarios en formato JSON"""
        users = self.search_users(query)
        return [user.to_dict() for user in users]