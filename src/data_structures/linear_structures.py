"""
Implementación de Estructuras de Datos Lineales
===============================================

Este módulo contiene las implementaciones de:
- Lista enlazada simple
- Pila (Stack) 
- Cola (Queue)
- Arreglo dinámico

Estas estructuras se usan para el almacenamiento y gestión de datos
en el sistema de biblioteca.
"""

class Node:
    """Nodo para lista enlazada"""
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    """
    ESTRUCTURA: LISTA ENLAZADA SIMPLE
    Uso: Almacenamiento principal de libros y usuarios
    Ventajas: Inserción/eliminación eficiente, tamaño dinámico
    """
    def __init__(self):
        self.head = None
        self.size = 0
    
    def append(self, data):
        """Agregar elemento al final"""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1
    
    def remove(self, key, key_func):
        """Eliminar elemento por clave"""
        if not self.head:
            return False
        
        if key_func(self.head.data) == key:
            self.head = self.head.next
            self.size -= 1
            return True
        
        current = self.head
        while current.next:
            if key_func(current.next.data) == key:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        return False
    
    def find(self, key, key_func):
        """Buscar elemento por clave"""
        current = self.head
        while current:
            if key_func(current.data) == key:
                return current.data
            current = current.next
        return None
    
    def to_list(self):
        """Convertir a lista Python para facilitar operaciones"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
    
    def search(self, query, search_func):
        """Buscar elementos que coincidan con criterio"""
        results = []
        current = self.head
        while current:
            if search_func(current.data, query):
                results.append(current.data)
            current = current.next
        return results
    
    def is_empty(self):
        """Verificar si la lista está vacía"""
        return self.size == 0
    
    def __len__(self):
        """Permitir usar len() con LinkedList"""
        return self.size
    
    def __str__(self):
        """Representación en string de la lista"""
        if self.is_empty():
            return "LinkedList(empty)"
        items = [str(item) for item in self.to_list()]
        return f"LinkedList({len(items)} items: {', '.join(items[:3])}{'...' if len(items) > 3 else ''})"

class Stack:
    """
    ESTRUCTURA: PILA (LIFO - Last In, First Out)
    Uso: Historial de operaciones y navegación de menús
    Ventajas: Acceso rápido al último elemento, ideal para deshacer operaciones
    """
    def __init__(self):
        self.items = []
    
    def push(self, item):
        """Agregar elemento al tope de la pila"""
        self.items.append(item)
    
    def pop(self):
        """Remover y retornar elemento del tope"""
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def peek(self):
        """Ver elemento del tope sin removerlo"""
        if not self.is_empty():
            return self.items[-1]
        return None
    
    def is_empty(self):
        """Verificar si la pila está vacía"""
        return len(self.items) == 0
    
    def size(self):
        """Obtener tamaño de la pila"""
        return len(self.items)
    
    def to_list(self):
        """Convertir a lista (del más reciente al más antiguo)"""
        return self.items[::-1]
    
    def __len__(self):
        """Permitir usar len() con Stack"""
        return len(self.items)
    
    def __str__(self):
        """Representación en string de la pila"""
        if self.is_empty():
            return "Stack(empty)"
        return f"Stack({len(self.items)} items, top: {self.peek()})"

class Queue:
    """
    ESTRUCTURA: COLA (FIFO - First In, First Out)
    Uso: Cola de préstamos pendientes y notificaciones
    Ventajas: Procesamiento justo por orden de llegada
    """
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        """Agregar elemento al final de la cola"""
        self.items.append(item)
    
    def dequeue(self):
        """Remover y retornar elemento del frente"""
        if not self.is_empty():
            return self.items.pop(0)
        return None
    
    def front(self):
        """Ver elemento del frente sin removerlo"""
        if not self.is_empty():
            return self.items[0]
        return None
    
    def is_empty(self):
        """Verificar si la cola está vacía"""
        return len(self.items) == 0
    
    def size(self):
        """Obtener tamaño de la cola"""
        return len(self.items)
    
    def to_list(self):
        """Convertir a lista"""
        return self.items.copy()
    
    def __len__(self):
        """Permitir usar len() con Queue"""
        return len(self.items)
    
    def __str__(self):
        """Representación en string de la cola"""
        if self.is_empty():
            return "Queue(empty)"
        return f"Queue({len(self.items)} items, front: {self.front()})"

class DynamicArray:
    """
    ESTRUCTURA: ARREGLO DINÁMICO
    Uso: Almacenamiento de préstamos activos y reportes
    Ventajas: Acceso aleatorio rápido, redimensionamiento automático
    """
    def __init__(self, initial_capacity=10):
        self.capacity = initial_capacity
        self.size = 0
        self.data = [None] * self.capacity
    
    def _resize(self):
        """Redimensionar arreglo cuando se llena"""
        old_data = self.data
        self.capacity *= 2
        self.data = [None] * self.capacity
        for i in range(self.size):
            self.data[i] = old_data[i]
    
    def append(self, item):
        """Agregar elemento al final"""
        if self.size >= self.capacity:
            self._resize()
        self.data[self.size] = item
        self.size += 1
    
    def get(self, index):
        """Obtener elemento por índice"""
        if 0 <= index < self.size:
            return self.data[index]
        raise IndexError("Índice fuera de rango")
    
    def set(self, index, item):
        """Establecer elemento en índice específico"""
        if 0 <= index < self.size:
            self.data[index] = item
        else:
            raise IndexError("Índice fuera de rango")
    
    def remove_at(self, index):
        """Remover elemento en índice específico"""
        if 0 <= index < self.size:
            for i in range(index, self.size - 1):
                self.data[i] = self.data[i + 1]
            self.size -= 1
            return True
        return False
    
    def find_index(self, item, key_func=None):
        """Encontrar índice de elemento"""
        for i in range(self.size):
            if key_func:
                if key_func(self.data[i]) == key_func(item):
                    return i
            else:
                if self.data[i] == item:
                    return i
        return -1
    
    def to_list(self):
        """Convertir a lista Python"""
        return [self.data[i] for i in range(self.size)]
    
    def is_empty(self):
        """Verificar si está vacío"""
        return self.size == 0
    
    def __len__(self):
        """Permitir usar len() con DynamicArray"""
        return self.size
    
    def __str__(self):
        """Representación en string del arreglo"""
        if self.is_empty():
            return "DynamicArray(empty)"
        items = self.to_list()
        return f"DynamicArray({len(items)} items, capacity: {self.capacity})"