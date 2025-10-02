from datetime import datetime
from typing import Optional
from src.data_structures.linear_structures import Stack, DynamicArray

class Book:
    def __init__(self, isbn: str, title: str, author: str, year: int, copies: int = 1):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.total_copies = copies
        self.available_copies = copies
        # ESTRUCTURA: ARREGLO DINÁMICO - Para préstamos activos del libro
        self.borrowed_by = DynamicArray()  # Usuarios que han tomado prestado el libro
        # ESTRUCTURA: PILA - Para historial de préstamos (LIFO)
        self.loan_history = Stack()  # Historial completo de préstamos
    
    def is_available(self) -> bool:
        """Verificar si hay copias disponibles"""
        return self.available_copies > 0
    
    def borrow(self, user_id: str) -> bool:
        """Prestar libro a un usuario"""
        if self.is_available():
            self.available_copies -= 1
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
        """Devolver libro de un usuario"""
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
    
    def get_current_borrowers(self):
        """Obtener lista de usuarios que actualmente tienen el libro"""
        return [self.borrowed_by.get(i)['user_id'] for i in range(len(self.borrowed_by))]
    
    def get_loan_history(self):
        """Obtener historial de préstamos (más reciente primero)"""
        return self.loan_history.to_list()
    
    def get_times_borrowed(self) -> int:
        """Obtener número de veces que se ha prestado el libro"""
        count = 0
        for record in self.loan_history.to_list():
            if record.get('action') == 'borrow':
                count += 1
        return count
    
    def __str__(self) -> str:
        status = f"({self.available_copies}/{self.total_copies} disponibles)"
        return f"{self.title} - {self.author} ({self.year}) - ISBN: {self.isbn} {status}"
    
    def __repr__(self) -> str:
        return f"Book(isbn='{self.isbn}', title='{self.title}', author='{self.author}')"