// API Base Types
export interface ApiResponse<T = any> {
  data?: T;
  message?: string;
  success: boolean;
}

// User Types
export interface User {
  id: number;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  phone?: string;
  department?: string;
  position?: string;
  bio?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface UserCreate {
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  password: string;
  phone?: string;
  department?: string;
  position?: string;
}

export interface UserUpdate {
  first_name?: string;
  last_name?: string;
  phone?: string;
  department?: string;
  position?: string;
  bio?: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// Document Types
export interface Document {
  id: number;
  title: string;
  description?: string;
  filename: string;
  file_path: string;
  file_size: number;
  mime_type: string;
  category?: string;
  tags?: string;
  is_public: boolean;
  owner_id: number;
  owner: User;
  current_version: number;
  created_at: string;
  updated_at: string;
}

export interface DocumentCreate {
  title: string;
  description?: string;
  category?: string;
  tags?: string;
  is_public?: boolean;
}

export interface DocumentUpdate {
  title?: string;
  description?: string;
  category?: string;
  tags?: string;
  is_public?: boolean;
}

export interface DocumentsResponse {
  documents: Document[];
  total: number;
  page: number;
  limit: number;
}

// Document Version Types
export interface DocumentVersion {
  id: number;
  document_id: number;
  version_number: number;
  filename: string;
  file_path: string;
  file_size: number;
  mime_type: string;
  created_at: string;
  created_by: number;
}

// Filter and Search Types
export interface DocumentFilters {
  search?: string;
  category?: string;
  owner_id?: number;
  is_public?: boolean;
  tags?: string;
  limit?: number;
  skip?: number;
}