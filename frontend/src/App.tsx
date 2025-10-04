import { Routes, Route, Navigate } from 'react-router-dom';
import Layout from '@/components/Layout';
import LoginPage from '@/pages/LoginPage';
import RegisterPage from '@/pages/RegisterPage';
import DashboardPage from '@/pages/DashboardPage';
import DocumentsPage from '@/pages/DocumentsPage';
import DocumentDetailPage from '@/pages/DocumentDetailPage';
import ProfilePage from '@/pages/ProfilePage';
import UploadPage from '@/pages/UploadPage';
import HelpPage from '@/pages/HelpPage';
import BulkImportPage from '@/pages/BulkImportPage';


// Todas las rutas son públicas, sin login
const ProtectedRoute = ({ children }: { children: React.ReactNode }) => <Layout>{children}</Layout>;
const PublicRoute = ({ children }: { children: React.ReactNode }) => <>{children}</>;

function App() {
  return (
    <Routes>
      {/* Public Routes */}
      <Route 
        path="/login" 
        element={
          <PublicRoute>
            <LoginPage />
          </PublicRoute>
        } 
      />
      <Route 
        path="/register" 
        element={
          <PublicRoute>
            <RegisterPage />
          </PublicRoute>
        } 
      />

      {/* Protected Routes */}
      <Route 
        path="/dashboard" 
        element={
          <ProtectedRoute>
            <DashboardPage />
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/documents" 
        element={
          <ProtectedRoute>
            <DocumentsPage />
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/documents/:id" 
        element={
          <ProtectedRoute>
            <DocumentDetailPage />
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/upload" 
        element={
          <ProtectedRoute>
            <UploadPage />
          </ProtectedRoute>
        } 
      />

      <Route 
        path="/profile" 
        element={
          <ProtectedRoute>
            <ProfilePage />
          </ProtectedRoute>
        } 
      />


      <Route 
        path="/help" 
        element={
          <ProtectedRoute>
            <HelpPage />
          </ProtectedRoute>
        } 
      />

      <Route 
        path="/bulk-import" 
        element={
          <ProtectedRoute>
            <BulkImportPage />
          </ProtectedRoute>
        } 
      />

      {/* Default redirect */}
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      
      {/* 404 fallback */}
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}

export default App;