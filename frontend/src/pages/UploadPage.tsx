import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUploadDocument } from '@/hooks/useDocuments';
import { DocumentCreate } from '@/types';
import { Upload, FileText, X } from 'lucide-react';

const UploadPage = () => {
  const navigate = useNavigate();
  const [file, setFile] = useState<File | null>(null);
  const [metadata, setMetadata] = useState<DocumentCreate>({
    title: '',
    description: '',
    category: '',
    tags: '',
    is_public: false,
  });
  const [dragActive, setDragActive] = useState(false);

  const uploadMutation = useUploadDocument();

  const handleFileSelect = (selectedFile: File) => {
    setFile(selectedFile);
    if (!metadata.title) {
      setMetadata({
        ...metadata,
        title: selectedFile.name.replace(/\.[^/.]+$/, ''), // Remove extension
      });
    }
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!file) {
      alert('Please select a file to upload');
      return;
    }

    try {
      await uploadMutation.mutateAsync({ file, metadata });
      navigate('/documents');
    } catch (error) {
      console.error('Upload failed:', error);
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div>
  <h1 className="text-2xl font-bold text-gray-900">Cargar documento</h1>
  <p className="text-gray-600">Agregue un nuevo documento a su biblioteca</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* File Upload Area */}
        <div className="card p-6">
          <div
            className={`
              relative border-2 border-dashed rounded-lg p-8 text-center transition-colors
              ${dragActive ? 'border-primary-500 bg-primary-50' : 'border-gray-300'}
              ${file ? 'border-green-500 bg-green-50' : ''}
            `}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <input
              id="file-upload"
              type="file"
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              onChange={(e) => e.target.files?.[0] && handleFileSelect(e.target.files[0])}
              accept=".pdf,.doc,.docx,.txt,.jpg,.jpeg,.png,.gif"
            />
            
            {file ? (
              <div className="flex items-center justify-center space-x-4">
                <FileText className="h-12 w-12 text-green-500" />
                <div className="text-left">
                  <p className="text-sm font-medium text-gray-900">{file.name}</p>
                  <p className="text-sm text-gray-500">
                    {(file.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() => {
                    setFile(null);
                    setMetadata({ ...metadata, title: '' });
                  }}
                  className="p-1 rounded-full text-gray-400 hover:text-gray-600"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
            ) : (
              <>
                <Upload className="mx-auto h-12 w-12 text-gray-400" />
                <div className="mt-4">
                  <p className="text-lg font-medium text-gray-900">
                    Arrastre su archivo aquí, o haga clic para buscar
                  </p>
                  <p className="text-sm text-gray-500 mt-2">
                    Se admiten PDF, DOC, DOCX, TXT, JPG, PNG, GIF (máx. 10MB)
                  </p>
                </div>
              </>
            )}
          </div>
        </div>

        {/* Metadata Form */}
        <div className="card p-6 space-y-4">
          <h3 className="text-lg font-medium text-gray-900">Información del documento</h3>
          
          <div>
            <label htmlFor="title" className="block text-sm font-medium text-gray-700">
              Título *
            </label>
            <input
              id="title"
              type="text"
              required
              value={metadata.title}
              onChange={(e) => setMetadata({ ...metadata, title: e.target.value })}
              className="mt-1 input"
              placeholder="Ingrese el título del documento"
            />
          </div>

          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700">
              Descripción
            </label>
            <textarea
              id="description"
              rows={3}
              value={metadata.description}
              onChange={(e) => setMetadata({ ...metadata, description: e.target.value })}
              className="mt-1 input"
              placeholder="Ingrese la descripción del documento"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="category" className="block text-sm font-medium text-gray-700">
                Categoría
              </label>
              <select
                id="category"
                value={metadata.category}
                onChange={(e) => setMetadata({ ...metadata, category: e.target.value })}
                className="mt-1 input"
              >
                <option value="">Seleccione categoría</option>
                <option value="contract">Contrato</option>
                <option value="report">Informe</option>
                <option value="invoice">Factura</option>
                <option value="policy">Política</option>
                <option value="manual">Manual</option>
                <option value="other">Otro</option>
              </select>
            </div>

            <div>
              <label htmlFor="tags" className="block text-sm font-medium text-gray-700">
                Etiquetas
              </label>
              <input
                id="tags"
                type="text"
                value={metadata.tags}
                onChange={(e) => setMetadata({ ...metadata, tags: e.target.value })}
                className="mt-1 input"
                placeholder="etiqueta1, etiqueta2, etiqueta3"
              />
            </div>
          </div>

          <div className="flex items-center">
            <input
              id="is_public"
              type="checkbox"
              checked={metadata.is_public}
              onChange={(e) => setMetadata({ ...metadata, is_public: e.target.checked })}
              className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
            />
              <label htmlFor="is_public" className="ml-2 block text-sm text-gray-900">
                Hacer este documento público (visible para todos los usuarios)
              </label>
          </div>
        </div>

        {/* Actions */}
        <div className="flex justify-end space-x-4">
          <button
            type="button"
            onClick={() => navigate('/documents')}
            className="btn-outline"
          >
            Cancelar
          </button>
          <button
            type="submit"
            disabled={!file || uploadMutation.isPending}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {uploadMutation.isPending ? 'Cargando...' : 'Cargar documento'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default UploadPage;