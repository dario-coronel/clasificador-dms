import api from './api';
import { LoginRequest, LoginResponse, UserCreate, User, UserUpdate } from '@/types';

export const authService = {
  // Register new user
  register: async (userData: UserCreate): Promise<User> => {
    const response = await api.post('/api/v1/auth/register', userData);
    return response.data;
  },

  // Login user
  login: async (credentials: LoginRequest): Promise<LoginResponse> => {
    // FastAPI expects form data for OAuth2 token endpoint
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    
    const response = await api.post('/api/v1/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    
    // Store token and user info
    localStorage.setItem('access_token', response.data.access_token);
    localStorage.setItem('user', JSON.stringify(response.data.user));
    
    return response.data;
  },

  // Logout user
  logout: (): void => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  },

  // Get current user
  getCurrentUser: (): User | null => {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },

  // Check if user is authenticated
  isAuthenticated: (): boolean => {
    return !!localStorage.getItem('access_token');
  },

  // Get stored token
  getToken: (): string | null => {
    return localStorage.getItem('access_token');
  },
};

export const userService = {
  // Get current user profile
  getProfile: async (): Promise<User> => {
    const response = await api.get('/api/v1/users/me');
    return response.data;
  },

  // Update current user profile
  updateProfile: async (userData: UserUpdate): Promise<User> => {
    const response = await api.put('/api/v1/users/me', userData);
    
    // Update stored user data
    localStorage.setItem('user', JSON.stringify(response.data));
    
    return response.data;
  },
};