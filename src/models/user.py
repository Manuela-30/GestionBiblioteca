from datetime import datetime
from typing import List
from src.data_structures.linear_structures import LinkedList, Queue

class User:
    def __init__(self, user_id: str, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        # ESTRUCTURA: LISTA ENLAZADA - Para libros prestados actualmente
        self.borrowed_books = LinkedList()  # ISBNs de libros prestados
        # ESTRUCTURA: COLA - Para solicitudes de préstamos pendientes
        self.pending_requests = Queue()  # Cola de solicitudes pendientes
        self.registration_date = datetime.now()
    
    def borrow_book(self, isbn: str) -> None:
        """Agregar libro a la lista de prestados"""
        if not self.has_book(isbn):
            self.borrowed_books.append(isbn)
    
    def return_book(self, isbn: str) -> bool:
        """Remover libro de la lista de prestados"""
        if self.has_book(isbn):
            return self.borrowed_books.remove(isbn, lambda x: x)
        return False
    
    def has_book(self, isbn: str) -> bool:
        """Verificar si el usuario tiene un libro específico"""
        return self.borrowed_books.find(isbn, lambda x: x) is not None
    
    def add_pending_request(self, isbn: str):
        """Agregar solicitud de préstamo a la cola"""
        request = {
            'isbn': isbn,
            'request_date': datetime.now()
        }
        self.pending_requests.enqueue(request)
    
    def get_next_pending_request(self):
        """Obtener siguiente solicitud pendiente"""
        return self.pending_requests.dequeue()
    
    def get_borrowed_books_list(self):
        """Obtener lista de libros prestados"""
        return self.borrowed_books.to_list()
    
    def get_pending_requests_list(self):
        """Obtener lista de solicitudes pendientes"""
        return self.pending_requests.to_list()
    
    def get_borrowed_count(self) -> int:
        """Obtener número de libros prestados"""
        return len(self.borrowed_books)
    
    def __str__(self) -> str:
        books_count = len(self.borrowed_books)
        return f"{self.name} (ID: {self.user_id}) - {books_count} libros prestados"
    
    def __repr__(self) -> str:
        return f"User(user_id='{self.user_id}', name='{self.name}', email='{self.email}')"