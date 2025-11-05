import React, { useState, useEffect } from 'react';
import { ArrowUpDown, ArrowRight, ArrowLeft, Loader, Search } from 'lucide-react';

interface LoanFormProps {
  onSuccess: () => void;
  onCancel: () => void;
}

interface Book {
  isbn: string;
  title: string;
  author: string;
  available_copies: number;
}

interface User {
  user_id: string;
  name: string;
  email: string;
  borrowed_count: number;
  can_borrow_more: boolean;
}

const LoanForm: React.FC<LoanFormProps> = ({ onSuccess, onCancel }) => {
  const [action, setAction] = useState<'borrow' | 'return'>('borrow');
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [selectedBook, setSelectedBook] = useState<Book | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [books, setBooks] = useState<Book[]>([]);
  const [userBooks, setUserBooks] = useState<Book[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [userSearch, setUserSearch] = useState('');
  const [bookSearch, setBookSearch] = useState('');

  /**
   * Función auxiliar para manejar respuestas HTTP de forma segura
   * Evita el error "Unexpected end of JSON input"
   */
  const safeJsonParse = async (response: Response) => {
    const text = await response.text();
    
    if (!text || text.trim() === '') {
      return {
        success: false,
        message: 'Respuesta vacía del servidor',
        data: null
      };
    }
    
    try {
      return JSON.parse(text);
    } catch (error) {
      console.error('Error parsing JSON:', error);
      console.error('Response text:', text);
      return {
        success: false,
        message: 'Respuesta inválida del servidor',
        data: null
      };
    }
  };

  useEffect(() => {
    loadUsers();
    if (action === 'borrow') {
      loadAvailableBooks();
    }
  }, [action]);

  useEffect(() => {
    if (selectedUser && action === 'return') {
      loadUserBooks();
    }
  }, [selectedUser, action]);

  const loadUsers = async () => {
    try {
      const response = await fetch('/api/users');
      const data = await safeJsonParse(response);
      if (data.success) {
        setUsers(data.data);
      }
    } catch (error) {
      console.error('Error cargando usuarios:', error);
    }
  };

  const loadAvailableBooks = async () => {
    try {
      const response = await fetch('/api/books');
      const data = await safeJsonParse(response);
      if (data.success) {
        setBooks(data.data.filter((book: Book) => book.available_copies > 0));
      }
    } catch (error) {
      console.error('Error cargando libros:', error);
    }
  };

  const loadUserBooks = async () => {
    if (!selectedUser) return;
    
    try {
      const response = await fetch(`/api/users/${selectedUser.user_id}/books`);
      const data = await safeJsonParse(response);
      if (data.success) {
        setUserBooks(data.data);
      }
    } catch (error) {
      console.error('Error cargando libros del usuario:', error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedUser || !selectedBook) {
      setError('Selecciona un usuario y un libro');
      return;
    }

    setIsSubmitting(true);
    setError('');

    try {
      let response;
      
      if (action === 'borrow') {
        console.log('Prestando libro:', { user_id: selectedUser.user_id, isbn: selectedBook.isbn });
        response = await fetch('/api/loans', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            user_id: selectedUser.user_id,
            isbn: selectedBook.isbn
          }),
        });
      } else {
        console.log('Devolviendo libro:', { user_id: selectedUser.user_id, isbn: selectedBook.isbn });
        response = await fetch(`/api/loans/${selectedUser.user_id}/${selectedBook.isbn}`, {
          method: 'DELETE'
        });
      }

      console.log('Respuesta del servidor - Status:', response.status);
      const data = await safeJsonParse(response);
      console.log('Datos parseados:', data);

      if (data.success) {
        console.log('Operación exitosa:', data.message);
        onSuccess();
      } else {
        const errorMessage = data.message || `Error al ${action === 'borrow' ? 'prestar' : 'devolver'} el libro`;
        console.error('Error del servidor:', errorMessage);
        setError(errorMessage);
      }
    } catch (error) {
      console.error('Error:', error);
      
      // Manejar diferentes tipos de errores
      if (error instanceof TypeError && error.message.includes('fetch')) {
        setError('Error de conexión. Verifica que el servidor esté funcionando.');
      } else if (error instanceof SyntaxError) {
        setError('Error de comunicación con el servidor. Respuesta inválida.');
      } else {
        setError(`Error inesperado: ${error instanceof Error ? error.message : 'Error desconocido'}`);
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const filteredUsers = users.filter(user => 
    user.name.toLowerCase().includes(userSearch.toLowerCase()) ||
    user.user_id.toLowerCase().includes(userSearch.toLowerCase()) ||
    user.email.toLowerCase().includes(userSearch.toLowerCase())
  );

  const filteredBooks = (action === 'borrow' ? books : userBooks).filter(book => 
    book.title.toLowerCase().includes(bookSearch.toLowerCase()) ||
    book.author.toLowerCase().includes(bookSearch.toLowerCase()) ||
    book.isbn.includes(bookSearch)
  );

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-sm text-red-600">{error}</p>
        </div>
      )}

      {/* Selector de acción */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Tipo de Operación
        </label>
        <div className="flex space-x-4">
          <button
            type="button"
            onClick={() => {
              setAction('borrow');
              setSelectedBook(null);
              setError('');
            }}
            className={`flex items-center space-x-2 px-4 py-2 rounded-lg border transition-colors ${
              action === 'borrow'
                ? 'bg-blue-50 border-blue-200 text-blue-700'
                : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
            }`}
          >
            <ArrowRight className="h-4 w-4" />
            <span>Prestar Libro</span>
          </button>
          <button
            type="button"
            onClick={() => {
              setAction('return');
              setSelectedBook(null);
              setError('');
            }}
            className={`flex items-center space-x-2 px-4 py-2 rounded-lg border transition-colors ${
              action === 'return'
                ? 'bg-green-50 border-green-200 text-green-700'
                : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
            }`}
          >
            <ArrowLeft className="h-4 w-4" />
            <span>Devolver Libro</span>
          </button>
        </div>
      </div>

      {/* Selector de usuario */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Usuario *
        </label>
        <div className="space-y-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              value={userSearch}
              onChange={(e) => setUserSearch(e.target.value)}
              placeholder="Buscar usuario por nombre, ID o email..."
              className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>
          
          <div className="max-h-40 overflow-y-auto border border-gray-300 rounded-lg">
            {filteredUsers.map((user) => (
              <button
                key={user.user_id}
                type="button"
                onClick={() => setSelectedUser(user)}
                className={`w-full text-left p-3 hover:bg-gray-50 transition-colors border-b border-gray-100 last:border-b-0 ${
                  selectedUser?.user_id === user.user_id ? 'bg-blue-50 border-blue-200' : ''
                }`}
              >
                <div className="flex justify-between items-start">
                  <div>
                    <p className="font-medium text-gray-900">{user.name}</p>
                    <p className="text-sm text-gray-600">{user.email}</p>
                    <p className="text-xs text-gray-500">ID: {user.user_id}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-gray-600">{user.borrowed_count} libros</p>
                    {!user.can_borrow_more && action === 'borrow' && (
                      <p className="text-xs text-red-600">Límite alcanzado</p>
                    )}
                  </div>
                </div>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Selector de libro */}
      {selectedUser && (
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {action === 'borrow' ? 'Libro a Prestar *' : 'Libro a Devolver *'}
          </label>
          <div className="space-y-3">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                value={bookSearch}
                onChange={(e) => setBookSearch(e.target.value)}
                placeholder="Buscar libro por título, autor o ISBN..."
                className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
            
            <div className="max-h-40 overflow-y-auto border border-gray-300 rounded-lg">
              {filteredBooks.length === 0 ? (
                <div className="p-4 text-center text-gray-500">
                  {action === 'borrow' 
                    ? 'No hay libros disponibles' 
                    : 'El usuario no tiene libros prestados'
                  }
                </div>
              ) : (
                filteredBooks.map((book) => (
                  <button
                    key={book.isbn}
                    type="button"
                    onClick={() => setSelectedBook(book)}
                    className={`w-full text-left p-3 hover:bg-gray-50 transition-colors border-b border-gray-100 last:border-b-0 ${
                      selectedBook?.isbn === book.isbn ? 'bg-blue-50 border-blue-200' : ''
                    }`}
                  >
                    <div className="flex justify-between items-start">
                      <div>
                        <p className="font-medium text-gray-900">{book.title}</p>
                        <p className="text-sm text-gray-600">{book.author}</p>
                        <p className="text-xs text-gray-500">ISBN: {book.isbn}</p>
                      </div>
                      {action === 'borrow' && (
                        <div className="text-right">
                          <p className="text-sm text-gray-600">
                            {book.available_copies} disponibles
                          </p>
                        </div>
                      )}
                    </div>
                  </button>
                ))
              )}
            </div>
          </div>
        </div>
      )}

      {/* Información de la operación */}
      {selectedUser && selectedBook && (
        <div className={`rounded-lg p-4 ${
          action === 'borrow' ? 'bg-blue-50 border border-blue-200' : 'bg-green-50 border border-green-200'
        }`}>
          <div className="flex items-start space-x-2">
            <ArrowUpDown className={`h-5 w-5 mt-0.5 ${
              action === 'borrow' ? 'text-blue-600' : 'text-green-600'
            }`} />
            <div>
              <h4 className={`text-sm font-medium ${
                action === 'borrow' ? 'text-blue-900' : 'text-green-900'
              }`}>
                {action === 'borrow' ? 'Confirmar Préstamo' : 'Confirmar Devolución'}
              </h4>
              <p className={`text-sm mt-1 ${
                action === 'borrow' ? 'text-blue-700' : 'text-green-700'
              }`}>
                <strong>{selectedUser.name}</strong> {action === 'borrow' ? 'tomará prestado' : 'devolverá'} 
                <strong> "{selectedBook.title}"</strong>
              </p>
            </div>
          </div>
        </div>
      )}

      <div className="flex justify-end space-x-3 pt-4 border-t border-gray-200">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
        >
          Cancelar
        </button>
        <button
          type="submit"
          disabled={isSubmitting || !selectedUser || !selectedBook}
          className={`px-4 py-2 text-sm font-medium text-white border border-transparent rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center space-x-2 ${
            action === 'borrow'
              ? 'bg-blue-600 hover:bg-blue-700 focus:ring-blue-500'
              : 'bg-green-600 hover:bg-green-700 focus:ring-green-500'
          }`}
        >
          {isSubmitting ? (
            <>
              <Loader className="h-4 w-4 animate-spin" />
              <span>Procesando...</span>
            </>
          ) : (
            <>
              {action === 'borrow' ? <ArrowRight className="h-4 w-4" /> : <ArrowLeft className="h-4 w-4" />}
              <span>{action === 'borrow' ? 'Prestar Libro' : 'Devolver Libro'}</span>
            </>
          )}
        </button>
      </div>
    </form>
  );
};

export default LoanForm;