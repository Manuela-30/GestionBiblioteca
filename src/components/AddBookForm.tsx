import React, { useState } from 'react';
import { BookPlus, Loader } from 'lucide-react';

interface AddBookFormProps {
  onSuccess: () => void;
  onCancel: () => void;
}

const AddBookForm: React.FC<AddBookFormProps> = ({ onSuccess, onCancel }) => {
  const [formData, setFormData] = useState({
    isbn: '',
    title: '',
    author: '',
    year: new Date().getFullYear(),
    copies: 1
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'year' || name === 'copies' ? parseInt(value) || 0 : value
    }));
    setError(''); // Limpiar error al cambiar datos
  };

  /**
   * Función auxiliar para manejar respuestas HTTP de forma segura
   * Evita el error "Unexpected end of JSON input"
   */
  const safeJsonParse = async (response: Response) => {
    const text = await response.text();
    
    // Si no hay contenido, devolver objeto por defecto
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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validaciones del frontend
    if (!formData.isbn.trim()) {
      setError('El ISBN es requerido');
      return;
    }
    if (!formData.title.trim()) {
      setError('El título es requerido');
      return;
    }
    if (!formData.author.trim()) {
      setError('El autor es requerido');
      return;
    }
    if (formData.year < 1000 || formData.year > new Date().getFullYear() + 10) {
      setError('El año debe ser válido');
      return;
    }
    if (formData.copies < 1) {
      setError('Debe haber al menos 1 copia');
      return;
    }

    setIsSubmitting(true);
    setError('');

    try {
      // Preparar datos para envío
      const bookData = {
        isbn: formData.isbn.trim(),
        title: formData.title.trim(),
        author: formData.author.trim(),
        year: formData.year,
        copies: formData.copies
      };

      console.log('Enviando datos del libro:', bookData);

      const response = await fetch('/api/books', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(bookData),
      });

      console.log('Respuesta del servidor - Status:', response.status);
      console.log('Respuesta del servidor - Headers:', response.headers);

      // Usar función segura para parsear JSON
      const data = await safeJsonParse(response);
      console.log('Datos parseados:', data);

      if (data.success) {
        console.log('Libro agregado exitosamente:', data.data);
        onSuccess();
      } else {
        const errorMessage = data.message || 'Error desconocido al agregar el libro';
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

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-start space-x-2">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div>
              <h3 className="text-sm font-medium text-red-800">Error al agregar libro</h3>
              <p className="text-sm text-red-600 mt-1">{error}</p>
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="md:col-span-2">
          <label htmlFor="isbn" className="block text-sm font-medium text-gray-700 mb-2">
            ISBN *
          </label>
          <input
            type="text"
            id="isbn"
            name="isbn"
            value={formData.isbn}
            onChange={handleChange}
            placeholder="978-0-123456-78-9"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            required
            disabled={isSubmitting}
          />
          <p className="text-xs text-gray-500 mt-1">
            Clave única para búsqueda O(log n) en Árbol Binario
          </p>
        </div>

        <div className="md:col-span-2">
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
            Título *
          </label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            placeholder="El nombre del libro"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            required
            disabled={isSubmitting}
          />
        </div>

        <div className="md:col-span-2">
          <label htmlFor="author" className="block text-sm font-medium text-gray-700 mb-2">
            Autor *
          </label>
          <input
            type="text"
            id="author"
            name="author"
            value={formData.author}
            onChange={handleChange}
            placeholder="Nombre del autor"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            required
            disabled={isSubmitting}
          />
        </div>

        <div>
          <label htmlFor="year" className="block text-sm font-medium text-gray-700 mb-2">
            Año de Publicación *
          </label>
          <input
            type="number"
            id="year"
            name="year"
            value={formData.year}
            onChange={handleChange}
            min="1000"
            max={new Date().getFullYear() + 10}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            required
            disabled={isSubmitting}
          />
        </div>

        <div>
          <label htmlFor="copies" className="block text-sm font-medium text-gray-700 mb-2">
            Número de Copias *
          </label>
          <input
            type="number"
            id="copies"
            name="copies"
            value={formData.copies}
            onChange={handleChange}
            min="1"
            max="100"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            required
            disabled={isSubmitting}
          />
        </div>
      </div>

      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-start space-x-2">
          <BookPlus className="h-5 w-5 text-blue-600 mt-0.5" />
          <div>
            <h4 className="text-sm font-medium text-blue-900">Optimización con Árboles Binarios</h4>
            <p className="text-sm text-blue-700 mt-1">
              El libro se indexará automáticamente por ISBN, título y autor para búsquedas eficientes O(log n).
            </p>
          </div>
        </div>
      </div>

      <div className="flex justify-end space-x-3 pt-4 border-t border-gray-200">
        <button
          type="button"
          onClick={onCancel}
          disabled={isSubmitting}
          className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
        >
          Cancelar
        </button>
        <button
          type="submit"
          disabled={isSubmitting}
          className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
        >
          {isSubmitting ? (
            <>
              <Loader className="h-4 w-4 animate-spin" />
              <span>Agregando...</span>
            </>
          ) : (
            <>
              <BookPlus className="h-4 w-4" />
              <span>Agregar Libro</span>
            </>
          )}
        </button>
      </div>
    </form>
  );
};

export default AddBookForm;