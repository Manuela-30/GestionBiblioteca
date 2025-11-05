import React, { useState, useEffect } from 'react';
import { Bell, X, CheckCircle, AlertCircle, Info } from 'lucide-react';

interface Notification {
  id: string;
  message: string;
  type: 'success' | 'warning' | 'info';
  timestamp: Date;
}

const Notifications: React.FC = () => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [unreadCount, setUnreadCount] = useState(0);

  /**
   * FUNCIÓN CRÍTICA: Manejo seguro de respuestas JSON
   * PREVIENE: "Unexpected end of JSON input"
   * GARANTIZA: Siempre retorna un objeto válido
   */
  const safeJsonParse = async (response: Response) => {
    try {
      // Paso 1: Obtener texto de la respuesta
      const text = await response.text();
      console.log('Notifications - Respuesta raw:', text);
      
      // Paso 2: Verificar si hay contenido
      if (!text || text.trim() === '') {
        console.warn('Notifications - Respuesta vacía del servidor');
        return {
          success: true,
          message: 'Sin notificaciones',
          data: []
        };
      }
      
      // Paso 3: Intentar parsear JSON
      const parsed = JSON.parse(text);
      console.log('Notifications - JSON parseado:', parsed);
      
      // Paso 4: Validar estructura esperada
      if (typeof parsed !== 'object' || parsed === null) {
        console.warn('Notifications - Estructura JSON inválida');
        return {
          success: false,
          message: 'Estructura de respuesta inválida',
          data: []
        };
      }
      
      // Paso 5: Asegurar propiedades requeridas
      return {
        success: parsed.success !== undefined ? Boolean(parsed.success) : true,
        message: parsed.message || 'Notificaciones cargadas',
        data: Array.isArray(parsed.data) ? parsed.data : []
      };
      
    } catch (error) {
      console.error('Notifications - Error en safeJsonParse:', error);
      return {
        success: false,
        message: 'Error al procesar notificaciones',
        data: []
      };
    }
  };

  useEffect(() => {
    // Cargar notificaciones iniciales
    loadNotifications();
    
    // Polling cada 30 segundos para nuevas notificaciones
    const interval = setInterval(loadNotifications, 30000);
    
    return () => clearInterval(interval);
  }, []);

  const loadNotifications = async () => {
    try {
      console.log('Cargando notificaciones...');
      
      // Realizar petición con timeout y headers apropiados
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 segundos timeout
      
      const response = await fetch('/api/notifications', {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      
      console.log('Notifications - Status:', response.status);
      console.log('Notifications - OK:', response.ok);
      
      // CRÍTICO: Usar función segura para parsear JSON
      const data = await safeJsonParse(response);
      console.log('Notifications - Datos parseados:', data);
      
      if (data.success && Array.isArray(data.data) && data.data.length > 0) {
        // Procesar notificaciones de forma segura
        const newNotifications = data.data
          .filter((message: any) => message && typeof message === 'string') // Filtrar mensajes válidos
          .map((message: string, index: number) => ({
          id: `${Date.now()}-${index}`,
          message: String(message), // Asegurar que sea string
          type: getNotificationType(message),
          timestamp: new Date()
        }));
        
        if (newNotifications.length > 0) {
          setNotifications(prev => [...newNotifications, ...prev].slice(0, 20)); // Mantener solo las últimas 20
          setUnreadCount(prev => prev + newNotifications.length);
          console.log(`Notifications - ${newNotifications.length} nuevas notificaciones agregadas`);
        }
      } else {
        console.log('Notifications - No hay nuevas notificaciones');
      }
    } catch (error) {
      console.error('Notifications - Error cargando:', error);
      
      // No mostrar error al usuario para notificaciones, solo log
      if (error instanceof Error && error.name === 'AbortError') {
        console.warn('Notifications - Timeout al cargar notificaciones');
      } else if (error instanceof TypeError && error.message.includes('fetch')) {
        console.warn('Notifications - Error de conexión al cargar notificaciones');
      } else {
        console.warn('Notifications - Error inesperado:', error);
      }
    }
  };

  const getNotificationType = (message: string | any): 'success' | 'warning' | 'info' => {
    // Asegurar que message sea string
    const messageStr = String(message || '').toLowerCase();
    
    if (messageStr.includes('agregado') || messageStr.includes('prestado') || messageStr.includes('devuelto')) {
      return 'success';
    }
    if (messageStr.includes('eliminado') || messageStr.includes('error')) {
      return 'warning';
    }
    return 'info';
  };

  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'success':
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'warning':
        return <AlertCircle className="h-4 w-4 text-orange-500" />;
      default:
        return <Info className="h-4 w-4 text-blue-500" />;
    }
  };

  const markAsRead = () => {
    setUnreadCount(0);
  };

  const clearNotification = (id: string) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  };

  const clearAllNotifications = () => {
    setNotifications([]);
    setUnreadCount(0);
  };

  const formatTime = (timestamp: Date) => {
    const now = new Date();
    const diff = now.getTime() - timestamp.getTime();
    const minutes = Math.floor(diff / 60000);
    
    if (minutes < 1) return 'Ahora';
    if (minutes < 60) return `${minutes}m`;
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `${hours}h`;
    return `${Math.floor(hours / 24)}d`;
  };

  return (
    <div className="relative">
      <button
        onClick={() => {
          setShowDropdown(!showDropdown);
          if (!showDropdown) markAsRead();
        }}
        className="relative p-2 text-gray-400 hover:text-gray-600 transition-colors"
      >
        <Bell className="h-6 w-6" />
        {unreadCount > 0 && (
          <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
            {unreadCount > 9 ? '9+' : unreadCount}
          </span>
        )}
      </button>

      {showDropdown && (
        <div className="absolute right-0 mt-2 w-80 bg-white rounded-xl shadow-lg border border-gray-200 z-50">
          <div className="p-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-900">Notificaciones</h3>
              {notifications.length > 0 && (
                <button
                  onClick={clearAllNotifications}
                  className="text-sm text-gray-500 hover:text-gray-700 transition-colors"
                >
                  Limpiar todo
                </button>
              )}
            </div>
          </div>

          <div className="max-h-96 overflow-y-auto">
            {notifications.length === 0 ? (
              <div className="p-6 text-center">
                <Bell className="h-12 w-12 text-gray-300 mx-auto mb-3" />
                <p className="text-gray-500">No hay notificaciones</p>
              </div>
            ) : (
              <div className="divide-y divide-gray-100">
                {notifications.map((notification) => (
                  <div key={notification.id} className="p-4 hover:bg-gray-50 transition-colors">
                    <div className="flex items-start space-x-3">
                      <div className="flex-shrink-0 mt-0.5">
                        {getNotificationIcon(notification.type)}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm text-gray-900">{notification.message}</p>
                        <p className="text-xs text-gray-500 mt-1">
                          {formatTime(notification.timestamp)}
                        </p>
                      </div>
                      <button
                        onClick={() => clearNotification(notification.id)}
                        className="flex-shrink-0 text-gray-400 hover:text-gray-600 transition-colors"
                      >
                        <X className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {notifications.length > 0 && (
            <div className="p-3 border-t border-gray-200 bg-gray-50 rounded-b-xl">
              <p className="text-xs text-gray-500 text-center">
                🔔 Sistema de notificaciones en tiempo real
              </p>
            </div>
          )}
        </div>
      )}

      {/* Overlay para cerrar dropdown */}
      {showDropdown && (
        <div
          className="fixed inset-0 z-40"
          onClick={() => setShowDropdown(false)}
        />
      )}
    </div>
  );
};

export default Notifications;