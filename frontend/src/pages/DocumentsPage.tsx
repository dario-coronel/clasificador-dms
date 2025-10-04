import { useState } from 'react';
import { useDocuments } from '@/hooks/useDocuments';
import { Link } from 'react-router-dom';
import { 
  FileText, 
  Search, 
  Filter, 
  Download, 
  Eye,
  Calendar,
  User,
  Tag,
  ChevronDown,
  ChevronUp,
  X,
  Building2,
  Hash
} from 'lucide-react';

const DocumentsPage = () => {
  const [showAdvancedFilters, setShowAdvancedFilters] = useState(false);
  const [filters, setFilters] = useState({
    search: '',
    category: '',
    dateFrom: '',
    dateTo: '',
    provider: '',
    cuit: '',
    documentType: '',
    limit: 10,
    skip: 0,
  });

  const { data: documentsData, isLoading } = useDocuments(filters);

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFilters({
      ...filters,
      search: e.target.value,
      skip: 0, // Reset pagination
    });
  };

  const handleCategoryChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setFilters({
      ...filters,
      category: e.target.value,
      skip: 0, // Reset pagination
    });
  };

  const handleFilterChange = (field: string, value: string) => {
    setFilters({
      ...filters,
      [field]: value,
      skip: 0, // Reset pagination
    });
  };

  const clearFilters = () => {
    setFilters({
      search: '',
      category: '',
      dateFrom: '',
      dateTo: '',
      provider: '',
      cuit: '',
      documentType: '',
      limit: 10,
      skip: 0,
    });
  };

  const hasActiveFilters = filters.dateFrom || filters.dateTo || filters.provider || filters.cuit || filters.documentType;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Documentos</h1>
          <p className="text-gray-600">
            Gestione y organice sus documentos
          </p>
        </div>
        <Link
          to="/upload"
          className="btn-primary"
        >
          Cargar documento
        </Link>
      </div>

      {/* Filters */}
      <div className="card p-6">
        {/* Basic Filters */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="md:col-span-2">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Buscar por título, descripción o contenido..."
                value={filters.search}
                onChange={handleSearchChange}
                className="input pl-10 w-full"
              />
            </div>
          </div>
          
          <div>
            <div className="relative">
              <Tag className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <select
                value={filters.category}
                onChange={handleCategoryChange}
                className="input pl-10 w-full"
              >
                <option value="">Todas las categorías</option>
                <option value="Contrato">Contrato</option>
                <option value="Contrato de Granos">Contrato de Granos</option>
                <option value="Informe">Informe</option>
                <option value="Factura">Factura</option>
                <option value="Remito">Remito</option>
                <option value="Nota de Crédito">Nota de Crédito</option>
                <option value="Nota de Débito">Nota de Débito</option>
                <option value="Política">Política</option>
                <option value="Manual">Manual</option>
                <option value="Orden de Compra">Orden de Compra</option>
                <option value="Recibo">Recibo</option>
                <option value="Otro">Otro</option>
              </select>
            </div>
          </div>
        </div>

        {/* Toggle Advanced Filters Button */}
        <div className="mt-4 flex items-center justify-between">
          <button
            onClick={() => setShowAdvancedFilters(!showAdvancedFilters)}
            className="flex items-center text-sm text-primary-600 hover:text-primary-700 font-medium transition-colors"
          >
            <Filter className="h-4 w-4 mr-2" />
            Filtros avanzados
            {showAdvancedFilters ? (
              <ChevronUp className="h-4 w-4 ml-1" />
            ) : (
              <ChevronDown className="h-4 w-4 ml-1" />
            )}
          </button>

          {hasActiveFilters && (
            <button
              onClick={clearFilters}
              className="flex items-center text-sm text-gray-600 hover:text-gray-700 font-medium transition-colors"
            >
              <X className="h-4 w-4 mr-1" />
              Limpiar filtros
            </button>
          )}
        </div>

        {/* Advanced Filters */}
        {showAdvancedFilters && (
          <div className="mt-4 pt-4 border-t border-gray-200">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {/* Date From */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <Calendar className="inline h-4 w-4 mr-1" />
                  Fecha desde
                </label>
                <input
                  type="date"
                  value={filters.dateFrom}
                  onChange={(e) => handleFilterChange('dateFrom', e.target.value)}
                  className="input w-full"
                />
              </div>

              {/* Date To */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <Calendar className="inline h-4 w-4 mr-1" />
                  Fecha hasta
                </label>
                <input
                  type="date"
                  value={filters.dateTo}
                  onChange={(e) => handleFilterChange('dateTo', e.target.value)}
                  className="input w-full"
                />
              </div>

              {/* Provider */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <Building2 className="inline h-4 w-4 mr-1" />
                  Proveedor
                </label>
                <input
                  type="text"
                  placeholder="Nombre del proveedor..."
                  value={filters.provider}
                  onChange={(e) => handleFilterChange('provider', e.target.value)}
                  className="input w-full"
                />
              </div>

              {/* CUIT */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <Hash className="inline h-4 w-4 mr-1" />
                  CUIT
                </label>
                <input
                  type="text"
                  placeholder="XX-XXXXXXXX-X"
                  value={filters.cuit}
                  onChange={(e) => handleFilterChange('cuit', e.target.value)}
                  className="input w-full"
                  maxLength={13}
                />
              </div>

              {/* Document Type */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <FileText className="inline h-4 w-4 mr-1" />
                  Tipo de documento
                </label>
                <select
                  value={filters.documentType}
                  onChange={(e) => handleFilterChange('documentType', e.target.value)}
                  className="input w-full"
                >
                  <option value="">Todos los tipos</option>
                  <option value="pdf">PDF</option>
                  <option value="word">Word</option>
                  <option value="excel">Excel</option>
                  <option value="image">Imagen</option>
                  <option value="text">Texto</option>
                  <option value="other">Otro</option>
                </select>
              </div>
            </div>

            {/* Active Filters Summary */}
            {hasActiveFilters && (
              <div className="mt-4 pt-4 border-t border-gray-100">
                <div className="flex flex-wrap gap-2">
                  <span className="text-sm text-gray-600 font-medium">Filtros activos:</span>
                  {filters.dateFrom && (
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                      Desde: {new Date(filters.dateFrom).toLocaleDateString()}
                      <button
                        onClick={() => handleFilterChange('dateFrom', '')}
                        className="ml-2 hover:text-primary-900"
                      >
                        <X className="h-3 w-3" />
                      </button>
                    </span>
                  )}
                  {filters.dateTo && (
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                      Hasta: {new Date(filters.dateTo).toLocaleDateString()}
                      <button
                        onClick={() => handleFilterChange('dateTo', '')}
                        className="ml-2 hover:text-primary-900"
                      >
                        <X className="h-3 w-3" />
                      </button>
                    </span>
                  )}
                  {filters.provider && (
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                      Proveedor: {filters.provider}
                      <button
                        onClick={() => handleFilterChange('provider', '')}
                        className="ml-2 hover:text-primary-900"
                      >
                        <X className="h-3 w-3" />
                      </button>
                    </span>
                  )}
                  {filters.cuit && (
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                      CUIT: {filters.cuit}
                      <button
                        onClick={() => handleFilterChange('cuit', '')}
                        className="ml-2 hover:text-primary-900"
                      >
                        <X className="h-3 w-3" />
                      </button>
                    </span>
                  )}
                  {filters.documentType && (
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                      Tipo: {filters.documentType.toUpperCase()}
                      <button
                        onClick={() => handleFilterChange('documentType', '')}
                        className="ml-2 hover:text-primary-900"
                      >
                        <X className="h-3 w-3" />
                      </button>
                    </span>
                  )}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Documents Grid */}
      <div className="card">
        {isLoading ? (
          <div className="p-6 text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
            <p className="mt-2 text-sm text-gray-500">Cargando documentos...</p>
          </div>
        ) : documentsData?.documents && documentsData.documents.length > 0 ? (
          <div className="divide-y divide-gray-200">
            {documentsData.documents.map((doc) => (
              <div key={doc.id} className="p-6 hover:bg-gray-50 transition-colors">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4 flex-1">
                    <div className="flex-shrink-0">
                      <FileText className="h-10 w-10 text-primary-500" />
                    </div>
                    
                    <div className="flex-1 min-w-0">
                      <h3 className="text-lg font-medium text-gray-900 truncate">
                        {doc.title}
                      </h3>
                      
                      {doc.description && (
                        <p className="text-sm text-gray-600 mt-1 line-clamp-2">
                          {doc.description}
                        </p>
                      )}
                      
                      <div className="flex items-center space-x-4 mt-2 text-xs text-gray-500">
                        <div className="flex items-center">
                          <User className="h-3 w-3 mr-1" />
                          {doc.owner.first_name} {doc.owner.last_name}
                        </div>
                        
                        <div className="flex items-center">
                          <Calendar className="h-3 w-3 mr-1" />
                          {new Date(doc.created_at).toLocaleDateString()}
                        </div>
                        
                        {doc.category && (
                          <div className="flex items-center">
                            <Tag className="h-3 w-3 mr-1" />
                            {doc.category}
                          </div>
                        )}
                        
                        <div className="text-xs bg-gray-100 px-2 py-1 rounded">
                          {(doc.file_size / 1024 / 1024).toFixed(2)} MB
                        </div>
                        
                        {doc.is_public && (
                          <div className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">
                            Public
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <Link
                      to={`/documents/${doc.id}`}
                      className="btn-outline p-2"
                      title="View document"
                    >
                      <Eye className="h-4 w-4" />
                    </Link>
                    
                    <button
                      className="btn-outline p-2"
                      title="Download document"
                    >
                      <Download className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="p-12 text-center">
            <FileText className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">No se encontraron documentos</h3>
            <p className="mt-1 text-sm text-gray-500">
              {filters.search || filters.category 
                ? 'Intente ajustar sus filtros de búsqueda.'
                : 'Comience cargando su primer documento.'
              }
            </p>
            {!filters.search && !filters.category && (
              <div className="mt-6">
                <Link
                  to="/upload"
                  className="btn-primary"
                >
                  Cargar documento
                </Link>
              </div>
            )}
          </div>
        )}
        
        {/* Pagination */}
        {documentsData && documentsData.total > documentsData.documents.length && (
          <div className="px-6 py-4 border-t border-gray-200">
            <div className="flex items-center justify-between">
              <div className="text-sm text-gray-700">
                Mostrando {documentsData.documents.length} de {documentsData.total} resultados
              </div>
              <div className="flex space-x-2">
                <button
                  disabled={filters.skip === 0}
                  onClick={() => setFilters({
                    ...filters,
                    skip: Math.max(0, filters.skip - filters.limit)
                  })}
                  className="btn-outline disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Anterior
                </button>
                <button
                  disabled={filters.skip + filters.limit >= documentsData.total}
                  onClick={() => setFilters({
                    ...filters,
                    skip: filters.skip + filters.limit
                  })}
                  className="btn-outline disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Siguiente
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DocumentsPage;