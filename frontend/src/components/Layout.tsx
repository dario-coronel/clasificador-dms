import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useLogout, useProfile } from '@/hooks/useAuth';
import { 
  FileText, 
  Home, 
  Upload, 
  User, 
  LogOut, 
  Menu, 
  X,
  Search,
  Bell
} from 'lucide-react';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();
  const { data: user, isError } = useProfile();
  const logoutMutation = useLogout();

  const navigation = [
    { name: 'Inicio', href: '/dashboard', icon: Home },
    { name: 'Documentos', href: '/documents', icon: FileText },
    { name: 'Cargar documento', href: '/upload', icon: Upload },
    { name: 'Importación masiva', href: '/bulk-import', icon: Upload },
    { name: 'Perfil', href: '/profile', icon: User },
    { name: 'Ayuda', href: '/help', icon: Bell },
  ];

  const handleLogout = () => {
    logoutMutation.mutate();
  };

  const isActive = (path: string) => location.pathname === path;

  return (
    <div className="min-h-screen flex">
      {/* Mobile sidebar backdrop */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 z-40 bg-gray-600 bg-opacity-75 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={`
        fixed inset-y-0 left-0 z-50 w-72 bg-white shadow-xl transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0 border-r border-gray-200
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
      `} aria-label="Menú lateral">
        <div className="flex items-center justify-between h-20 px-8 border-b border-gray-200 bg-gradient-to-r from-primary-600 to-primary-700">
          <h1 className="text-2xl font-bold text-white tracking-wide">EDMS</h1>
          <button
            className="lg:hidden text-white hover:text-primary-100"
            onClick={() => setSidebarOpen(false)}
            aria-label="Cerrar menú"
          >
            <X className="h-7 w-7" />
          </button>
        </div>

        <nav className="mt-8">
          <div className="px-4 space-y-1">
            {navigation.map((item, idx) => {
              const Icon = item.icon;
              return (
                <>
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`
                      group flex items-center px-6 py-4 text-base font-medium rounded-xl transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2
                      ${isActive(item.href)
                        ? 'bg-primary-100 text-primary-700 border-r-4 border-primary-500 shadow-md transform scale-[1.02]'
                        : 'text-gray-700 hover:bg-white hover:shadow-md hover:transform hover:scale-[1.01] hover:border-r-4 hover:border-primary-300'
                      }
                    `}
                    aria-current={isActive(item.href) ? 'page' : undefined}
                    onClick={() => setSidebarOpen(false)}
                  >
                    <Icon className={`mr-4 h-6 w-6 transition-colors ${
                      isActive(item.href) 
                        ? 'text-primary-600' 
                        : 'text-gray-500 group-hover:text-primary-500'
                    }`} />
                    <span className="truncate">{item.name}</span>
                  </Link>
                  {/* Divider visual entre secciones principales */}
                  {idx === 0 || idx === navigation.length - 2 ? (
                    <div className="my-4 border-t border-gray-200"></div>
                  ) : null}
                </>
              );
            })}
          </div>
        </nav>

        {/* Sección de usuario */}
        <div className="absolute bottom-0 left-0 right-0 p-6 border-t border-gray-200 bg-gradient-to-r from-gray-50 to-white">
          <div className="flex items-center bg-white rounded-xl p-4 shadow-sm border border-gray-200">
            <div className="flex-shrink-0">
              <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-primary-500 to-primary-600 flex items-center justify-center shadow-md">
                <span className="text-white text-lg font-bold">
                  {user?.first_name?.[0]}{user?.last_name?.[0]}
                </span>
              </div>
            </div>
            <div className="ml-4 flex-1 min-w-0">
              <p className="text-base font-semibold text-gray-900 truncate">
                {user?.first_name} {user?.last_name}
              </p>
              <p className="text-sm text-gray-500 truncate">{user?.email}</p>
            </div>
            <button
              onClick={handleLogout}
              className="ml-3 p-2 rounded-lg text-gray-400 hover:text-red-500 hover:bg-red-50 transition-colors"
              title="Cerrar sesión"
              aria-label="Cerrar sesión"
            >
              <LogOut className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col bg-gradient-to-br from-gray-50 to-gray-100">
        {/* Top header con barra de búsqueda */}
        <div className="bg-white shadow-sm border-b border-gray-200 h-20">
          <div className="flex items-center h-full px-8">
            <button
              className="lg:hidden mr-4 p-2 rounded-lg text-gray-600 hover:text-primary-600 hover:bg-primary-50 transition-colors"
              onClick={() => setSidebarOpen(true)}
              aria-label="Abrir menú"
            >
              <Menu className="h-6 w-6" />
            </button>

            {/* Barra de búsqueda */}
            <div className="flex-1 max-w-2xl">
              <div className="relative">
                <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                <input
                  type="text"
                  placeholder="Buscar documentos, categorías, contenido..."
                  className="w-full pl-12 pr-4 py-2.5 border border-gray-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all text-sm"
                  aria-label="Buscar documentos"
                />
              </div>
            </div>

            <div className="flex items-center space-x-4 ml-6">
              <button className="p-2 rounded-lg text-gray-600 hover:text-primary-600 hover:bg-primary-50 transition-colors relative">
                <Bell className="h-5 w-5" />
                <span className="absolute top-0 right-0 h-2 w-2 bg-red-500 rounded-full"></span>
              </button>
            </div>
          </div>
        </div>

        {/* Page content */}
        <main className="flex-1 overflow-auto">
          <div className="py-8">
            <div className="max-w-7xl mx-auto px-8">
              {children}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default Layout;