import { useState } from 'react';
import { useProfile, useUpdateProfile } from '@/hooks/useAuth';
import { UserUpdate } from '@/types';
import { Mail, Phone, Building, Briefcase } from 'lucide-react';

const ProfilePage = () => {
  const { data: user } = useProfile();
  const updateProfileMutation = useUpdateProfile();
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState<UserUpdate>({
    first_name: user?.first_name || '',
    last_name: user?.last_name || '',
    phone: user?.phone || '',
    department: user?.department || '',
    position: user?.position || '',
    bio: user?.bio || '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      await updateProfileMutation.mutateAsync(formData);
      setIsEditing(false);
    } catch (error) {
      console.error('Profile update failed:', error);
    }
  };

  const handleCancel = () => {
    setFormData({
      first_name: user?.first_name || '',
      last_name: user?.last_name || '',
      phone: user?.phone || '',
      department: user?.department || '',
      position: user?.position || '',
      bio: user?.bio || '',
    });
    setIsEditing(false);
  };

  if (!user) {
    return (
      <div className="text-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
        <p className="mt-2 text-sm text-gray-500">Loading profile...</p>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div>
  <h1 className="text-2xl font-bold text-gray-900">Perfil</h1>
  <p className="text-gray-600">Gestione la información de su cuenta</p>
      </div>

      <div className="card">
        {/* Profile Header */}
        <div className="px-6 py-8 border-b border-gray-200">
          <div className="flex items-center space-x-6">
            <div className="h-20 w-20 rounded-full bg-primary-500 flex items-center justify-center">
              <span className="text-white text-2xl font-bold">
                {user.first_name?.[0]}{user.last_name?.[0]}
              </span>
            </div>
            <div className="flex-1">
              <h2 className="text-xl font-bold text-gray-900">
                {user.first_name} {user.last_name}
              </h2>
              <p className="text-gray-600">{user.email}</p>
              <div className="flex items-center mt-2 space-x-4 text-sm text-gray-500">
                <span className="flex items-center">
                  <Building className="h-4 w-4 mr-1" />
                  {user.department || 'No department'}
                </span>
                <span className="flex items-center">
                  <Briefcase className="h-4 w-4 mr-1" />
                  {user.position || 'No position'}
                </span>
              </div>
            </div>
            <button
              onClick={() => setIsEditing(!isEditing)}
              className="btn-outline"
            >
              {isEditing ? 'Cancelar' : 'Editar perfil'}
            </button>
          </div>
        </div>

        {/* Profile Form */}
        <div className="p-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label htmlFor="first_name" className="block text-sm font-medium text-gray-700">
                  Nombre
                </label>
                <input
                  id="first_name"
                  type="text"
                  value={formData.first_name}
                  onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                  disabled={!isEditing}
                  className="mt-1 input disabled:bg-gray-50 disabled:text-gray-500"
                />
              </div>

              <div>
                <label htmlFor="last_name" className="block text-sm font-medium text-gray-700">
                  Apellido
                </label>
                <input
                  id="last_name"
                  type="text"
                  value={formData.last_name}
                  onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                  disabled={!isEditing}
                  className="mt-1 input disabled:bg-gray-50 disabled:text-gray-500"
                />
              </div>
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Correo electrónico
              </label>
              <div className="mt-1 relative">
                <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <input
                  id="email"
                  type="email"
                  value={user.email}
                  disabled
                  className="input pl-10 disabled:bg-gray-50 disabled:text-gray-500"
                />
              </div>
              <p className="mt-1 text-xs text-gray-500">El correo electrónico no puede ser modificado</p>
            </div>

            <div>
              <label htmlFor="phone" className="block text-sm font-medium text-gray-700">
                Teléfono
              </label>
              <div className="mt-1 relative">
                <Phone className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <input
                  id="phone"
                  type="tel"
                  value={formData.phone}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  disabled={!isEditing}
                  className="input pl-10 disabled:bg-gray-50 disabled:text-gray-500"
                  placeholder="+52 (555) 123-4567"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label htmlFor="department" className="block text-sm font-medium text-gray-700">
                  Departamento
                </label>
                <div className="mt-1 relative">
                  <Building className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                  <input
                    id="department"
                    type="text"
                    value={formData.department}
                    onChange={(e) => setFormData({ ...formData, department: e.target.value })}
                    disabled={!isEditing}
                    className="input pl-10 disabled:bg-gray-50 disabled:text-gray-500"
                    placeholder="TI, RRHH, Finanzas..."
                  />
                </div>
              </div>

              <div>
                <label htmlFor="position" className="block text-sm font-medium text-gray-700">
                  Puesto
                </label>
                <div className="mt-1 relative">
                  <Briefcase className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                  <input
                    id="position"
                    type="text"
                    value={formData.position}
                    onChange={(e) => setFormData({ ...formData, position: e.target.value })}
                    disabled={!isEditing}
                    className="input pl-10 disabled:bg-gray-50 disabled:text-gray-500"
                    placeholder="Gerente, Desarrollador..."
                  />
                </div>
              </div>
            </div>

            <div>
              <label htmlFor="bio" className="block text-sm font-medium text-gray-700">
                Biografía
              </label>
              <textarea
                id="bio"
                rows={4}
                value={formData.bio}
                onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
                disabled={!isEditing}
                className="mt-1 input disabled:bg-gray-50 disabled:text-gray-500"
                placeholder="Cuéntenos sobre usted..."
              />
            </div>

            {isEditing && (
              <div className="flex justify-end space-x-4">
                <button
                  type="button"
                  onClick={handleCancel}
                  className="btn-outline"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={updateProfileMutation.isPending}
                  className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {updateProfileMutation.isPending ? 'Guardando...' : 'Guardar cambios'}
                </button>
              </div>
            )}
          </form>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;