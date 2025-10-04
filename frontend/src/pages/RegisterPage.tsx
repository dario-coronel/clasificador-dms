import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useRegister } from '@/hooks/useAuth';
import { UserCreate } from '@/types';
import { UserPlus } from 'lucide-react';

const RegisterPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<UserCreate>({
    email: '',
    username: '',
    first_name: '',
    last_name: '',
    password: '',
    phone: '',
    department: '',
    position: '',
  });
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');

  const registerMutation = useRegister();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (formData.password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    try {
      await registerMutation.mutateAsync(formData);
      navigate('/login', { 
        state: { message: 'Registration successful! Please sign in.' }
      });
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.');
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
            <UserPlus className="h-6 w-6 text-primary-600" />
          </div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Crear su cuenta
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Únase al Sistema de Gestión Electrónica de Documentos
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="rounded-md bg-red-50 p-4">
              <div className="text-sm text-red-700">{error}</div>
            </div>
          )}

          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label htmlFor="first_name" className="block text-sm font-medium text-gray-700">
                  Nombre
                </label>
                <input
                  id="first_name"
                  name="first_name"
                  type="text"
                  required
                  value={formData.first_name}
                  onChange={handleChange}
                  className="mt-1 input"
                  placeholder="Nombre"
                />
              </div>

              <div>
                <label htmlFor="last_name" className="block text-sm font-medium text-gray-700">
                  Apellido
                </label>
                <input
                  id="last_name"
                  name="last_name"
                  type="text"
                  required
                  value={formData.last_name}
                  onChange={handleChange}
                  className="mt-1 input"
                  placeholder="Apellido"
                />
              </div>
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Correo electrónico
              </label>
              <input
                id="email"
                name="email"
                type="email"
                required
                value={formData.email}
                onChange={handleChange}
                className="mt-1 input"
                placeholder="su.correo@empresa.com"
              />
            </div>

            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-700">
                Usuario
              </label>
              <input
                id="username"
                name="username"
                type="text"
                required
                value={formData.username}
                onChange={handleChange}
                className="mt-1 input"
                placeholder="Elija un usuario"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label htmlFor="department" className="block text-sm font-medium text-gray-700">
                  Departamento
                </label>
                <input
                  id="department"
                  name="department"
                  type="text"
                  value={formData.department}
                  onChange={handleChange}
                  className="mt-1 input"
                  placeholder="TI, RRHH, Finanzas..."
                />
              </div>

              <div>
                <label htmlFor="position" className="block text-sm font-medium text-gray-700">
                  Puesto
                </label>
                <input
                  id="position"
                  name="position"
                  type="text"
                  value={formData.position}
                  onChange={handleChange}
                  className="mt-1 input"
                  placeholder="Gerente, Desarrollador..."
                />
              </div>
            </div>

            <div>
              <label htmlFor="phone" className="block text-sm font-medium text-gray-700">
                Teléfono
              </label>
              <input
                id="phone"
                name="phone"
                type="tel"
                value={formData.phone}
                onChange={handleChange}
                className="mt-1 input"
                placeholder="+52 (555) 123-4567"
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
                placeholder="Elija una contraseña segura"
              />
            </div>

            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">
                Confirmar contraseña
              </label>
              <input
                id="confirmPassword"
                name="confirmPassword"
                type="password"
                required
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="mt-1 input"
                placeholder="Confirme su contraseña"
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={registerMutation.isPending}
              className="btn-primary w-full py-3"
            >
              {registerMutation.isPending ? 'Creando cuenta...' : 'Crear cuenta'}
            </button>
          </div>

          <div className="text-center">
            <p className="text-sm text-gray-600">
              ¿Ya tiene una cuenta?{' '}
              <Link
                to="/login"
                className="font-medium text-primary-600 hover:text-primary-500"
              >
                Iniciar sesión
              </Link>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RegisterPage;