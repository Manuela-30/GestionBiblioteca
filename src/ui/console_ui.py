from typing import List
from src.services.library_service import LibraryService
from src.models.book import Book
from src.models.user import User

class ConsoleUI:
    def __init__(self):
        self.library_service = LibraryService()
    
    def clear_screen(self):
        # Simular limpieza de pantalla con líneas en blanco
        print('\n' * 50)
    
    def pause(self):
        input("\nPresiona Enter para continuar...")
    
    def print_header(self, title: str):
        print("=" * 60)
        print(f" {title.center(58)} ")
        print("=" * 60)
    
    def print_books(self, books: List[Book], title: str = "Libros"):
        self.print_header(title)
        if not books:
            print("No se encontraron libros.")
        else:
            for i, book in enumerate(books, 1):
                print(f"{i:2d}. {book}")
        print()
    
    def print_users(self, users: List[User], title: str = "Usuarios"):
        self.print_header(title)
        if not users:
            print("No se encontraron usuarios.")
        else:
            for i, user in enumerate(users, 1):
                print(f"{i:2d}. {user}")
        print()
    
    def get_input(self, prompt: str, required: bool = True) -> str:
        while True:
            value = input(prompt).strip()
            if value or not required:
                return value
            print("Este campo es obligatorio. Por favor, ingresa un valor.")
    
    def get_int_input(self, prompt: str, min_val: int = 0) -> int:
        while True:
            try:
                value = int(input(prompt))
                if value >= min_val:
                    return value
                print(f"El valor debe ser mayor o igual a {min_val}")
            except ValueError:
                print("Por favor, ingresa un número válido.")
    
    def show_main_menu(self):
        self.clear_screen()
        self.print_header("📚 SISTEMA DE GESTIÓN DE BIBLIOTECA 📚")
        print("📖 1. Gestión de Libros")
        print("👥 2. Gestión de Usuarios")
        print("🔄 3. Gestión de Préstamos")
        print("📊 4. Reportes")
        print("🚪 5. Salir")
        print()
        return self.get_input("Selecciona una opción (1-5): ")
    
    def show_books_menu(self):
        while True:
            self.clear_screen()
            self.print_header("📖 GESTIÓN DE LIBROS 📖")
            print("📚 1. Ver todos los libros")
            print("🔍 2. Buscar libros")
            print("➕ 3. Agregar libro")
            print("🗑️  4. Eliminar libro")
            print("⬅️  5. Volver al menú principal")
            print()
            
            option = self.get_input("Selecciona una opción (1-5): ")
            
            if option == "1":
                self.show_all_books()
            elif option == "2":
                self.search_books()
            elif option == "3":
                self.add_book()
            elif option == "4":
                self.remove_book()
            elif option == "5":
                break
            else:
                print("Opción no válida.")
                self.pause()
    
    def show_all_books(self):
        self.clear_screen()
        books = self.library_service.get_all_books()
        self.print_books(books, "TODOS LOS LIBROS")
        self.pause()
    
    def search_books(self):
        self.clear_screen()
        self.print_header("🔍 BUSCAR LIBROS 🔍")
        query = self.get_input("Ingresa título, autor o ISBN: ")
        books = self.library_service.search_books(query)
        print()
        self.print_books(books, f"🔍 RESULTADOS DE BÚSQUEDA: '{query}' 🔍")
        self.pause()
    
    def add_book(self):
        self.clear_screen()
        self.print_header("➕ AGREGAR LIBRO ➕")
        
        isbn = self.get_input("ISBN: ")
        title = self.get_input("Título: ")
        author = self.get_input("Autor: ")
        year = self.get_int_input("Año de publicación: ", 1000)
        copies = self.get_int_input("Número de copias: ", 1)
        
        if self.library_service.add_book(isbn, title, author, year, copies):
            print(f"\n✅ Libro '{title}' agregado exitosamente.")
        else:
            print(f"\n❌ Error al agregar el libro.")
        
        self.pause()
    
    def remove_book(self):
        self.clear_screen()
        books = self.library_service.get_all_books()
        self.print_books(books, "🗑️ ELIMINAR LIBRO 🗑️")
        
        if not books:
            self.pause()
            return
        
        isbn = self.get_input("Ingresa el ISBN del libro a eliminar: ")
        book = self.library_service.get_book(isbn)
        
        if not book:
            print("❌ Libro no encontrado.")
        elif book.available_copies != book.total_copies:
            print("⚠️ No se puede eliminar el libro porque tiene copias prestadas.")
        else:
            confirm = self.get_input(f"¿Estás seguro de eliminar '{book.title}'? (s/N): ")
            if confirm.lower() == 's':
                if self.library_service.remove_book(isbn):
                    print("✅ Libro eliminado exitosamente.")
                else:
                    print("❌ Error al eliminar el libro.")
            else:
                print("🚫 Operación cancelada.")
        
        self.pause()
    
    def show_users_menu(self):
        while True:
            self.clear_screen()
            self.print_header("👥 GESTIÓN DE USUARIOS 👥")
            print("👤 1. Ver todos los usuarios")
            print("➕ 2. Agregar usuario")
            print("🗑️  3. Eliminar usuario")
            print("📚 4. Ver libros prestados por usuario")
            print("⬅️  5. Volver al menú principal")
            print()
            
            option = self.get_input("Selecciona una opción (1-5): ")
            
            if option == "1":
                self.show_all_users()
            elif option == "2":
                self.add_user()
            elif option == "3":
                self.remove_user()
            elif option == "4":
                self.show_user_books()
            elif option == "5":
                break
            else:
                print("Opción no válida.")
                self.pause()
    
    def show_all_users(self):
        self.clear_screen()
        users = self.library_service.get_all_users()
        self.print_users(users, "👥 TODOS LOS USUARIOS 👥")
        self.pause()
    
    def add_user(self):
        self.clear_screen()
        self.print_header("➕ AGREGAR USUARIO ➕")
        
        user_id = self.get_input("ID de usuario: ")
        name = self.get_input("Nombre completo: ")
        email = self.get_input("Email: ")
        
        if self.library_service.add_user(user_id, name, email):
            print(f"\n✅ Usuario '{name}' agregado exitosamente.")
        else:
            print(f"\n❌ Error: Ya existe un usuario con ID '{user_id}'.")
        
        self.pause()
    
    def remove_user(self):
        self.clear_screen()
        users = self.library_service.get_all_users()
        self.print_users(users, "🗑️ ELIMINAR USUARIO 🗑️")
        
        if not users:
            self.pause()
            return
        
        user_id = self.get_input("Ingresa el ID del usuario a eliminar: ")
        user = self.library_service.get_user(user_id)
        
        if not user:
            print("❌ Usuario no encontrado.")
        elif len(user.borrowed_books) > 0:
            print("⚠️ No se puede eliminar el usuario porque tiene libros prestados.")
        else:
            confirm = self.get_input(f"¿Estás seguro de eliminar a '{user.name}'? (s/N): ")
            if confirm.lower() == 's':
                if self.library_service.remove_user(user_id):
                    print("✅ Usuario eliminado exitosamente.")
                else:
                    print("❌ Error al eliminar el usuario.")
            else:
                print("🚫 Operación cancelada.")
        
        self.pause()
    
    def show_user_books(self):
        self.clear_screen()
        self.print_header("📚 LIBROS PRESTADOS POR USUARIO 📚")
        
        user_id = self.get_input("Ingresa el ID del usuario: ")
        user = self.library_service.get_user(user_id)
        
        if not user:
            print("❌ Usuario no encontrado.")
        else:
            borrowed_books = self.library_service.get_user_borrowed_books(user_id)
            print(f"\n👤 Usuario: {user.name}")
            self.print_books(borrowed_books, f"📚 LIBROS PRESTADOS A {user.name} 📚")
        
        self.pause()
    
    def show_loans_menu(self):
        while True:
            self.clear_screen()
            self.print_header("🔄 GESTIÓN DE PRÉSTAMOS 🔄")
            print("📤 1. Prestar libro")
            print("📥 2. Devolver libro")
            print("📋 3. Ver préstamos activos")
            print("⬅️  4. Volver al menú principal")
            print()
            
            option = self.get_input("Selecciona una opción (1-4): ")
            
            if option == "1":
                self.borrow_book()
            elif option == "2":
                self.return_book()
            elif option == "3":
                self.show_active_loans()
            elif option == "4":
                break
            else:
                print("Opción no válida.")
                self.pause()
    
    def borrow_book(self):
        self.clear_screen()
        self.print_header("📤 PRESTAR LIBRO 📤")
        
        # Mostrar libros disponibles
        available_books = [book for book in self.library_service.get_all_books() if book.is_available()]
        if not available_books:
            print("❌ No hay libros disponibles para préstamo.")
            self.pause()
            return
        
        self.print_books(available_books, "✅ LIBROS DISPONIBLES ✅")
        
        user_id = self.get_input("ID del usuario: ")
        isbn = self.get_input("ISBN del libro: ")
        
        success, message = self.library_service.borrow_book(user_id, isbn)
        
        if success:
            print(f"\n✅ {message}")
        else:
            print(f"\n❌ {message}")
        
        self.pause()
    
    def return_book(self):
        self.clear_screen()
        self.print_header("📥 DEVOLVER LIBRO 📥")
        
        user_id = self.get_input("ID del usuario: ")
        user = self.library_service.get_user(user_id)
        
        if not user:
            print("❌ Usuario no encontrado.")
            self.pause()
            return
        
        borrowed_books = self.library_service.get_user_borrowed_books(user_id)
        if not borrowed_books:
            print(f"ℹ️ El usuario {user.name} no tiene libros prestados.")
            self.pause()
            return
        
        self.print_books(borrowed_books, f"📚 LIBROS PRESTADOS A {user.name} 📚")
        
        isbn = self.get_input("ISBN del libro a devolver: ")
        
        success, message = self.library_service.return_book(user_id, isbn)
        
        if success:
            print(f"\n✅ {message}")
        else:
            print(f"\n❌ {message}")
        
        self.pause()
    
    def show_active_loans(self):
        self.clear_screen()
        self.print_header("📋 PRÉSTAMOS ACTIVOS 📋")
        
        users = self.library_service.get_all_users()
        active_loans = []
        
        for user in users:
            if user.borrowed_books:
                borrowed_books = self.library_service.get_user_borrowed_books(user.user_id)
                for book in borrowed_books:
                    active_loans.append(f"{user.name} ({user.user_id}) - {book.title}")
        
        if not active_loans:
            print("ℹ️ No hay préstamos activos.")
        else:
            for i, loan in enumerate(active_loans, 1):
                print(f"📖 {i:2d}. {loan}")
        
        print()
        self.pause()
    
    def show_reports_menu(self):
        while True:
            self.clear_screen()
            self.print_header("📊 REPORTES 📊")
            print("🏆 1. Libros más prestados")
            print("⭐ 2. Usuarios más activos")
            print("📈 3. Estadísticas generales")
            print("📋 4. Historial de operaciones")
            print("🔔 5. Ver notificaciones")
            print("⬅️  6. Volver al menú principal")
            print()
            
            option = self.get_input("Selecciona una opción (1-6): ")
            
            if option == "1":
                self.show_most_borrowed_books()
            elif option == "2":
                self.show_most_active_users()
            elif option == "3":
                self.show_general_stats()
            elif option == "4":
                self.show_operation_history()
            elif option == "5":
                self.show_notifications()
            elif option == "6":
                break
            else:
                print("Opción no válida.")
                self.pause()
    
    def show_most_borrowed_books(self):
        self.clear_screen()
        self.print_header("🏆 LIBROS MÁS PRESTADOS 🏆")
        
        books = self.library_service.get_all_books()
        borrowed_books = [(book, len(book.borrowed_by)) for book in books if book.borrowed_by]
        borrowed_books.sort(key=lambda x: x[1], reverse=True)
        
        if not borrowed_books:
            print("ℹ️ No hay historial de préstamos.")
        else:
            for i, (book, count) in enumerate(borrowed_books[:10], 1):
                print(f"📚 {i:2d}. {book.title} - {count} préstamos")
        
        print()
        self.pause()
    
    def show_most_active_users(self):
        self.clear_screen()
        self.print_header("⭐ USUARIOS MÁS ACTIVOS ⭐")
        
        users = self.library_service.get_all_users()
        active_users = [(user, len(user.borrowed_books)) for user in users if user.borrowed_books]
        active_users.sort(key=lambda x: x[1], reverse=True)
        
        if not active_users:
            print("ℹ️ No hay usuarios con préstamos activos.")
        else:
            for i, (user, count) in enumerate(active_users, 1):
                print(f"👤 {i:2d}. {user.name} - {count} libros prestados")
        
        print()
        self.pause()
    
    def show_general_stats(self):
        self.clear_screen()
        self.print_header("📈 ESTADÍSTICAS GENERALES 📈")
        
        books = self.library_service.get_all_books()
        users = self.library_service.get_all_users()
        
        total_books = len(books)
        total_copies = sum(book.total_copies for book in books)
        available_copies = sum(book.available_copies for book in books)
        borrowed_copies = total_copies - available_copies
        total_users = len(users)
        active_users = len([user for user in users if user.borrowed_books])
        
        print(f"📚 Total de libros únicos: {total_books}")
        print(f"📖 Total de copias: {total_copies}")
        print(f"✅ Copias disponibles: {available_copies}")
        print(f"📤 Copias prestadas: {borrowed_copies}")
        print(f"👥 Total de usuarios: {total_users}")
        print(f"⭐ Usuarios con préstamos activos: {active_users}")
        
        if total_copies > 0:
            utilization = (borrowed_copies / total_copies) * 100
            print(f"📊 Tasa de utilización: {utilization:.1f}%")
        
        print()
        self.pause()
    
    def show_operation_history(self):
        self.clear_screen()
        self.print_header("📋 HISTORIAL DE OPERACIONES 📋")
        
        history = self.library_service.get_operation_history(15)
        
        if not history:
            print("ℹ️ No hay operaciones registradas.")
        else:
            print("🕒 Últimas 15 operaciones (más reciente primero):\n")
            for i, operation in enumerate(history, 1):
                action_icons = {
                    'add_book': '📚➕',
                    'remove_book': '📚🗑️',
                    'add_user': '👤➕',
                    'remove_user': '👤🗑️',
                    'borrow_book': '📤',
                    'return_book': '📥'
                }
                
                icon = action_icons.get(operation['action'], '📝')
                timestamp = operation['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
                
                if operation['action'] in ['add_book', 'remove_book']:
                    detail = f"ISBN: {operation['isbn']}"
                    if 'title' in operation:
                        detail += f" - {operation['title']}"
                elif operation['action'] in ['add_user', 'remove_user']:
                    detail = f"Usuario: {operation['user_id']}"
                    if 'name' in operation:
                        detail += f" - {operation['name']}"
                elif operation['action'] in ['borrow_book', 'return_book']:
                    detail = f"Usuario: {operation['user_id']}, ISBN: {operation['isbn']}"
                else:
                    detail = "Operación del sistema"
                
                print(f"{icon} {i:2d}. [{timestamp}] {detail}")
        
        print()
        self.pause()
    
    def show_notifications(self):
        self.clear_screen()
        self.print_header("🔔 NOTIFICACIONES DEL SISTEMA 🔔")
        
        notifications = self.library_service.get_notifications()
        
        if not notifications:
            print("ℹ️ No hay notificaciones pendientes.")
        else:
            print("📢 Notificaciones recientes:\n")
            for i, notification in enumerate(notifications, 1):
                print(f"🔔 {i:2d}. {notification}")
        
        print()
        self.pause()
    
    def run(self):
        print("🎉 ¡Bienvenido al Sistema de Gestión de Biblioteca! 🎉")
        self.pause()
        
        while True:
            option = self.show_main_menu()
            
            if option == "1":
                self.show_books_menu()
            elif option == "2":
                self.show_users_menu()
            elif option == "3":
                self.show_loans_menu()
            elif option == "4":
                self.show_reports_menu()
            elif option == "5":
                print("\n👋 ¡Gracias por usar el Sistema de Gestión de Biblioteca! 📚")
                break
            else:
                print("❌ Opción no válida.")
                self.pause()