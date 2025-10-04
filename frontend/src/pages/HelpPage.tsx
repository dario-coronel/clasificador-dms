import React from 'react';

const HelpPage: React.FC = () => (
  <div className="max-w-2xl mx-auto py-8">
    <h1 className="text-2xl font-bold mb-4 text-primary-700">Ayuda y Preguntas Frecuentes</h1>
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-2">¿Cómo cargar un documento?</h2>
        <p className="text-gray-700">Seleccione la opción "Cargar documento" en el menú lateral y complete el formulario con los datos requeridos.</p>
      </div>
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-2">¿Cómo buscar documentos?</h2>
        <p className="text-gray-700">Utilice la barra de búsqueda en la parte superior para filtrar documentos por título, categoría o etiquetas.</p>
      </div>
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-2">¿Cómo editar mi perfil?</h2>
        <p className="text-gray-700">Acceda a la sección "Perfil" y haga clic en "Editar perfil" para modificar su información personal.</p>
      </div>
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-2">¿A quién contactar en caso de problemas?</h2>
        <p className="text-gray-700">Comuníquese con el administrador del sistema o escriba a soporte@empresa.com.</p>
      </div>
    </div>
  </div>
);

export default HelpPage;
