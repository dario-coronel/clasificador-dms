import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useLogin } from '@/hooks/useAuth';
import { LoginRequest } from '@/types';
import { LogIn } from 'lucide-react';

const LoginPage = () => {
  const [formData, setFormData] = useState<LoginRequest>({
    username: '',
    password: '',
  });
  const [error, setError] = useState('');

  const loginMutation = useLogin();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      await loginMutation.mutateAsync(formData);
      // Navigation will be handled by the mutation's onSuccess
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed. Please try again.');
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <div className="mx-auto h-12 w-12 flex items-center justify-center rounded-full bg-primary-100">
            <LogIn className="h-6 w-6 text-primary-600" />
          </div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Iniciar sesión en EDMS
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Sistema de Gestión Electrónica de Documentos
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="rounded-md bg-red-50 p-4">
              <div className="text-sm text-red-700">{error}</div>
            </div>
          )}

          <div className="space-y-4">
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-700">
                Correo electrónico o usuario
              </label>
              <input
                id="username"
                name="username"
                type="text"
                required
                value={formData.username}
                onChange={handleChange}
                className="mt-1 input"
                placeholder="Ingrese su correo electrónico o usuario"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                Contraseña
              </label>
              <input
                id="password"
                name="password"
                type="password"
                required
                value={formData.password}
                onChange={handleChange}
                className="mt-1 input"
                placeholder="Ingrese su contraseña"
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={loginMutation.isPending}
              className="btn-primary w-full py-3"
            >
              {loginMutation.isPending ? 'Iniciando sesión...' : 'Iniciar sesión'}
            </button>
          </div>

          <div className="text-center">
            <p className="text-sm text-gray-600">
              ¿No tiene una cuenta?{' '}
              <Link
                to="/register"
                className="font-medium text-primary-600 hover:text-primary-500"
              >
                Regístrese
              </Link>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;