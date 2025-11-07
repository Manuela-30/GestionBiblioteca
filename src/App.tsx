import React, { useState, useEffect } from 'react';
import { 
  BookOpen, 
  Users, 
  TrendingUp, 
  Search, 
  Plus, 
  BarChart3,
  Library,
  UserPlus,
  BookPlus,
  ArrowUpDown,
  Clock,
  Star,
  Activity
} from 'lucide-react';

// Componentes
import BookCard from './components/BookCard';
import UserCard from './components/UserCard';
import StatsCard from './components/StatsCard';
import SearchBar from './components/SearchBar';
import Modal from './components/Modal';
import AddBookForm from './components/AddBookForm';
import AddUserForm from './components/AddUserForm';
import LoanForm from './components/LoanForm';
import Notifications from './components/Notifications';

// Tipos
interface Book {
  isbn: string;
  title: string;
  author: string;
  year: number;
  total_copies: number;
  available_copies: number;
  times_borrowed: number;
  popularity_score: number;
  current_borrowers: string[];
}

interface User {
  user_id: string;
  name: string;
  email: string;
  borrowed_count: number;
  borrowed_books: string[];
  activity_score: number;
  can_borrow_more: boolean;
}

interface Stats {
  total_books: number;
  total_copies: number;
  available_copies: number;
  borrowed_copies: number;
  total_users: number;
  active_users: number;
  utilization_rate: number;
}

