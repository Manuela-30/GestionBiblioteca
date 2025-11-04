from datetime import datetime
from typing import Optional, List
from src.data_structures.linear_structures import Stack, DynamicArray

class Book:
    """
    MODELO DE LIBRO CON INTEGRACIÓN DE ESTRUCTURAS DE DATOS
    =======================================================
    
    Utiliza estructuras lineales para:
    - Stack: Historial de préstamos (LIFO - último préstamo primero)
    - DynamicArray: Lista de usuarios que actualmente tienen el libro
    
    JUSTIFICACIÓN:
    - Stack para historial: Acceso rápido a préstamos recientes O(1)
    - DynamicArray para préstamos activos: Acceso aleatorio eficiente O(1)
    """
    
    def __init__(self, isbn: str, title: str, author: str, year: int, copies: int = 1):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.total_copies = copies
        self.available_copies = copies
        
        # ESTRUCTURA LINEAL: ARREGLO DINÁMICO para préstamos activos
        # Permite acceso rápido por índice y redimensionamiento automático
        self.borrowed_by = DynamicArray()  # Usuarios que tienen el libro prestado
        
        # ESTRUCTURA LINEAL: PILA para historial de préstamos
        # LIFO - Los préstamos más recientes son más relevantes
        self.loan_history = Stack()  # Historial completo de operaciones
        
        self.created_at = datetime.now()
    
    def is_available(self) -> bool:
        """Verificar si hay copias disponibles"""
        return self.available_copies > 0
    
    def borrow(self, user_id: str) -> bool:
        """
        Prestar libro a un usuario
        Complejidad: O(1) - Inserción al final del arreglo dinámico
        """
        if self.is_available():
            self.available_copies -= 1
            
            # Registro de préstamo
            loan_record = {
                'user_id': user_id,
                'borrowed_date': datetime.now(),
                'action': 'borrow'
            }
            
            # Agregar a préstamos activos (Arreglo Dinámico)
            self.borrowed_by.append(loan_record)
            
            # Agregar al historial (Pila)
            self.loan_history.push(loan_record)
            
            return True
        return False
    
    def return_book(self, user_id: str) -> bool:
        """
        Devolver libro de un usuario
        Complejidad: O(n) - Búsqueda en arreglo dinámico
        """
        # Buscar en arreglo dinámico de préstamos activos
        for i in range(len(self.borrowed_by)):
            borrow_record = self.borrowed_by.get(i)
            if borrow_record['user_id'] == user_id:
                self.available_copies += 1
                self.borrowed_by.remove_at(i)
                
                # Agregar registro de devolución al historial
                return_record = {
                    'user_id': user_id,
                    'returned_date': datetime.now(),
                    'action': 'return'
                }
                self.loan_history.push(return_record)
                return True
        return False
    
    def get_current_borrowers(self) -> List[str]:
        """Obtener lista de usuarios que actualmente tienen el libro"""
        return [self.borrowed_by.get(i)['user_id'] for i in range(len(self.borrowed_by))]
    
    def get_loan_history(self) -> List[dict]:
        """
        Obtener historial de préstamos (más reciente primero)
        Complejidad: O(n) - Conversión de pila a lista
        """
        return self.loan_history.to_list()
    
    def get_times_borrowed(self) -> int:
        """
        Obtener número de veces que se ha prestado el libro
        Complejidad: O(n) - Recorrido de historial
        """
        count = 0
        for record in self.loan_history.to_list():
            if record.get('action') == 'borrow':
                count += 1
        return count
    
    def get_popularity_score(self) -> float:
        """
        Calcular puntuación de popularidad basada en préstamos
        Útil para recomendaciones y estadísticas
        """
        times_borrowed = self.get_times_borrowed()
        if times_borrowed == 0:
            return 0.0
        
        # Factor de popularidad: préstamos / copias totales
        base_score = times_borrowed / self.total_copies
        
        # Bonus por préstamos recientes (últimos 10)
        recent_loans = 0
        history = self.loan_history.to_list()[:10]
        for record in history:
            if record.get('action') == 'borrow':
                recent_loans += 1
        
        recent_bonus = recent_loans * 0.1
        return base_score + recent_bonus
    
    def to_dict(self) -> dict:
        """Convertir a diccionario para API JSON"""
        return {
            'isbn': self.isbn,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'total_copies': self.total_copies,
            'available_copies': self.available_copies,
            'times_borrowed': self.get_times_borrowed(),
            'popularity_score': self.get_popularity_score(),
            'current_borrowers': self.get_current_borrowers(),
            'created_at': self.created_at.isoformat()
        }
    
    def __str__(self) -> str:
        status = f"({self.available_copies}/{self.total_copies} disponibles)"
        return f"{self.title} - {self.author} ({self.year}) - ISBN: {self.isbn} {status}"
    
    def __repr__(self) -> str:
        return f"Book(isbn='{self.isbn}', title='{self.title}', author='{self.author}')"