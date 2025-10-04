import { useProfile } from '@/hooks/useAuth';
import { useDocuments } from '@/hooks/useDocuments';
import { Link } from 'react-router-dom';
import { 
  FileText, 
  Upload, 
  Users, 
  TrendingUp,
  Clock,
  Star,
  FolderOpen,
  Brain,
  CheckCircle,
  Eye
} from 'lucide-react';

const DashboardPage = () => {
  const { data: user } = useProfile();
  const { data: documentsData } = useDocuments({ limit: 5 });

  const stats = [
    {
      name: 'Documentos totales',
      value: documentsData?.total || 0,
      icon: FileText,
      color: 'bg-blue-500',
    },
    {
      name: 'Cargas recientes',
      value: documentsData?.documents?.length || 0,
      icon: Upload,
      color: 'bg-green-500',
    },
    {
      name: 'Archivos compartidos',
      value: documentsData?.documents?.filter(doc => doc.is_public).length || 0,
      icon: Users,
      color: 'bg-purple-500',
    },
    {
      name: 'Almacenamiento utilizado',
      value: '2.4 GB',
      icon: TrendingUp,
      color: 'bg-orange-500',
    },
  ];

  return (
  <div className="space-y-6">
      {/* Welcome Header */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-700 rounded-lg shadow-lg p-6 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">
              ¡Bienvenido de nuevo, {user?.first_name}! 👋
            </h1>
            <p className="text-primary-100 mt-2">
              Sistema de Gestión Documental con Inteligencia Artificial
            </p>
          </div>
          <div className="flex space-x-3">
            <Link
              to="/bulk-import"
              className="bg-white text-primary-700 px-6 py-3 rounded-lg font-semibold hover:bg-primary-50 transition-colors flex items-center space-x-2 shadow-md"
            >
              <Brain className="h-5 w-5" />
              <span>Importación Inteligente</span>
            </Link>
            <Link
              to="/upload"
              className="bg-primary-500 text-white px-6 py-3 rounded-lg font-semibold hover:bg-primary-400 transition-colors flex items-center space-x-2"
            >
              <Upload className="h-5 w-5" />
              <span>Cargar Individual</span>
            </Link>
          </div>
        </div>
      </div>

      {/* Main Action Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Importación Masiva - Acción Principal */}
        <div className="bg-white rounded-2xl border-2 border-primary-200 bg-gradient-to-br from-primary-50 to-white shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
          <div className="p-8">
            <div className="flex items-center mb-6">
              <div className="bg-primary-100 p-4 rounded-2xl shadow-lg">
                <Brain className="h-10 w-10 text-primary-600" />
              </div>
              <div className="ml-6">
                <h3 className="text-2xl font-bold text-gray-900">Importación Inteligente</h3>
                <p className="text-gray-600 text-lg">Clasificación automática con IA</p>
              </div>
            </div>
            <p className="text-gray-700 mb-8 text-lg leading-relaxed">
              Sube múltiples documentos y nuestro sistema de Machine Learning los clasificará automáticamente en categorías como Contratos, Facturas, Informes, etc.
            </p>
            <div className="space-y-4 mb-8">
              <div className="flex items-center text-base text-gray-600">
                <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                <span>Clasificación automática con IA</span>
              </div>
              <div className="flex items-center text-base text-gray-600">
                <FolderOpen className="h-5 w-5 text-blue-500 mr-3" />
                <span>Distribución en carpetas organizadas</span>
              </div>
              <div className="flex items-center text-base text-gray-600">
                <Eye className="h-5 w-5 text-purple-500 mr-3" />
                <span>Revisión y aprobación manual</span>
              </div>
            </div>
            <Link
              to="/bulk-import"
              className="btn-primary w-full flex items-center justify-center space-x-3 py-4 text-lg font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
            >
              <Brain className="h-6 w-6" />
              <span>Comenzar Importación Inteligente</span>
            </Link>
          </div>
        </div>

        {/* Carga Individual */}
        <div className="bg-white rounded-2xl shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
          <div className="p-8">
            <div className="flex items-center mb-6">
              <div className="bg-green-100 p-4 rounded-2xl shadow-lg">
                <Upload className="h-10 w-10 text-green-600" />
              </div>
              <div className="ml-6">
                <h3 className="text-2xl font-bold text-gray-900">Carga Individual</h3>
                <p className="text-gray-600 text-lg">Para documentos específicos</p>
              </div>
            </div>
            <p className="text-gray-700 mb-8 text-lg leading-relaxed">
              Sube un documento individual cuando necesites control total sobre su clasificación y metadatos.
            </p>
            <Link
              to="/upload"
              className="btn-secondary w-full flex items-center justify-center space-x-3 py-4 text-lg font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
            >
              <Upload className="h-6 w-6" />
              <span>Cargar Documento Individual</span>
            </Link>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div key={stat.name} className="bg-white rounded-2xl p-8 shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border border-gray-100">
              <div className="flex items-center">
                <div className={`${stat.color} rounded-2xl p-4 shadow-lg`}>
                  <Icon className="h-8 w-8 text-white" />
                </div>
                <div className="ml-6">
                  <p className="text-base font-semibold text-gray-500">{stat.name}</p>
                  <p className="text-3xl font-bold text-gray-900">{stat.value}</p>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Recent Documents */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white rounded-2xl shadow-xl border border-gray-100">
          <div className="p-8">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-2xl font-bold text-gray-900">Documentos recientes</h3>
              <Link
                to="/documents"
                className="text-primary-600 hover:text-primary-700 font-semibold text-lg transition-colors"
              >
                Ver todos →
              </Link>
            </div>
            
            {documentsData?.documents && documentsData.documents.length > 0 ? (
              <div className="space-y-4">
                {documentsData.documents.slice(0, 5).map((doc) => (
                  <Link
                    key={doc.id}
                    to={`/documents/${doc.id}`}
                    className="flex items-center p-4 rounded-xl hover:bg-gray-50 transition-all duration-200 transform hover:scale-105 border border-gray-100 hover:border-primary-200"
                  >
                    <FileText className="h-10 w-10 text-primary-500 flex-shrink-0" />
                    <div className="ml-4 flex-1 min-w-0">
                      <p className="text-lg font-semibold text-gray-900 truncate">
                        {doc.title}
                      </p>
                      <p className="text-base text-gray-500 truncate">
                        {doc.category} • {new Date(doc.updated_at).toLocaleDateString()}
                      </p>
                    </div>
                    <div className="flex items-center space-x-3">
                      {doc.is_public && (
                        <Users className="h-5 w-5 text-gray-400" />
                      )}
                      <Clock className="h-5 w-5 text-gray-400" />
                    </div>
                  </Link>
                ))}
              </div>
            ) : (
              <div className="text-center py-12">
                <FileText className="mx-auto h-16 w-16 text-gray-400" />
                <h3 className="mt-4 text-xl font-semibold text-gray-900">No hay documentos</h3>
                <p className="mt-2 text-lg text-gray-500">
                  Comience importando documentos con nuestro sistema inteligente.
                </p>
                <div className="mt-8">
                  <Link
                    to="/bulk-import"
                    className="btn-primary text-lg px-8 py-4 rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
                  >
                    <Brain className="h-5 w-5 mr-3" />
                    Importar con IA
                  </Link>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-2xl shadow-xl border border-gray-100">
          <div className="p-8">
            <h3 className="text-2xl font-bold text-gray-900 mb-6">Acciones rápidas</h3>
            <div className="space-y-4">
              <Link
                to="/bulk-import"
                className="flex items-center p-6 rounded-xl border-2 border-primary-200 bg-gradient-to-r from-primary-50 to-primary-100 hover:from-primary-100 hover:to-primary-200 transition-all duration-200 transform hover:scale-105 shadow-lg hover:shadow-xl"
              >
                <Brain className="h-8 w-8 text-primary-600" />
                <div className="ml-6">
                  <p className="text-lg font-semibold text-gray-900">Importación Inteligente</p>
                  <p className="text-base text-gray-600">Clasificación automática con IA</p>
                </div>
              </Link>

              <Link
                to="/documents"
                className="flex items-center p-6 rounded-xl border border-gray-200 hover:bg-gray-50 transition-all duration-200 transform hover:scale-105 shadow-lg hover:shadow-xl"
              >
                <FileText className="h-8 w-8 text-green-500" />
                <div className="ml-6">
                  <p className="text-lg font-semibold text-gray-900">Ver documentos</p>
                  <p className="text-base text-gray-600">Ver y administrar todos los archivos</p>
                </div>
              </Link>

              <Link
                to="/profile"
                className="flex items-center p-6 rounded-xl border border-gray-200 hover:bg-gray-50 transition-all duration-200 transform hover:scale-105 shadow-lg hover:shadow-xl"
              >
                <Star className="h-8 w-8 text-purple-500" />
                <div className="ml-6">
                  <p className="text-lg font-semibold text-gray-900">Actualizar perfil</p>
                  <p className="text-base text-gray-600">Administre la configuración de su cuenta</p>
                </div>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;