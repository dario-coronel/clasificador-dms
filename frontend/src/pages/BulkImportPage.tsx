import Button from '@/components/Button';
import Card from '@/components/Card';
import { useToast } from '@/components/ToastProvider';
import { bulkProcessDocuments, checkMLHealth, ProcessedDocument } from '@/services/ml';
import {
  AlertTriangle,
  Brain,
  CheckCircle,
  Eye,
  FileText,
  Save,
  XCircle
} from 'lucide-react';
import React, { useEffect, useState } from 'react';

interface DocumentReview extends ProcessedDocument {
  approved?: boolean;
  manualCategory?: string;
  reviewed?: boolean;
}

const BulkImportPage: React.FC = () => {
  const [selectedFiles, setSelectedFiles] = useState<FileList | null>(null);
  const [importing, setImporting] = useState(false);
  const [results, setResults] = useState<DocumentReview[]>([]);
  const [reviewMode, setReviewMode] = useState(false);
  const [saving, setSaving] = useState(false);
  const [mlAvailable, setMlAvailable] = useState<boolean>(false);
  const [checkingML, setCheckingML] = useState(true);
  const [selectedDocument, setSelectedDocument] = useState<DocumentReview | null>(null);
  const { showToast } = useToast();

  // Verificar si el servicio ML está disponible
  useEffect(() => {
    checkMLHealth()
      .then(available => {
        setMlAvailable(available);
        if (!available) {
          showToast('El servicio de clasificación ML no está disponible. Inicia el servidor ML en el puerto 8002.', 'error');
        }
      })
      .finally(() => setCheckingML(false));
  }, []);

  const handleFolderSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSelectedFiles(e.target.files);
    setResults([]);
    setReviewMode(false);
  };

  const handleImport = async () => {
    if (!selectedFiles || selectedFiles.length === 0) {
      showToast('Seleccione una carpeta con archivos para importar.', 'error');
      return;
    }

    if (!mlAvailable) {
      showToast('El servicio ML no está disponible. No se puede procesar los archivos.', 'error');
      return;
    }

    setImporting(true);
    setResults([]);
    setReviewMode(false);

    try {
      // Convertir FileList a Array
      const filesArray = Array.from(selectedFiles);
      
      // Procesar archivos con el backend ML
      const result = await bulkProcessDocuments(filesArray);
      
      // Convertir resultados para revisión
      const reviewResults: DocumentReview[] = result.results.map(doc => ({
        ...doc,
        approved: doc.success && (doc.confidence || 0) > 0.7, // Auto-aprobar si confianza > 70%
        reviewed: false
      }));
      
      setResults(reviewResults);
      setReviewMode(true);
      
      if (result.processed > 0) {
        showToast(
          `Procesados ${result.processed} de ${result.total_files} archivos. Revisa las clasificaciones antes de guardar.`,
          'success'
        );
      }
      
      if (result.failed > 0) {
        showToast(
          `${result.failed} archivos no pudieron ser procesados.`,
          'error'
        );
      }
    } catch (error) {
      console.error('Error al procesar archivos:', error);
      showToast('Error al procesar los archivos. Verifica que el servidor ML esté corriendo.', 'error');
    } finally {
      setImporting(false);
    }
  };

  const handleApproveDocument = (index: number) => {
    setResults(prev => prev.map((doc, i) => 
      i === index ? { ...doc, approved: true, reviewed: true } : doc
    ));
  };

  const handleRejectDocument = (index: number) => {
    setResults(prev => prev.map((doc, i) => 
      i === index ? { ...doc, approved: false, reviewed: true } : doc
    ));
  };

  const handleChangeCategory = (index: number, newCategory: string) => {
    setResults(prev => prev.map((doc, i) => 
      i === index ? { ...doc, manualCategory: newCategory, reviewed: true } : doc
    ));
  };

  const handleSaveDocuments = async () => {
    const approvedDocs = results.filter(doc => doc.approved);
    if (approvedDocs.length === 0) {
      showToast('No hay documentos aprobados para guardar.', 'error');
      return;
    }

    setSaving(true);
    try {
      // Entrenar el clasificador ML con los textos y categorías corregidas
      const texts = approvedDocs.map(doc => doc.text || doc.text_preview || '');
      const labels = approvedDocs.map(doc => doc.manualCategory || doc.category || 'Otro');
      // Importar la función de entrenamiento
      const { trainClassifier } = await import('@/services/ml');
      const trainResult = await trainClassifier(texts, labels);

      // Simular guardado en backend principal (puedes reemplazar por tu lógica real)
      await new Promise(resolve => setTimeout(resolve, 2000));

      // Organizar por categorías
      const categories = approvedDocs.reduce((acc, doc) => {
        const category = doc.manualCategory || doc.category || 'Sin Categoría';
        if (!acc[category]) acc[category] = [];
        acc[category].push(doc);
        return acc;
      }, {} as Record<string, DocumentReview[]>);

      // Mostrar resumen de guardado y entrenamiento
      const totalSaved = approvedDocs.length;
      const categoriesCount = Object.keys(categories).length;
      let trainMsg = trainResult.success
        ? `🧠 Clasificador entrenado con ${trainResult.trained_samples} ejemplos.`
        : `⚠️ Error al entrenar clasificador: ${trainResult.message}`;

      showToast(
        `✅ Guardados ${totalSaved} documentos en ${categoriesCount} categorías diferentes.\n${trainMsg}`,
        trainResult.success ? 'success' : 'error'
      );

      // Resetear estado
      setResults([]);
      setReviewMode(false);
      setSelectedFiles(null);
    } catch (error) {
      console.error('Error al guardar documentos o entrenar ML:', error);
      showToast('Error al guardar los documentos o entrenar el clasificador ML.', 'error');
    } finally {
      setSaving(false);
    }
  };

  const getCategoryColor = (category?: string) => {
    const colors: Record<string, string> = {
      'Contrato': 'bg-blue-100 text-blue-800',
      'Contrato de Granos': 'bg-blue-200 text-blue-900',
      'Informe': 'bg-green-100 text-green-800',
      'Factura': 'bg-yellow-100 text-yellow-800',
      'Remito': 'bg-orange-100 text-orange-800',
      'Nota de Crédito': 'bg-red-100 text-red-800',
      'Nota de Débito': 'bg-pink-100 text-pink-800',
      'Política': 'bg-purple-100 text-purple-800',
      'Manual': 'bg-indigo-100 text-indigo-800',
      'Orden de Compra': 'bg-teal-100 text-teal-800',
      'Recibo': 'bg-cyan-100 text-cyan-800',
      'Otro': 'bg-gray-100 text-gray-800',
    };
    return colors[category || ''] || 'bg-gray-100 text-gray-800';
  };

  const getConfidenceColor = (confidence?: number) => {
    if (!confidence) return 'text-gray-500';
    if (confidence > 0.8) return 'text-green-600';
    if (confidence > 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  const categories = [
    'Contrato',
    'Contrato de Granos',
    'Informe',
    'Factura',
    'Remito',
    'Nota de Crédito',
    'Nota de Débito',
    'Política',
    'Manual',
    'Orden de Compra',
    'Recibo',
    'Otro'
  ];

  return (
    <div className="space-y-6">
      <Card>
        <h1 className="text-2xl font-bold mb-4 text-primary-700">
          Importación Inteligente de Documentos
        </h1>
        <p className="mb-6 text-gray-700">
          Sube múltiples documentos y nuestro sistema de Machine Learning los clasificará automáticamente. 
          Revisa y aprueba las clasificaciones antes de guardar.
        </p>

        {/* Estado del servicio ML */}
        <div className="mb-4">
          {checkingML ? (
            <div className="flex items-center text-sm text-gray-600">
              <svg className="animate-spin h-4 w-4 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Verificando servicio de clasificación...
            </div>
          ) : mlAvailable ? (
            <div className="flex items-center text-sm text-green-600">
              <svg className="h-4 w-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              Servicio ML disponible - Listo para clasificar
            </div>
          ) : (
            <div className="flex items-center text-sm text-red-600">
              <svg className="h-4 w-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              Servicio ML no disponible (ejecuta: python run_server.py en backend-ml/)
            </div>
          )}
        </div>

        {/* Selector de carpeta */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Seleccionar carpeta con documentos
          </label>
          <input
            type="file"
            multiple
            onChange={handleFolderSelect}
            className="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none focus:border-primary-500 p-2"
            // @ts-ignore - webkitdirectory no está en tipos oficiales pero funciona
            webkitdirectory="true"
            disabled={!mlAvailable || importing}
          />
          <p className="text-xs text-gray-500 mt-1">
            Se procesarán todos los archivos de la carpeta (TXT, PDF, imágenes, etc.)
          </p>
        </div>

        {/* Contador de archivos */}
        {selectedFiles && selectedFiles.length > 0 && (
          <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
            <p className="text-sm font-semibold text-blue-900">
              📁 {selectedFiles.length} archivo{selectedFiles.length !== 1 ? 's' : ''} seleccionado{selectedFiles.length !== 1 ? 's' : ''}
            </p>
          </div>
        )}

        {/* Botón de importar */}
        <Button 
          onClick={handleImport} 
          disabled={importing || !mlAvailable || !selectedFiles || selectedFiles.length === 0}
          className="w-full"
        >
          {importing ? (
            <>
              <svg className="animate-spin h-5 w-5 mr-2 inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Procesando con IA...
            </>
          ) : (
            <>
              <Brain className="h-5 w-5 mr-2" />
              Analizar y Clasificar con IA
            </>
          )}
        </Button>
      </Card>

      {/* Vista de Revisión */}
      {reviewMode && results.length > 0 && (
        <Card>
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-xl font-bold text-gray-900">
                Revisar Clasificaciones
              </h2>
              <p className="text-gray-600 mt-1">
                Revisa cada documento, modifica categorías si es necesario y aprueba antes de guardar.
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-600">
                Aprobados: {results.filter(r => r.approved).length} / {results.length}
              </div>
              <Button 
                onClick={handleSaveDocuments}
                disabled={saving || results.filter(r => r.approved).length === 0}
                className="flex items-center space-x-2"
              >
                {saving ? (
                  <>
                    <svg className="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <span>Guardando...</span>
                  </>
                ) : (
                  <>
                    <Save className="h-4 w-4" />
                    <span>Guardar Aprobados</span>
                  </>
                )}
              </Button>
            </div>
          </div>

          <div className="space-y-4">
            {results.map((result, index) => (
              <div
                key={index}
                className={`border rounded-lg p-4 transition-all ${
                  result.approved 
                    ? 'bg-green-50 border-green-200' 
                    : result.reviewed 
                      ? 'bg-red-50 border-red-200'
                      : 'bg-white border-gray-200'
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    {/* Header del documento */}
                    <div className="flex items-center space-x-3 mb-3">
                      <FileText className="h-6 w-6 text-gray-500" />
                      <span className="font-medium text-gray-900 truncate">
                        {result.filename}
                      </span>
                      {result.success ? (
                        <CheckCircle className="h-5 w-5 text-green-500" />
                      ) : (
                        <XCircle className="h-5 w-5 text-red-500" />
                      )}
                    </div>

                    {result.success ? (
                      <>
                        {/* Clasificación automática */}
                        <div className="mb-3">
                          <div className="flex items-center space-x-2 mb-2">
                            <span className="text-sm font-medium text-gray-700">Clasificación IA:</span>
                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getCategoryColor(result.category)}`}>
                              {result.category}
                            </span>
                            <span className={`text-sm font-medium ${getConfidenceColor(result.confidence)}`}>
                              {result.confidence !== undefined && (
                                `${(result.confidence * 100).toFixed(1)}% confianza`
                              )}
                            </span>
                          </div>

                          {/* Selector de categoría manual */}
                          <div className="flex items-center space-x-2">
                            <span className="text-sm text-gray-600">Cambiar a:</span>
                            <select
                              value={result.manualCategory || result.category || ''}
                              onChange={(e) => handleChangeCategory(index, e.target.value)}
                              className="text-sm border border-gray-300 rounded px-2 py-1"
                            >
                              {categories.map(cat => (
                                <option key={cat} value={cat}>{cat}</option>
                              ))}
                            </select>
                          </div>
                        </div>

                        {/* Vista previa del texto */}
                        {result.text_preview && (
                          <div className="mb-3">
                            <p className="text-sm text-gray-600 mb-2">
                              <strong>Vista previa:</strong>
                            </p>
                            <p className="text-sm text-gray-700 bg-gray-50 p-2 rounded line-clamp-3">
                              {result.text_preview}
                            </p>
                          </div>
                        )}

                        {/* Palabras clave */}
                        {result.keywords && result.keywords.length > 0 && (
                          <div className="mb-3">
                            <p className="text-sm text-gray-600 mb-2">
                              <strong>Palabras clave detectadas:</strong>
                            </p>
                            <div className="flex flex-wrap gap-1">
                              {result.keywords.slice(0, 8).map((keyword, kIndex) => (
                                <span
                                  key={kIndex}
                                  className="px-2 py-0.5 bg-blue-100 text-blue-700 text-xs rounded"
                                >
                                  {keyword}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}
                      </>
                    ) : (
                      <div className="mb-3">
                        <div className="flex items-center space-x-2 text-red-600">
                          <AlertTriangle className="h-4 w-4" />
                          <span className="text-sm">
                            {result.error || 'Error al procesar el archivo'}
                          </span>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Acciones */}
                  <div className="flex flex-col space-y-2 ml-4">
                    {result.success && (
                      <>
                        <Button
                          onClick={() => setSelectedDocument(result)}
                          variant="outline"
                          className="text-xs px-3 py-1"
                        >
                          <Eye className="h-3 w-3 mr-1" />
                          Ver
                        </Button>
                        <Button
                          onClick={() => handleApproveDocument(index)}
                          disabled={result.approved}
                          className="text-xs px-3 py-1"
                        >
                          <CheckCircle className="h-3 w-3 mr-1" />
                          {result.approved ? 'Aprobado' : 'Aprobar'}
                        </Button>
                        <Button
                          onClick={() => handleRejectDocument(index)}
                          variant="danger"
                          className="text-xs px-3 py-1"
                        >
                          <XCircle className="h-3 w-3 mr-1" />
                          Rechazar
                        </Button>
                      </>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Modal de vista previa del documento */}
      {selectedDocument && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg max-w-4xl w-full mx-4 max-h-[90vh] overflow-hidden">
            <div className="flex items-center justify-between p-6 border-b">
              <h3 className="text-lg font-semibold text-gray-900">
                Vista previa: {selectedDocument.filename}
              </h3>
              <button
                onClick={() => setSelectedDocument(null)}
                className="text-gray-400 hover:text-gray-600"
              >
                <XCircle className="h-6 w-6" />
              </button>
            </div>
            <div className="p-6 overflow-y-auto max-h-[70vh]">
              <div className="mb-4">
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${getCategoryColor(selectedDocument.category)}`}>
                  {selectedDocument.category}
                </span>
                <span className={`ml-2 text-sm ${getConfidenceColor(selectedDocument.confidence)}`}>
                  {selectedDocument.confidence !== undefined && (
                    `${(selectedDocument.confidence * 100).toFixed(1)}% confianza`
                  )}
                </span>
              </div>
              
              {selectedDocument.text && (
                <div className="bg-gray-50 p-4 rounded-lg">
                  <pre className="text-sm text-gray-800 whitespace-pre-wrap font-mono">
                    {selectedDocument.text}
                  </pre>
                </div>
              )}
              
              {selectedDocument.keywords && selectedDocument.keywords.length > 0 && (
                <div className="mt-4">
                  <p className="text-sm font-medium text-gray-700 mb-2">Palabras clave:</p>
                  <div className="flex flex-wrap gap-2">
                    {selectedDocument.keywords.map((keyword, kIndex) => (
                      <span
                        key={kIndex}
                        className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded"
                      >
                        {keyword}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default BulkImportPage;
