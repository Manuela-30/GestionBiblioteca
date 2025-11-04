import React, { useState } from 'react';
import { User, Mail, BookOpen, Activity, Trash2, Eye, Star } from 'lucide-react';

interface UserProps {
  user: {
    user_id: string;
    name: string;
    email: string;
    borrowed_count: number;
    borrowed_books: string[];
    activity_score: number;
    can_borrow_more: boolean;
  };
  onUpdate: () => void;
}

const UserCard: React.FC<UserProps> = ({ user, onUpdate }) => {
  const [showDetails, setShowDetails] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [borrowedBooks, setBorrowedBooks] = useState<any[]>([]);
  const [loadingBooks, setLoadingBooks] = useState(false);

  const handleDelete = async () => {
    if (!confirm(`¿Estás seguro de eliminar al usuario "${user.name}"?`)) return;
    
    setIsDeleting(true);
    try {
      const response = await fetch(`/api/users/${user.user_id}`, {
        method: 'DELETE'
      });
      
      const data = await response.json();
      
      if (data.success) {
        onUpdate();
      } else {
        alert(data.message || 'Error al eliminar el usuario');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error al eliminar el usuario');
    } finally {
      setIsDeleting(false);
    }
  };

  const loadBorrowedBooks = async () => {
    if (borrowedBooks.length > 0) return; // Ya cargados
    
    setLoadingBooks(true);
    try {
      const response = await fetch(`/api/users/${user.user_id}/books`);
      const data = await response.json();
      
      if (data.success) {
        setBorrowedBooks(data.data);
      }
    } catch (error) {
      console.error('Error cargando libros:', error);
    } finally {
      setLoadingBooks(false);
    }
  };

  const handleShowDetails = () => {
    setShowDetails(!showDetails);
    if (!showDetails && user.borrowed_count > 0) {
      loadBorrowedBooks();
    }
  };

  const getActivityLevel = () => {
    if (user.activity_score >= 10) return { level: 'Muy Alto', color: 'text-green-600 bg-green-50' };
    if (user.activity_score >= 5) return { level: 'Alto', color: 'text-blue-600 bg-blue-50' };
    if (user.activity_score >= 2) return { level: 'Medio', color: 'text-yellow-600 bg-yellow-50' };
    return { level: 'Bajo', color: 'text-gray-600 bg-gray-50' };
  };

  const getActivityStars = () => {
    const stars = Math.min(5, Math.floor(user.activity_score / 2));
    return Array.from({ length: 5 }, (_, i) => (
      <Star
        key={i}
        className={`h-4 w-4 ${
          i < stars ? 'text-blue-400 fill-current' : 'text-gray-300'
        }`}
      />
    ));
  };

  const activityLevel = getActivityLevel();

  return (
    <div className="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow duration-200 overflow-hidden">
      {/* Header */}
      <div className="p-6 pb-4">
        <div className="flex items-start justify-between mb-3">
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900 mb-1">
              {user.name}
            </h3>
            <div className="flex items-center space-x-2 text-sm text-gray-600 mb-2">
              <Mail className="h-4 w-4" />
              <span>{user.email}</span>
            </div>
            <div className="text-xs text-gray-500">
              ID: {user.user_id}
            </div>
          </div>
          
          <div className="flex items-center space-x-1 ml-4">
            <button
              onClick={handleShowDetails}
              className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
              title="Ver detalles"
            >
              <Eye className="h-4 w-4" />
            </button>
            <button
              onClick={handleDelete}
              disabled={isDeleting || user.borrowed_count > 0}
              className="p-2 text-gray-400 hover:text-red-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              title={user.borrowed_count > 0 ? "No se puede eliminar (tiene libros prestados)" : "Eliminar usuario"}
            >
              <Trash2 className="h-4 w-4" />
            </button>
          </div>
        </div>

        {/* Actividad */}
        <div className="flex items-center space-x-2 mb-3">
          <div className="flex items-center space-x-1">
            {getActivityStars()}
          </div>
          <span className="text-xs text-gray-500">
            Score: {user.activity_score.toFixed(1)}
          </span>
        </div>

        {/* Estadísticas */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <BookOpen className="h-4 w-4 text-gray-400" />
            <span className="text-sm text-gray-600">
              {user.borrowed_count} libros prestados
            </span>
          </div>
          
          <div className="flex items-center space-x-2">
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${activityLevel.color}`}>
              {activityLevel.level}
            </span>
            {!user.can_borrow_more && (
              <span className="px-2 py-1 rounded-full text-xs font-medium text-red-600 bg-red-50">
                Límite alcanzado
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Detalles expandibles */}
      {showDetails && (
        <div className="px-6 pb-6 pt-2 border-t border-gray-100">
          <div className="space-y-3">
            <div>
              <h4 className="text-sm font-medium text-gray-900 mb-2">Estadísticas de Usuario</h4>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-gray-500">Actividad:</span>
                  <span className="ml-2 font-medium">{user.activity_score.toFixed(2)}</span>
                </div>
                <div>
                  <span className="text-gray-500">Estado:</span>
                  <span className="ml-2 font-medium">
                    {user.can_borrow_more ? 'Puede pedir más' : 'Límite alcanzado'}
                  </span>
                </div>
              </div>
            </div>

            {user.borrowed_count > 0 && (
              <div>
                <h4 className="text-sm font-medium text-gray-900 mb-2">
                  Libros Prestados ({user.borrowed_count})
                </h4>
                
                {loadingBooks ? (
                  <div className="flex items-center justify-center py-4">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
                  </div>
                ) : (
                  <div className="space-y-2 max-h-32 overflow-y-auto">
                    {borrowedBooks.map((book, index) => (
                      <div key={index} className="flex items-center space-x-2 text-sm p-2 bg-gray-50 rounded-lg">
                        <BookOpen className="h-3 w-3 text-gray-400 flex-shrink-0" />
                        <div className="flex-1 min-w-0">
                          <p className="font-medium text-gray-900 truncate">{book.title}</p>
                          <p className="text-gray-500 truncate">{book.author}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            <div className="pt-2 border-t border-gray-100">
              <div className="text-xs text-gray-500">
                🔍 <strong>Búsqueda eficiente:</strong> O(log n) con BST por ID de usuario
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Indicador de carga */}
      {isDeleting && (
        <div className="absolute inset-0 bg-white bg-opacity-75 flex items-center justify-center">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-red-600"></div>
        </div>
      )}
    </div>
  );
};

export default UserCard;