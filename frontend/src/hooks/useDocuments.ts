import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { documentService } from '@/services/documents';
import { DocumentCreate, DocumentUpdate, DocumentFilters } from '@/types';

// Documents list hook
export const useDocuments = (filters: DocumentFilters = {}) => {
  return useQuery({
    queryKey: ['documents', filters],
    queryFn: () => documentService.getDocuments(filters),
    staleTime: 30000, // 30 seconds
  });
};

// Single document hook
export const useDocument = (id: number) => {
  return useQuery({
    queryKey: ['document', id],
    queryFn: () => documentService.getDocument(id),
    enabled: !!id,
    staleTime: 60000, // 1 minute
  });
};

// Upload document hook
export const useUploadDocument = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ file, metadata }: { file: File; metadata: DocumentCreate }) =>
      documentService.upload(file, metadata),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['documents'] });
    },
  });
};

// Update document hook
export const useUpdateDocument = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ id, updates }: { id: number; updates: DocumentUpdate }) =>
      documentService.updateDocument(id, updates),
    onSuccess: (data, variables) => {
      queryClient.setQueryData(['document', variables.id], data);
      queryClient.invalidateQueries({ queryKey: ['documents'] });
    },
  });
};

// Delete document hook
export const useDeleteDocument = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (id: number) => documentService.deleteDocument(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['documents'] });
    },
  });
};

// Download document hook
export const useDownloadDocument = () => {
  return useMutation({
    mutationFn: async (id: number) => {
      const blob = await documentService.downloadDocument(id);
      const document = await documentService.getDocument(id);
      
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const link = window.document.createElement('a');
      link.href = url;
      link.download = document.filename;
      window.document.body.appendChild(link);
      link.click();
      window.URL.revokeObjectURL(url);
      window.document.body.removeChild(link);
    },
  });
};

// Categories hook
export const useCategories = () => {
  return useQuery({
    queryKey: ['categories'],
    queryFn: documentService.getCategories,
    staleTime: 60 * 60 * 1000, // 1 hour
  });
};