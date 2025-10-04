import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { authService, userService } from '@/services/auth';
import { LoginRequest, UserCreate, UserUpdate } from '@/types';

// Auth hooks
export const useLogin = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (credentials: LoginRequest) => authService.login(credentials),
    onSuccess: (data) => {
      queryClient.setQueryData(['user'], data.user);
      queryClient.invalidateQueries({ queryKey: ['user'] });
    },
  });
};

export const useRegister = () => {
  return useMutation({
    mutationFn: (userData: UserCreate) => authService.register(userData),
  });
};

export const useLogout = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: () => Promise.resolve(authService.logout()),
    onSuccess: () => {
      queryClient.clear();
      window.location.href = '/login';
    },
  });
};

// User profile hooks
export const useProfile = () => {
  return useQuery({
    queryKey: ['user'],
    queryFn: userService.getProfile,
    enabled: authService.isAuthenticated(),
    retry: false, // No reintentar si falla
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

export const useUpdateProfile = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (userData: UserUpdate) => userService.updateProfile(userData),
    onSuccess: (data) => {
      queryClient.setQueryData(['user'], data);
      queryClient.invalidateQueries({ queryKey: ['user'] });
    },
  });
};