function App() {
  // Estados principales
  const [books, setBooks] = useState<Book[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'books' | 'users' | 'loans' | 'stats'>('books');
  
  // Estados de búsqueda
  const [searchQuery, setSearchQuery] = useState('');
  const [filteredBooks, setFilteredBooks] = useState<Book[]>([]);
  const [filteredUsers, setFilteredUsers] = useState<User[]>([]);
  
  // Estados de modales
  const [showAddBook, setShowAddBook] = useState(false);
  const [showAddUser, setShowAddUser] = useState(false);
  const [showLoanForm, setShowLoanForm] = useState(false);
  
  // Estados de ordenamiento
  const [bookSortBy, setBookSortBy] = useState<'title' | 'author' | 'popularity' | 'availability'>('title');
  const [userSortBy, setUserSortBy] = useState<'name' | 'activity' | 'borrowed_count'>('name');

  /**
   * FUNCIÓN CRÍTICA: Manejo seguro de respuestas JSON
   * PREVIENE: "Unexpected end of JSON input"
   * GARANTIZA: Siempre retorna un objeto válido
   */
  const safeJsonParse = async (response: Response) => {
    try {
      // Paso 1: Verificar si la respuesta es exitosa
      if (!response.ok) {
        console.warn(`HTTP Error: ${response.status} - ${response.statusText}`);
        return {
          success: false,
          message: `Error HTTP: ${response.status}`,
          data: []
        };
      }

      // Paso 2: Obtener texto de la respuesta
      const text = await response.text();
      console.log(`Respuesta raw de ${response.url}:`, text);
      
      // Paso 3: Verificar si hay contenido
      if (!text || text.trim() === '') {
        console.warn('Respuesta vacía del servidor');
        return {
          success: true,
          message: 'Sin datos disponibles',
          data: []
        };
      }
      
      // Paso 4: Intentar parsear JSON
      const parsed = JSON.parse(text);
      console.log('JSON parseado exitosamente:', parsed);
      
      // Paso 5: Validar estructura esperada
      if (typeof parsed !== 'object' || parsed === null) {
        console.warn('Estructura JSON inválida');
        return {
          success: false,
          message: 'Estructura de respuesta inválida',
          data: []
        };
      }
      
      // Paso 6: Asegurar propiedades requeridas
      return {
        success: parsed.success !== undefined ? Boolean(parsed.success) : true,
        message: parsed.message || 'Datos cargados correctamente',
        data: Array.isArray(parsed.data) ? parsed.data : (parsed.data ? [parsed.data] : [])
      };
      
    } catch (error) {
      console.error('Error en safeJsonParse:', error);
      return {
        success: false,
        message: 'Error al procesar respuesta del servidor',
        data: []
      };
    }
  };

  // Cargar datos iniciales
  useEffect(() => {
    loadInitialData();
  }, []);

  // Filtrar y ordenar cuando cambian los datos o búsqueda
  useEffect(() => {
    filterAndSortBooks();
  }, [books, searchQuery, bookSortBy]);

  useEffect(() => {
    filterAndSortUsers();
  }, [users, searchQuery, userSortBy]);

  const loadInitialData = async () => {
    try {
      setLoading(true);
      console.log('🔄 Iniciando carga de datos iniciales...');
      
      // Configurar timeout para las peticiones
      const controller = new AbortController();
      const timeoutId = setTimeout(() => {
        controller.abort();
        console.warn('⏰ Timeout en carga de datos iniciales');
      }, 15000); // 15 segundos timeout

      try {
        // Cargar datos en paralelo para mejor rendimiento
        console.log('📚 Cargando libros...');
        console.log('👥 Cargando usuarios...');
        console.log('📊 Cargando estadísticas...');
        
        const [booksRes, usersRes, statsRes] = await Promise.all([
          fetch('/api/books', {
            method: 'GET',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
            },
            signal: controller.signal
          }),
          fetch('/api/users', {
            method: 'GET',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
            },
            signal: controller.signal
          }),
          fetch('/api/stats', {
            method: 'GET',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
            },
            signal: controller.signal
          })
        ]);

        clearTimeout(timeoutId);

        // Procesar respuestas de forma segura
        console.log('🔍 Procesando respuestas...');
        
        const booksData = await safeJsonParse(booksRes);
        const usersData = await safeJsonParse(usersRes);
        const statsData = await safeJsonParse(statsRes);

        // Actualizar estado solo si hay datos válidos
        if (booksData.success && Array.isArray(booksData.data)) {
          setBooks(booksData.data);
          console.log(`✅ ${booksData.data.length} libros cargados`);
        } else {
          console.warn('⚠️ No se pudieron cargar los libros:', booksData.message);
          setBooks([]); // Asegurar array vacío
        }

        if (usersData.success && Array.isArray(usersData.data)) {
          setUsers(usersData.data);
          console.log(`✅ ${usersData.data.length} usuarios cargados`);
        } else {
          console.warn('⚠️ No se pudieron cargar los usuarios:', usersData.message);
          setUsers([]); // Asegurar array vacío
        }

        if (statsData.success && statsData.data) {
          setStats(statsData.data);
          console.log('✅ Estadísticas cargadas');
        } else {
          console.warn('⚠️ No se pudieron cargar las estadísticas:', statsData.message);
          // Establecer estadísticas por defecto
          setStats({
            total_books: 0,
            total_copies: 0,
            available_copies: 0,
            borrowed_copies: 0,
            total_users: 0,
            active_users: 0,
            utilization_rate: 0
          });
        }

        console.log('🎉 Carga de datos iniciales completada');

      } catch (fetchError) {
        clearTimeout(timeoutId);
        
        if (fetchError instanceof Error && fetchError.name === 'AbortError') {
          console.error('⏰ Timeout: El servidor tardó demasiado en responder');
          // Establecer datos por defecto en caso de timeout
          setBooks([]);
          setUsers([]);
          setStats({
            total_books: 0,
            total_copies: 0,
            available_copies: 0,
            borrowed_copies: 0,
            total_users: 0,
            active_users: 0,
            utilization_rate: 0
          });
        } else {
          throw fetchError; // Re-lanzar para el catch externo
        }
      }

    } catch (error) {
      console.error('❌ Error crítico cargando datos iniciales:', error);
      
      // Manejar diferentes tipos de errores
      if (error instanceof TypeError && error.message.includes('fetch')) {
        console.error('🌐 Error de conexión - Verifica que el servidor esté funcionando');
      } else if (error instanceof SyntaxError && error.message.includes('JSON')) {
        console.error('📄 Error de formato JSON - Respuesta inválida del servidor');
      } else {
        console.error('🔥 Error inesperado:', error);
      }
      
      // Establecer datos por defecto para evitar crashes
      setBooks([]);
      setUsers([]);
      setStats({
        total_books: 0,
        total_copies: 0,
        available_copies: 0,
        borrowed_copies: 0,
        total_users: 0,
        active_users: 0,
        utilization_rate: 0
      });
    } finally {
      setLoading(false);
      console.log('🏁 Proceso de carga finalizado');
    }
  };

  const filterAndSortBooks = () => {
    let filtered = books;

    // Filtrar por búsqueda
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = books.filter(book => 
        book.title.toLowerCase().includes(query) ||
        book.author.toLowerCase().includes(query) ||
        book.isbn.includes(query)
      );
    }

    // Ordenar
    filtered.sort((a, b) => {
      switch (bookSortBy) {
        case 'title':
          return a.title.localeCompare(b.title);
        case 'author':
          return a.author.localeCompare(b.author);
        case 'popularity':
          return b.popularity_score - a.popularity_score;
        case 'availability':
          return b.available_copies - a.available_copies;
        default:
          return 0;
      }
    });

    setFilteredBooks(filtered);
  };

  const filterAndSortUsers = () => {
    let filtered = users;

    // Filtrar por búsqueda
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = users.filter(user => 
        user.name.toLowerCase().includes(query) ||
        user.email.toLowerCase().includes(query) ||
        user.user_id.toLowerCase().includes(query)
      );
    }

    // Ordenar
    filtered.sort((a, b) => {
      switch (userSortBy) {
        case 'name':
          return a.name.localeCompare(b.name);
        case 'activity':
          return b.activity_score - a.activity_score;
        case 'borrowed_count':
          return b.borrowed_count - a.borrowed_count;
        default:
          return 0;
      }
    });

    setFilteredUsers(filtered);
  };

  const handleBookAdded = () => {
    setShowAddBook(false);
    loadInitialData();
  };

  const handleUserAdded = () => {
    setShowAddUser(false);
    loadInitialData();
  };

  const handleLoanProcessed = () => {
    setShowLoanForm(false);
    loadInitialData();
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-indigo-600 mx-auto mb-4"></div>
          <p className="text-lg text-gray-600">Cargando Sistema de Biblioteca...</p>
          <p className="text-sm text-gray-500 mt-2">Optimizado con Árboles Binarios 🌳</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-lg border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-3">
              <div className="bg-gradient-to-r from-indigo-600 to-purple-600 p-3 rounded-xl">
                <Library className="h-8 w-8 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">
                  Sistema de Biblioteca
                </h1>
                <p className="text-sm text-gray-600 mt-1">
                  Optimizado con Estructuras de Datos Avanzadas
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <Notifications />
              <div className="flex space-x-2">
                <button
                  onClick={() => setShowAddBook(true)}
                  className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg flex items-center space-x-2 transition-colors"
                >
                  <BookPlus className="h-4 w-4" />
                  <span>Agregar Libro</span>
                </button>
                <button
                  onClick={() => setShowAddUser(true)}
                  className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg flex items-center space-x-2 transition-colors"
                >
                  <UserPlus className="h-4 w-4" />
                  <span>Agregar Usuario</span>
                </button>
                <button
                  onClick={() => setShowLoanForm(true)}
                  className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg flex items-center space-x-2 transition-colors"
                >
                  <ArrowUpDown className="h-4 w-4" />
                  <span>Préstamo</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {[
              { id: 'books', label: 'Libros', icon: BookOpen, count: books.length },
              { id: 'users', label: 'Usuarios', icon: Users, count: users.length },
              { id: 'loans', label: 'Préstamos', icon: ArrowUpDown, count: stats?.borrowed_copies || 0 },
              { id: 'stats', label: 'Estadísticas', icon: BarChart3 }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                  activeTab === tab.id
                    ? 'border-indigo-500 text-indigo-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <tab.icon className="h-5 w-5" />
                <span>{tab.label}</span>
                {tab.count !== undefined && (
                  <span className={`px-2 py-1 rounded-full text-xs ${
                    activeTab === tab.id
                      ? 'bg-indigo-100 text-indigo-600'
                      : 'bg-gray-100 text-gray-600'
                  }`}>
                    {tab.count}
                  </span>
                )}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search and Filters */}
        {(activeTab === 'books' || activeTab === 'users') && (
          <div className="mb-8 bg-white rounded-xl shadow-sm p-6">
            <div className="flex flex-col sm:flex-row gap-4 items-center justify-between">
              <SearchBar
                value={searchQuery}
                onChange={setSearchQuery}
                placeholder={`Buscar ${activeTab === 'books' ? 'libros' : 'usuarios'}...`}
              />
              
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <ArrowUpDown className="h-4 w-4 text-gray-500" />
                  <span className="text-sm text-gray-600">Ordenar por:</span>
                  {activeTab === 'books' ? (
                    <select
                      value={bookSortBy}
                      onChange={(e) => setBookSortBy(e.target.value as any)}
                      className="border border-gray-300 rounded-lg px-3 py-1 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    >
                      <option value="title">Título</option>
                      <option value="author">Autor</option>
                      <option value="popularity">Popularidad</option>
                      <option value="availability">Disponibilidad</option>
                    </select>
                  ) : (
                    <select
                      value={userSortBy}
                      onChange={(e) => setUserSortBy(e.target.value as any)}
                      className="border border-gray-300 rounded-lg px-3 py-1 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    >
                      <option value="name">Nombre</option>
                      <option value="activity">Actividad</option>
                      <option value="borrowed_count">Libros Prestados</option>
                    </select>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Content by Tab */}
        {activeTab === 'books' && (
          <div>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">
                Catálogo de Libros ({filteredBooks.length})
              </h2>
              <div className="text-sm text-gray-600">
                Búsqueda optimizada con Árboles Binarios - O(log n)
              </div>
            </div>
            
            {filteredBooks.length === 0 ? (
              <div className="text-center py-12">
                <BookOpen className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                <p className="text-xl text-gray-600 mb-2">No se encontraron libros</p>
                <p className="text-gray-500">
                  {searchQuery ? 'Intenta con otros términos de búsqueda' : 'Agrega algunos libros para comenzar'}
                </p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {filteredBooks.map((book) => (
                  <BookCard key={book.isbn} book={book} onUpdate={loadInitialData} />
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'users' && (
          <div>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">
                Usuarios Registrados ({filteredUsers.length})
              </h2>
              <div className="text-sm text-gray-600">
                Gestión eficiente con Índices Múltiples
              </div>
            </div>
            
            {filteredUsers.length === 0 ? (
              <div className="text-center py-12">
                <Users className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                <p className="text-xl text-gray-600 mb-2">No se encontraron usuarios</p>
                <p className="text-gray-500">
                  {searchQuery ? 'Intenta con otros términos de búsqueda' : 'Registra algunos usuarios para comenzar'}
                </p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredUsers.map((user) => (
                  <UserCard key={user.user_id} user={user} onUpdate={loadInitialData} />
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'stats' && stats && (
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              Estadísticas del Sistema
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <StatsCard
                title="Total Libros"
                value={stats.total_books}
                icon={BookOpen}
                color="blue"
                subtitle={`${stats.total_copies} copias totales`}
              />
              <StatsCard
                title="Usuarios Activos"
                value={stats.active_users}
                icon={Users}
                color="green"
                subtitle={`de ${stats.total_users} registrados`}
              />
              <StatsCard
                title="Préstamos Activos"
                value={stats.borrowed_copies}
                icon={ArrowUpDown}
                color="purple"
                subtitle={`${stats.available_copies} disponibles`}
              />
              <StatsCard
                title="Tasa de Utilización"
                value={`${stats.utilization_rate.toFixed(1)}%`}
                icon={TrendingUp}
                color="orange"
                subtitle="Eficiencia del sistema"
              />
            </div>

            {/* Gráficos y estadísticas adicionales */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div className="bg-white rounded-xl shadow-sm p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <Star className="h-5 w-5 text-yellow-500 mr-2" />
                  Libros Más Populares
                </h3>
                <div className="space-y-3">
                  {books
                    .sort((a, b) => b.popularity_score - a.popularity_score)
                    .slice(0, 5)
                    .map((book, index) => (
                      <div key={book.isbn} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div className="flex items-center space-x-3">
                          <span className="flex items-center justify-center w-6 h-6 bg-yellow-100 text-yellow-800 rounded-full text-sm font-medium">
                            {index + 1}
                          </span>
                          <div>
                            <p className="font-medium text-gray-900">{book.title}</p>
                            <p className="text-sm text-gray-600">{book.author}</p>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="text-sm font-medium text-gray-900">{book.times_borrowed} préstamos</p>
                          <p className="text-xs text-gray-500">Score: {book.popularity_score.toFixed(2)}</p>
                        </div>
                      </div>
                    ))}
                </div>
              </div>

              <div className="bg-white rounded-xl shadow-sm p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <Activity className="h-5 w-5 text-green-500 mr-2" />
                  Usuarios Más Activos
                </h3>
                <div className="space-y-3">
                  {users
                    .sort((a, b) => b.activity_score - a.activity_score)
                    .slice(0, 5)
                    .map((user, index) => (
                      <div key={user.user_id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div className="flex items-center space-x-3">
                          <span className="flex items-center justify-center w-6 h-6 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                            {index + 1}
                          </span>
                          <div>
                            <p className="font-medium text-gray-900">{user.name}</p>
                            <p className="text-sm text-gray-600">{user.email}</p>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="text-sm font-medium text-gray-900">{user.borrowed_count} libros</p>
                          <p className="text-xs text-gray-500">Score: {user.activity_score.toFixed(2)}</p>
                        </div>
                      </div>
                    ))}
                </div>
              </div>
            </div>

            {/* Información técnica */}
            <div className="mt-8 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                🌳 Optimización con Estructuras de Datos
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div className="bg-white rounded-lg p-4">
                  <h4 className="font-medium text-indigo-600 mb-2">Árboles Binarios de Búsqueda</h4>
                  <p className="text-gray-600">Búsquedas O(log n) vs O(n) en listas lineales</p>
                </div>
                <div className="bg-white rounded-lg p-4">
                  <h4 className="font-medium text-purple-600 mb-2">Índices Múltiples</h4>
                  <p className="text-gray-600">Búsquedas multi-criterio eficientes</p>
                </div>
                <div className="bg-white rounded-lg p-4">
                  <h4 className="font-medium text-green-600 mb-2">Estructuras Lineales</h4>
                  <p className="text-gray-600">Pilas, colas y arreglos dinámicos complementarios</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Modales */}
      <Modal isOpen={showAddBook} onClose={() => setShowAddBook(false)} title="Agregar Nuevo Libro">
        <AddBookForm onSuccess={handleBookAdded} onCancel={() => setShowAddBook(false)} />
      </Modal>

      <Modal isOpen={showAddUser} onClose={() => setShowAddUser(false)} title="Registrar Nuevo Usuario">
        <AddUserForm onSuccess={handleUserAdded} onCancel={() => setShowAddUser(false)} />
      </Modal>

      <Modal isOpen={showLoanForm} onClose={() => setShowLoanForm(false)} title="Gestionar Préstamo">
        <LoanForm onSuccess={handleLoanProcessed} onCancel={() => setShowLoanForm(false)} />
      </Modal>
    </div>
  );
}

export default App;