import api from './api';
import { Document, DocumentCreate, DocumentUpdate, DocumentsResponse, DocumentFilters } from '@/types';

export const documentService = {
  // Upload new document
  upload: async (file: File, metadata: DocumentCreate): Promise<Document> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('title', metadata.title);
    
    if (metadata.description) formData.append('description', metadata.description);
    if (metadata.category) formData.append('category', metadata.category);
    if (metadata.tags) formData.append('tags', metadata.tags);
    if (metadata.is_public !== undefined) formData.append('is_public', metadata.is_public.toString());

    const response = await api.post('/api/v1/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Get documents with filters
  getDocuments: async (filters: DocumentFilters = {}): Promise<DocumentsResponse> => {
    const params = new URLSearchParams();
    
    if (filters.search) params.append('search', filters.search);
    if (filters.category) params.append('category', filters.category);
    if (filters.owner_id) params.append('owner_id', filters.owner_id.toString());
    if (filters.is_public !== undefined) params.append('is_public', filters.is_public.toString());
    if (filters.tags) params.append('tags', filters.tags);
    if (filters.limit) params.append('limit', filters.limit.toString());
    if (filters.skip) params.append('skip', filters.skip.toString());

    const response = await api.get(`/api/v1/documents/?${params.toString()}`);
    return response.data;
  },

  // Get single document
  getDocument: async (id: number): Promise<Document> => {
    const response = await api.get(`/api/v1/documents/${id}`);
    return response.data;
  },

  // Update document
  updateDocument: async (id: number, updates: DocumentUpdate): Promise<Document> => {
    const response = await api.put(`/api/v1/documents/${id}`, updates);
    return response.data;
  },

  // Delete document
  deleteDocument: async (id: number): Promise<void> => {
    await api.delete(`/api/v1/documents/${id}`);
  },

  // Download document
  downloadDocument: async (id: number): Promise<Blob> => {
    const response = await api.get(`/api/v1/documents/${id}/download`, {
      responseType: 'blob',
    });
    return response.data;
  },

  // Get document categories (helper)
  getCategories: async (): Promise<string[]> => {
    // This would need to be implemented in the backend
    // For now, return some common categories
    return ['General', 'Contract', 'Report', 'Invoice', 'Policy', 'Manual', 'Other'];
  },
};