import React, { useState } from 'react';
import { UserPlus, Loader } from 'lucide-react';

interface AddUserFormProps {
  onSuccess: () => void;
  onCancel: () => void;
}

const AddUserForm: React.FC<AddUserFormProps> = ({ onSuccess, onCancel }) => {
  const [formData, setFormData] = useState({
    user_id: '',
    name: '',
    email: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    setError(''); // Limpiar error al cambiar datos
  };

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

  const validateEmail = (email: string) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validaciones del frontend
    if (!formData.user_id.trim()) {
      setError('El ID de usuario es requerido');
      return;
    }
    if (!formData.name.trim()) {
      setError('El nombre es requerido');
      return;
    }
    if (!formData.email.trim()) {
      setError('El email es requerido');
      return;
    }
    if (!validateEmail(formData.email)) {
      setError('El email no tiene un formato válido');
      return;
    }

    setIsSubmitting(true);
    setError('');

    try {
      // Preparar datos para envío
      const userData = {
        user_id: formData.user_id.trim(),
        name: formData.name.trim(),
        email: formData.email.trim()
      };

      console.log('Enviando datos del usuario:', userData);

      const response = await fetch('/api/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      console.log('Respuesta del servidor - Status:', response.status);

      // Usar función segura para parsear JSON
      const data = await safeJsonParse(response);
      console.log('Datos parseados:', data);

      if (data.success) {
        console.log('Usuario agregado exitosamente:', data.data);
        onSuccess();
      } else {
        const errorMessage = data.message || 'Error desconocido al agregar el usuario';
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

  const generateUserId = () => {
    const timestamp = Date.now().toString().slice(-6);
    const random = Math.random().toString(36).substring(2, 5).toUpperCase();
    setFormData(prev => ({
      ...prev,
      user_id: `U${timestamp}${random}`
    }));
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
              <h3 className="text-sm font-medium text-red-800">Error al registrar usuario</h3>
              <p className="text-sm text-red-600 mt-1">{error}</p>
            </div>
          </div>
        </div>
      )}

      <div className="space-y-6">
        <div>
          <label htmlFor="user_id" className="block text-sm font-medium text-gray-700 mb-2">
            ID de Usuario *
          </label>
          <div className="flex space-x-2">
            <input
              type="text"
              id="user_id"
              name="user_id"
              value={formData.user_id}
              onChange={handleChange}
              placeholder="U001, USER123, etc."
              className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              required
              disabled={isSubmitting}
            />
            <button
              type="button"
              onClick={generateUserId}
              disabled={isSubmitting}
              className="px-3 py-2 text-sm bg-gray-100 hover:bg-gray-200 border border-gray-300 rounded-lg transition-colors"
            >
              Generar
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-1">
            Identificador único para búsqueda O(log n) en BST
          </p>
        </div>

        <div>
          <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
            Nombre Completo *
          </label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="Juan Pérez García"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            required
            disabled={isSubmitting}
          />
        </div>

        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
            Correo Electrónico *
          </label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="usuario@ejemplo.com"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            required
            disabled={isSubmitting}
          />
        </div>
      </div>

      <div className="bg-green-50 border border-green-200 rounded-lg p-4">
        <div className="flex items-start space-x-2">
          <UserPlus className="h-5 w-5 text-green-600 mt-0.5" />
          <div>
            <h4 className="text-sm font-medium text-green-900">Registro Optimizado</h4>
            <p className="text-sm text-green-700 mt-1">
              El usuario se indexará por ID, nombre y email para búsquedas rápidas y gestión eficiente.
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
          className="px-4 py-2 text-sm font-medium text-white bg-green-600 border border-transparent rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
        >
          {isSubmitting ? (
            <>
              <Loader className="h-4 w-4 animate-spin" />
              <span>Registrando...</span>
            </>
          ) : (
            <>
              <UserPlus className="h-4 w-4" />
              <span>Registrar Usuario</span>
            </>
          )}
        </button>
      </div>
    </form>
  );
};

export default AddUserForm;