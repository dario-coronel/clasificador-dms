import axios from 'axios';

const ML_API_URL = import.meta.env.VITE_ML_API_URL || 'http://localhost:8002';

const mlApi = axios.create({
  baseURL: ML_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface OCRResponse {
  text: string;
  success: boolean;
  message: string;
}

export interface ClassificationResponse {
  category: string;
  confidence: number;
  all_probabilities: Record<string, number>;
  keywords: string[];
  success: boolean;
  message: string;
}

export interface ProcessedDocument {
  filename: string;
  text?: string;
  text_preview?: string;
  full_text_length: number;
  category?: string;
  confidence?: number;
  all_probabilities?: Record<string, number>;
  keywords?: string[];
  success: boolean;
  error?: string;
}

export interface BulkProcessResult {
  total_files: number;
  processed: number;
  failed: number;
  results: ProcessedDocument[];
}

export interface TrainingRequest {
  texts: string[];
  labels: string[];
}

export interface TrainingResponse {
  success: boolean;
  message: string;
  trained_samples: number;
}

// Extraer texto de un archivo usando OCR
export const extractText = async (file: File): Promise<OCRResponse> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await mlApi.post<OCRResponse>('/ocr', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

// Clasificar un texto
export const classifyText = async (text: string): Promise<ClassificationResponse> => {
  const response = await mlApi.post<ClassificationResponse>('/classify', {
    text,
  });

  return response.data;
};

// Procesar un documento completo (OCR + Clasificación)
export const processDocument = async (file: File): Promise<ProcessedDocument> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await mlApi.post<ProcessedDocument>('/process', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

// Procesar múltiples documentos
export const bulkProcessDocuments = async (files: File[]): Promise<BulkProcessResult> => {
  const formData = new FormData();
  files.forEach(file => {
    formData.append('files', file);
  });

  const response = await mlApi.post<BulkProcessResult>('/bulk-process', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

// Entrenar el clasificador con nuevos datos
export const trainClassifier = async (
  texts: string[],
  labels: string[]
): Promise<TrainingResponse> => {
  const response = await mlApi.post<TrainingResponse>('/train', {
    texts,
    labels,
  });

  return response.data;
};

// Verificar salud del servicio ML
export const checkMLHealth = async (): Promise<boolean> => {
  try {
    const response = await mlApi.get('/');
    return response.status === 200;
  } catch (error) {
    console.error('ML API no disponible:', error);
    return false;
  }
};

export default {
  extractText,
  classifyText,
  processDocument,
  bulkProcessDocuments,
  trainClassifier,
  checkMLHealth,
};
