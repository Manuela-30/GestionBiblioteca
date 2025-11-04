import React, { useState } from 'react';
import { Book, User, Star, Calendar, Copy, Trash2, Eye } from 'lucide-react';

interface BookProps {
  book: {
    isbn: string;
    title: string;
    author: string;
    year: number;
    total_copies: number;
    available_copies: number;
    times_borrowed: number;
    popularity_score: number;
    current_borrowers: string[];
  };
  onUpdate: () => void;
}

const BookCard: React.FC<BookProps> = ({ book, onUpdate }) => {
  const [showDetails, setShowDetails] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const handleDelete = async () => {
    if (!confirm(`¿Estás seguro de eliminar "${book.title}"?`)) return;
    
    setIsDeleting(true);
    try {
      const response = await fetch(`/api/books/${book.isbn}`, {
        method: 'DELETE'
      });
      
      const data = await response.json();
      
      if (data.success) {
        onUpdate();
      } else {
        alert(data.message || 'Error al eliminar el libro');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error al eliminar el libro');
    } finally {
      setIsDeleting(false);
    }
  };

  const getAvailabilityColor = () => {
    const ratio = book.available_copies / book.total_copies;
    if (ratio === 0) return 'text-red-600 bg-red-50';
    if (ratio < 0.5) return 'text-orange-600 bg-orange-50';
    return 'text-green-600 bg-green-50';
  };

  const getPopularityStars = () => {
    const stars = Math.min(5, Math.floor(book.popularity_score * 2));
    return Array.from({ length: 5 }, (_, i) => (
      <Star
        key={i}
        className={`h-4 w-4 ${
          i < stars ? 'text-yellow-400 fill-current' : 'text-gray-300'
        }`}
      />
    ));
  };

  return (
    <div className="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow duration-200 overflow-hidden">
      {/* Header */}
      <div className="p-6 pb-4">
        <div className="flex items-start justify-between mb-3">
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900 mb-1 line-clamp-2">
              {book.title}
            </h3>
            <p className="text-sm text-gray-600 mb-1">por {book.author}</p>
            <div className="flex items-center space-x-2 text-xs text-gray-500">
              <Calendar className="h-3 w-3" />
              <span>{book.year}</span>
              <span>•</span>
              <span>ISBN: {book.isbn}</span>
            </div>
          </div>
          
          <div className="flex items-center space-x-1 ml-4">
            <button
              onClick={() => setShowDetails(!showDetails)}
              className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
              title="Ver detalles"
            >
              <Eye className="h-4 w-4" />
            </button>
            <button
              onClick={handleDelete}
              disabled={isDeleting || book.available_copies !== book.total_copies}
              className="p-2 text-gray-400 hover:text-red-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              title={book.available_copies !== book.total_copies ? "No se puede eliminar (copias prestadas)" : "Eliminar libro"}
            >
              <Trash2 className="h-4 w-4" />
            </button>
          </div>
        </div>

        {/* Popularidad */}
        <div className="flex items-center space-x-2 mb-3">
          <div className="flex items-center space-x-1">
            {getPopularityStars()}
          </div>
          <span className="text-xs text-gray-500">
            {book.times_borrowed} préstamos
          </span>
        </div>

        {/* Disponibilidad */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Copy className="h-4 w-4 text-gray-400" />
            <span className="text-sm text-gray-600">
              {book.available_copies} de {book.total_copies} disponibles
            </span>
          </div>
          
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getAvailabilityColor()}`}>
            {book.available_copies === 0 ? 'Agotado' : 
             book.available_copies === book.total_copies ? 'Disponible' : 'Parcial'}
          </span>
        </div>
      </div>

      {/* Detalles expandibles */}
      {showDetails && (
        <div className="px-6 pb-6 pt-2 border-t border-gray-100">
          <div className="space-y-3">
            <div>
              <h4 className="text-sm font-medium text-gray-900 mb-2">Estadísticas</h4>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-gray-500">Popularidad:</span>
                  <span className="ml-2 font-medium">{book.popularity_score.toFixed(2)}</span>
                </div>
                <div>
                  <span className="text-gray-500">Préstamos:</span>
                  <span className="ml-2 font-medium">{book.times_borrowed}</span>
                </div>
              </div>
            </div>

            {book.current_borrowers.length > 0 && (
              <div>
                <h4 className="text-sm font-medium text-gray-900 mb-2">
                  Prestado actualmente a:
                </h4>
                <div className="space-y-1">
                  {book.current_borrowers.map((borrower, index) => (
                    <div key={index} className="flex items-center space-x-2 text-sm">
                      <User className="h-3 w-3 text-gray-400" />
                      <span className="text-gray-600">{borrower}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="pt-2 border-t border-gray-100">
              <div className="text-xs text-gray-500">
                💡 <strong>Optimización:</strong> Búsqueda O(log n) con Árbol Binario por ISBN
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

export default BookCard;