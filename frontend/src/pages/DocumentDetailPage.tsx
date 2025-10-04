import { useParams, useNavigate } from 'react-router-dom';
import { useDocument, useDownloadDocument } from '@/hooks/useDocuments';
import { 
  FileText, 
  Download, 
  Edit, 
  Share, 
  Calendar, 
  User, 
  Tag,
  ArrowLeft,
  Eye
} from 'lucide-react';

const DocumentDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: document, isLoading } = useDocument(Number(id));
  const downloadMutation = useDownloadDocument();

  const handleDownload = () => {
    if (document) {
      downloadMutation.mutate(document.id);
    }
  };

  if (isLoading) {
    return (
      <div className="text-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
  <p className="mt-2 text-sm text-gray-500">Cargando documento...</p>
      </div>
    );
  }

  if (!document) {
    return (
      <div className="text-center py-8">
        <FileText className="mx-auto h-12 w-12 text-gray-400" />
        <h3 className="mt-2 text-sm font-medium text-gray-900">Documento no encontrado</h3>
        <p className="mt-1 text-sm text-gray-500">
          El documento que busca no existe o no tiene permiso para verlo.
        </p>
        <div className="mt-6">
          <button
            onClick={() => navigate('/documents')}
            className="btn-primary"
          >
            Volver a documentos
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <button
            onClick={() => navigate('/documents')}
            className="btn-outline p-2"
          >
            <ArrowLeft className="h-4 w-4" />
          </button>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{document.title}</h1>
            <p className="text-gray-600">Detalles del documento</p>
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          <button
            onClick={handleDownload}
            disabled={downloadMutation.isPending}
            className="btn-outline flex items-center space-x-2"
          >
            <Download className="h-4 w-4" />
            <span>{downloadMutation.isPending ? 'Descargando...' : 'Descargar'}</span>
          </button>
          
          <button className="btn-outline flex items-center space-x-2">
            <Share className="h-4 w-4" />
            <span>Compartir</span>
          </button>
          
          <button className="btn-primary flex items-center space-x-2">
            <Edit className="h-4 w-4" />
            <span>Editar</span>
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Document Preview */}
        <div className="lg:col-span-2">
          <div className="card">
            <div className="p-6">
              <div className="flex items-center justify-center h-96 bg-gray-50 rounded-lg">
                <div className="text-center">
                  <FileText className="mx-auto h-16 w-16 text-gray-400" />
                  <h3 className="mt-4 text-lg font-medium text-gray-900">{document.filename}</h3>
                  <p className="mt-2 text-sm text-gray-500">
                    {document.mime_type} • {(document.file_size / 1024 / 1024).toFixed(2)} MB
                  </p>
                  <div className="mt-6">
                    <button
                      onClick={handleDownload}
                      className="btn-primary flex items-center space-x-2 mx-auto"
                    >
                      <Eye className="h-4 w-4" />
                      <span>Ver documento</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Document Information */}
        <div className="space-y-6">
          {/* Basic Info */}
          <div className="card">
            <div className="p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Información del documento</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-500">Título</label>
                  <p className="mt-1 text-sm text-gray-900">{document.title}</p>
                </div>
                
                {document.description && (
                  <div>
                    <label className="block text-sm font-medium text-gray-500">Descripción</label>
                    <p className="mt-1 text-sm text-gray-900">{document.description}</p>
                  </div>
                )}
                
                <div>
                  <label className="block text-sm font-medium text-gray-500">Nombre de archivo</label>
                  <p className="mt-1 text-sm text-gray-900 font-mono">{document.filename}</p>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-500">Tamaño de archivo</label>
                  <p className="mt-1 text-sm text-gray-900">
                    {(document.file_size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-500">Tipo de archivo</label>
                  <p className="mt-1 text-sm text-gray-900">{document.mime_type}</p>
                </div>
                
                {document.category && (
                  <div>
                    <label className="block text-sm font-medium text-gray-500">Categoría</label>
                    <div className="mt-1 flex items-center">
                      <Tag className="h-4 w-4 text-gray-400 mr-1" />
                      <span className="text-sm text-gray-900">{document.category}</span>
                    </div>
                  </div>
                )}
                
                {document.tags && (
                  <div>
                    <label className="block text-sm font-medium text-gray-500">Etiquetas</label>
                    <div className="mt-1 flex flex-wrap gap-1">
                      {document.tags.split(',').map((tag, index) => (
                        <span
                          key={index}
                          className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800"
                        >
                          {tag.trim()}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                
                <div>
                  <label className="block text-sm font-medium text-gray-500">Visibilidad</label>
                  <div className="mt-1">
                    <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                      document.is_public ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                    }`}>
                      {document.is_public ? 'Público' : 'Privado'}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Metadata */}
          <div className="card">
            <div className="p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Metadatos</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-500">Propietario</label>
                  <div className="mt-1 flex items-center">
                    <User className="h-4 w-4 text-gray-400 mr-1" />
                    <span className="text-sm text-gray-900">
                      {document.owner.first_name} {document.owner.last_name}
                    </span>
                  </div>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-500">Creado</label>
                  <div className="mt-1 flex items-center">
                    <Calendar className="h-4 w-4 text-gray-400 mr-1" />
                    <span className="text-sm text-gray-900">
                      {new Date(document.created_at).toLocaleString()}
                    </span>
                  </div>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-500">Última modificación</label>
                  <div className="mt-1 flex items-center">
                    <Calendar className="h-4 w-4 text-gray-400 mr-1" />
                    <span className="text-sm text-gray-900">
                      {new Date(document.updated_at).toLocaleString()}
                    </span>
                  </div>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-500">Versión</label>
                  <p className="mt-1 text-sm text-gray-900">v{document.current_version}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DocumentDetailPage;