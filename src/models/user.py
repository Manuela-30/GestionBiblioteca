from datetime import datetime
from typing import List, Dict
from src.data_structures.linear_structures import LinkedList, Queue

class User:
    """
    MODELO DE USUARIO CON INTEGRACIÓN DE ESTRUCTURAS DE DATOS
    =========================================================
    
    Utiliza estructuras lineales para:
    - LinkedList: Libros prestados actualmente (inserción/eliminación eficiente)
    - Queue: Solicitudes de préstamos pendientes (FIFO - justo por orden de llegada)
    
    JUSTIFICACIÓN:
    - LinkedList para préstamos: Inserción/eliminación O(1) al inicio
    - Queue para solicitudes: Procesamiento justo FIFO O(1) enqueue/dequeue
    """
    
    def __init__(self, user_id: str, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        
        # ESTRUCTURA LINEAL: LISTA ENLAZADA para libros prestados
        # Permite inserción/eliminación eficiente sin reorganizar elementos
        self.borrowed_books = LinkedList()  # ISBNs de libros prestados
        
        # ESTRUCTURA LINEAL: COLA para solicitudes pendientes
        # FIFO - Las solicitudes se procesan por orden de llegada
        self.pending_requests = Queue()  # Cola de solicitudes de préstamo
        
        self.registration_date = datetime.now()
        self.last_activity = datetime.now()
    
    def borrow_book(self, isbn: str) -> bool:
        """
        Agregar libro a la lista de prestados
        Complejidad: O(n) - Verificación de duplicados + O(1) inserción
        """
        if not self.has_book(isbn):
            self.borrowed_books.append(isbn)
            self.last_activity = datetime.now()
            return True
        return False
    
    def return_book(self, isbn: str) -> bool:
        """
        Remover libro de la lista de prestados
        Complejidad: O(n) - Búsqueda y eliminación en lista enlazada
        """
        if self.has_book(isbn):
            success = self.borrowed_books.remove(isbn, lambda x: x)
            if success:
                self.last_activity = datetime.now()
            return success
        return False
    
    def has_book(self, isbn: str) -> bool:
        """
        Verificar si el usuario tiene un libro específico
        Complejidad: O(n) - Búsqueda en lista enlazada
        """
        return self.borrowed_books.find(isbn, lambda x: x) is not None
    
    def add_pending_request(self, isbn: str, priority: str = 'normal') -> None:
        """
        Agregar solicitud de préstamo a la cola
        Complejidad: O(1) - Inserción al final de la cola
        """
        request = {
            'isbn': isbn,
            'request_date': datetime.now(),
            'priority': priority,
            'user_id': self.user_id
        }
        self.pending_requests.enqueue(request)
    
    def get_next_pending_request(self) -> Dict:
        """
        Obtener siguiente solicitud pendiente (FIFO)
        Complejidad: O(1) - Eliminación del frente de la cola
        """
        return self.pending_requests.dequeue()
    
    def get_borrowed_books_list(self) -> List[str]:
        """
        Obtener lista de libros prestados
        Complejidad: O(n) - Conversión de lista enlazada a lista Python
        """
        return self.borrowed_books.to_list()
    
    def get_pending_requests_list(self) -> List[Dict]:
        """
        Obtener lista de solicitudes pendientes sin removerlas
        Complejidad: O(n) - Conversión de cola a lista
        """
        return self.pending_requests.to_list()
    
    def get_borrowed_count(self) -> int:
        """
        Obtener número de libros prestados
        Complejidad: O(1) - Acceso directo al tamaño
        """
        return len(self.borrowed_books)
    
    def get_activity_score(self) -> float:
        """
        Calcular puntuación de actividad del usuario
        Basada en número de libros prestados y solicitudes pendientes
        """
        borrowed_score = len(self.borrowed_books) * 2.0
        pending_score = len(self.pending_requests) * 0.5
        
        # Bonus por actividad reciente (últimos 30 días)
        days_since_activity = (datetime.now() - self.last_activity).days
        recency_bonus = max(0, 30 - days_since_activity) * 0.1
        
        return borrowed_score + pending_score + recency_bonus
    
    def can_borrow_more(self, max_books: int = 5) -> bool:
        """Verificar si el usuario puede pedir más libros prestados"""
        return len(self.borrowed_books) < max_books
    
    def to_dict(self) -> dict:
        """Convertir a diccionario para API JSON"""
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'borrowed_count': self.get_borrowed_count(),
            'borrowed_books': self.get_borrowed_books_list(),
            'pending_requests': len(self.pending_requests),
            'activity_score': self.get_activity_score(),
            'registration_date': self.registration_date.isoformat(),
            'last_activity': self.last_activity.isoformat(),
            'can_borrow_more': self.can_borrow_more()
        }
    
    def __str__(self) -> str:
        books_count = len(self.borrowed_books)
        return f"{self.name} (ID: {self.user_id}) - {books_count} libros prestados"
    
    def __repr__(self) -> str:
        return f"User(user_id='{self.user_id}', name='{self.name}', email='{self.email}')"