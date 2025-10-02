from datetime import datetime
from typing import Dict, List, Optional, Tuple
from src.models.book import Book
from src.models.user import User
from src.data_structures.linear_structures import LinkedList, Stack, Queue, DynamicArray

class LibraryService:
    def __init__(self):
        # ESTRUCTURA: LISTA ENLAZADA - Para catálogo de libros
        self.books_catalog = LinkedList()
        # ESTRUCTURA: LISTA ENLAZADA - Para registro de usuarios  
        self.users_registry = LinkedList()
        # ESTRUCTURA: PILA - Para historial de operaciones del sistema
        self.operation_history = Stack()
        # ESTRUCTURA: COLA - Para notificaciones del sistema
        self.notifications = Queue()
        # ESTRUCTURA: ARREGLO DINÁMICO - Para préstamos activos
        self.active_loans = DynamicArray()
        
        self._load_sample_data()
    
    def _load_sample_data(self):
        """Carga datos de ejemplo para demostrar el sistema"""
        # Libros de ejemplo
        sample_books = [
            Book("978-0-7432-7356-5", "El Código Da Vinci", "Dan Brown", 2003, 3),
            Book("978-84-376-0494-7", "Cien Años de Soledad", "Gabriel García Márquez", 1967, 2),
            Book("978-0-06-112008-4", "Matar a un Ruiseñor", "Harper Lee", 1960, 2),
            Book("978-0-452-28423-4", "1984", "George Orwell", 1949, 4),
            Book("978-0-7432-4722-1", "El Gran Gatsby", "F. Scott Fitzgerald", 1925, 1),
        ]
        
        for book in sample_books:
            self.books_catalog.append(book)
            # Registrar operación en historial
            self.operation_history.push({
                'action': 'add_book',
                'isbn': book.isbn,
                'title': book.title,
                'timestamp': datetime.now()
            })
        
        # Usuarios de ejemplo
        sample_users = [
            User("U001", "Ana García", "ana.garcia@email.com"),
            User("U002", "Carlos López", "carlos.lopez@email.com"),
            User("U003", "María Rodríguez", "maria.rodriguez@email.com"),
        ]
        
        for user in sample_users:
            self.users_registry.append(user)
            # Registrar operación en historial
            self.operation_history.push({
                'action': 'add_user',
                'user_id': user.user_id,
                'name': user.name,
                'timestamp': datetime.now()
            })
    
    # ==================== GESTIÓN DE LIBROS ====================
    
    def add_book(self, isbn: str, title: str, author: str, year: int, copies: int = 1) -> bool:
        """Agregar libro al catálogo"""
        try:
            existing_book = self.books_catalog.find(isbn, lambda book: book.isbn)
            
            if existing_book:
                # Si el libro ya existe, aumentar copias
                existing_book.total_copies += copies
                existing_book.available_copies += copies
            else:
                # Crear nuevo libro y agregarlo a la lista enlazada
                new_book = Book(isbn, title, author, year, copies)
                self.books_catalog.append(new_book)
            
            # Registrar operación en pila de historial
            self.operation_history.push({
                'action': 'add_book',
                'isbn': isbn,
                'title': title,
                'timestamp': datetime.now()
            })
            
            # Agregar notificación a la cola
            self.notifications.enqueue(f"📚 Libro agregado: {title}")
            return True
        except Exception as e:
            print(f"Error al agregar libro: {e}")
            return False
    
    def remove_book(self, isbn: str) -> bool:
        """Eliminar libro del catálogo"""
        try:
            book = self.books_catalog.find(isbn, lambda book: book.isbn)
            if book and book.available_copies == book.total_copies:
                self.books_catalog.remove(isbn, lambda book: book.isbn)
                
                # Registrar en historial
                self.operation_history.push({
                    'action': 'remove_book',
                    'isbn': isbn,
                    'title': book.title,
                    'timestamp': datetime.now()
                })
                
                # Notificación
                self.notifications.enqueue(f"🗑️ Libro eliminado: {book.title}")
                return True
            return False
        except Exception as e:
            print(f"Error al eliminar libro: {e}")
            return False
    
    def search_books(self, query: str) -> List[Book]:
        """Buscar libros por título, autor o ISBN"""
        try:
            def search_criteria(book, query_term):
                query_term = query_term.lower()
                return (query_term in book.title.lower() or 
                       query_term in book.author.lower() or 
                       query_term in book.isbn.lower())
            
            return self.books_catalog.search(query, search_criteria)
        except Exception as e:
            print(f"Error al buscar libros: {e}")
            return []
    
    def get_all_books(self) -> List[Book]:
        """Obtener todos los libros"""
        try:
            return self.books_catalog.to_list()
        except Exception as e:
            print(f"Error al obtener libros: {e}")
            return []
    
    def get_book(self, isbn: str) -> Optional[Book]:
        """Obtener libro por ISBN"""
        try:
            return self.books_catalog.find(isbn, lambda book: book.isbn)
        except Exception as e:
            print(f"Error al obtener libro: {e}")
            return None
    
    # ==================== GESTIÓN DE USUARIOS ====================
    
    def add_user(self, user_id: str, name: str, email: str) -> bool:
        """Agregar usuario al sistema"""
        try:
            existing_user = self.users_registry.find(user_id, lambda user: user.user_id)
            if not existing_user:
                new_user = User(user_id, name, email)
                self.users_registry.append(new_user)
                
                # Registrar en historial
                self.operation_history.push({
                    'action': 'add_user',
                    'user_id': user_id,
                    'name': name,
                    'timestamp': datetime.now()
                })
                
                # Notificación
                self.notifications.enqueue(f"👤 Usuario registrado: {name}")
                return True
            return False
        except Exception as e:
            print(f"Error al agregar usuario: {e}")
            return False
    
    def remove_user(self, user_id: str) -> bool:
        """Eliminar usuario del sistema"""
        try:
            user = self.users_registry.find(user_id, lambda user: user.user_id)
            if user and len(user.borrowed_books) == 0:
                self.users_registry.remove(user_id, lambda user: user.user_id)
                
                # Registrar en historial
                self.operation_history.push({
                    'action': 'remove_user',
                    'user_id': user_id,
                    'name': user.name,
                    'timestamp': datetime.now()
                })
                
                # Notificación
                self.notifications.enqueue(f"🗑️ Usuario eliminado: {user.name}")
                return True
            return False
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            return False
    
    def get_all_users(self) -> List[User]:
        """Obtener todos los usuarios"""
        try:
            return self.users_registry.to_list()
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            return []
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Obtener usuario por ID"""
        try:
            return self.users_registry.find(user_id, lambda user: user.user_id)
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            return None
    
    # ==================== GESTIÓN DE PRÉSTAMOS ====================
    
    def borrow_book(self, user_id: str, isbn: str) -> Tuple[bool, str]:
        """Prestar libro a usuario"""
        try:
            user = self.users_registry.find(user_id, lambda user: user.user_id)
            book = self.books_catalog.find(isbn, lambda book: book.isbn)
            
            if not user:
                return False, "Usuario no encontrado"
            
            if not book:
                return False, "Libro no encontrado"
            
            if not book.is_available():
                return False, "No hay copias disponibles"
            
            if user.has_book(isbn):
                return False, "El usuario ya tiene este libro prestado"
            
            if book.borrow(user_id) and user.borrow_book(isbn):
                # Agregar préstamo al arreglo dinámico de préstamos activos
                loan_record = {
                    'user_id': user_id,
                    'isbn': isbn,
                    'user_name': user.name,
                    'book_title': book.title,
                    'loan_date': datetime.now()
                }
                self.active_loans.append(loan_record)
                
                # Registrar en historial
                self.operation_history.push({
                    'action': 'borrow_book',
                    'user_id': user_id,
                    'isbn': isbn,
                    'timestamp': datetime.now()
                })
                
                # Notificación
                self.notifications.enqueue(f"📤 Préstamo: {book.title} → {user.name}")
                return True, "Libro prestado exitosamente"
            
            return False, "Error al procesar el préstamo"
        except Exception as e:
            print(f"Error al prestar libro: {e}")
            return False, f"Error inesperado: {e}"
    
    def return_book(self, user_id: str, isbn: str) -> Tuple[bool, str]:
        """Devolver libro prestado"""
        try:
            user = self.users_registry.find(user_id, lambda user: user.user_id)
            book = self.books_catalog.find(isbn, lambda book: book.isbn)
            
            if not user:
                return False, "Usuario no encontrado"
            
            if not book:
                return False, "Libro no encontrado"
            
            if not user.has_book(isbn):
                return False, "El usuario no tiene este libro prestado"
            
            if book.return_book(user_id) and user.return_book(isbn):
                # Remover del arreglo de préstamos activos
                for i in range(len(self.active_loans)):
                    loan = self.active_loans.get(i)
                    if loan['user_id'] == user_id and loan['isbn'] == isbn:
                        self.active_loans.remove_at(i)
                        break
                
                # Registrar en historial
                self.operation_history.push({
                    'action': 'return_book',
                    'user_id': user_id,
                    'isbn': isbn,
                    'timestamp': datetime.now()
                })
                
                # Notificación
                self.notifications.enqueue(f"📥 Devolución: {book.title} ← {user.name}")
                return True, "Libro devuelto exitosamente"
            
            return False, "Error al procesar la devolución"
        except Exception as e:
            print(f"Error al devolver libro: {e}")
            return False, f"Error inesperado: {e}"
    
    def get_user_borrowed_books(self, user_id: str) -> List[Book]:
        """Obtener libros prestados por un usuario"""
        try:
            user = self.users_registry.find(user_id, lambda user: user.user_id)
            if not user:
                return []
            
            borrowed_books = []
            for isbn in user.get_borrowed_books_list():
                book = self.books_catalog.find(isbn, lambda book: book.isbn)
                if book:
                    borrowed_books.append(book)
            return borrowed_books
        except Exception as e:
            print(f"Error al obtener libros prestados: {e}")
            return []
    
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
        """Obtener libros más prestados"""
        try:
            books = self.get_all_books()
            borrowed_books = [(book, book.get_times_borrowed()) for book in books]
            borrowed_books.sort(key=lambda x: x[1], reverse=True)
            return borrowed_books[:limit]
        except Exception as e:
            print(f"Error al obtener libros más prestados: {e}")
            return []
    
    def get_most_active_users(self, limit: int = 10) -> List[Tuple[User, int]]:
        """Obtener usuarios más activos"""
        try:
            users = self.get_all_users()
            active_users = [(user, user.get_borrowed_count()) for user in users]
            active_users.sort(key=lambda x: x[1], reverse=True)
            return active_users[:limit]
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
                'utilization_rate': utilization
            }
        except Exception as e:
            print(f"Error al obtener estadísticas: {e}")
            return {}