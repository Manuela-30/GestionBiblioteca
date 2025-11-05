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

  /**
   * FUNCIÓN CRÍTICA: Manejo seguro de respuestas JSON
   * PREVIENE: "Unexpected end of JSON input"
   * GARANTIZA: Siempre retorna un objeto válido
   */
  const safeJsonParse = async (response: Response) => {
    try {
      // Paso 1: Obtener texto de la respuesta
      const text = await response.text();
      console.log('Respuesta raw del servidor:', text);
      
      // Paso 2: Verificar si hay contenido
      if (!text || text.trim() === '') {
        console.warn('Respuesta vacía del servidor');
        return {
          success: false,
          message: 'Respuesta vacía del servidor',
          data: null
        };
      }
      
      // Paso 3: Intentar parsear JSON
      const parsed = JSON.parse(text);
      console.log('JSON parseado exitosamente:', parsed);
      
      // Paso 4: Validar estructura esperada
      if (typeof parsed !== 'object' || parsed === null) {
        console.warn('Estructura JSON inválida');
        return {
          success: false,
          message: 'Estructura de respuesta inválida',
          data: null
        };
      }
      
      // Paso 5: Asegurar propiedades requeridas
      return {
        success: parsed.success !== undefined ? Boolean(parsed.success) : false,
        message: parsed.message || 'Sin mensaje',
        data: parsed.data !== undefined ? parsed.data : null
      };
      
    } catch (error) {
      console.error('Error en safeJsonParse:', error);
      return {
        success: false,
        message: 'Error al procesar respuesta del servidor',
        data: null
      };
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'year' || name === 'copies' ? parseInt(value) || 0 : value
    }));
    setError(''); // Limpiar error al cambiar datos
  };

  /**
   * VALIDACIÓN ROBUSTA: Verificar datos antes de enviar
   */
  const validateFormData = () => {
    if (!formData.isbn.trim()) {
      setError('El ISBN es requerido');
      return false;
    }
    if (formData.isbn.trim().length < 10) {
      setError('El ISBN debe tener al menos 10 caracteres');
      return false;
    }
    if (!formData.title.trim()) {
      setError('El título es requerido');
      return false;
    }
    if (!formData.author.trim()) {
      setError('El autor es requerido');
      return false;
    }
    if (formData.year < 1000 || formData.year > new Date().getFullYear() + 10) {
      setError('El año debe ser válido');
      return false;
    }
    if (formData.copies < 1 || formData.copies > 100) {
      setError('El número de copias debe estar entre 1 y 100');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validar formulario antes de enviar
    if (!validateFormData()) {
      return;
    }

    setIsSubmitting(true);
    setError('');

    try {
      // Preparar datos con validación adicional
      const bookData = {
        isbn: formData.isbn.trim(),
        title: formData.title.trim(),
        author: formData.author.trim(),
        year: Number(formData.year),
        copies: Number(formData.copies)
      };

      console.log('Enviando datos del libro:', bookData);

      // Realizar petición con timeout
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 segundos timeout

      try {
        const response = await fetch('/api/books', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          body: JSON.stringify(bookData),
          signal: controller.signal
        });

        clearTimeout(timeoutId);

        console.log('Respuesta del servidor - Status:', response.status);
        console.log('Respuesta del servidor - OK:', response.ok);

        // CRÍTICO: Usar función segura para parsear JSON
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
      } catch (fetchError) {
        clearTimeout(timeoutId);
        
        if (fetchError instanceof Error && fetchError.name === 'AbortError') {
          setError('Timeout: El servidor tardó demasiado en responder');
        } else {
          throw fetchError; // Re-lanzar para el catch externo
        }
      }
      
    } catch (error) {
      console.error('Error:', error);
      
      // Manejo específico de diferentes tipos de errores
      if (error instanceof TypeError && error.message.includes('fetch')) {
        setError('Error de conexión. Verifica que el servidor esté funcionando.');
      } else if (error instanceof SyntaxError && error.message.includes('JSON')) {
        setError('Error de comunicación: Respuesta inválida del servidor.');
      } else if (error instanceof Error && error.message.includes('NetworkError')) {
        setError('Error de red. Verifica tu conexión a internet.');
      } else {
        const errorMessage = error instanceof Error ? error.message : 'Error desconocido';
        setError(`Error inesperado: ${errorMessage}`);
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