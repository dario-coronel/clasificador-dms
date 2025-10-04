# EDMS Frontend

Electronic Document Management System (EDMS) Frontend built with React, TypeScript, Vite, and Tailwind CSS.

## 🚀 Features

- **Authentication System**: Login/Register with JWT tokens
- **Document Management**: Upload, view, search, and organize documents
- **User Profiles**: Manage user information and settings
- **Responsive Design**: Mobile-first design with Tailwind CSS
- **Real-time Updates**: React Query for efficient data fetching
- **File Upload**: Drag & drop file upload with progress tracking
- **Search & Filters**: Advanced document search and filtering
- **Document Versioning**: Track document versions and changes

## 🛠️ Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **React Query** - Server state management
- **Axios** - HTTP client
- **Lucide React** - Icon library

## 📁 Project Structure

```
src/
├── components/          # Reusable UI components
│   └── Layout.tsx      # Main layout component
├── pages/              # Page components
│   ├── LoginPage.tsx
│   ├── RegisterPage.tsx
│   ├── DashboardPage.tsx
│   ├── DocumentsPage.tsx
│   ├── DocumentDetailPage.tsx
│   ├── UploadPage.tsx
│   └── ProfilePage.tsx
├── services/           # API services
│   ├── api.ts         # Axios configuration
│   ├── auth.ts        # Authentication services
│   └── documents.ts   # Document services
├── hooks/              # Custom React hooks
│   ├── useAuth.ts     # Authentication hooks
│   └── useDocuments.ts # Document management hooks
├── types/              # TypeScript type definitions
│   └── index.ts       # Shared types
├── utils/              # Utility functions
├── App.tsx            # Main app component
├── main.tsx           # App entry point
└── index.css          # Global styles
```

## 🚦 Getting Started

### Prerequisites

- Node.js 20.19+ or 22.12+
- npm or yarn
- FastAPI backend running on http://localhost:8000

### Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

3. **Open your browser:**
   Navigate to http://localhost:3000

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## 🔧 Configuration

### API Configuration

The frontend is configured to proxy API requests to the backend:

```typescript
// vite.config.ts
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
      secure: false,
    },
  },
}
```

### Environment Variables

Create a `.env` file in the root directory:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=EDMS
```

## 📱 Pages & Features

### 🔐 Authentication
- **Login Page** (`/login`) - User authentication
- **Register Page** (`/register`) - New user registration

### 📊 Dashboard
- **Dashboard** (`/dashboard`) - Overview and quick actions
- Recent documents display
- Upload shortcuts
- System statistics

### 📄 Document Management
- **Documents List** (`/documents`) - Browse and search documents
- **Document Detail** (`/documents/:id`) - View document details
- **Upload Page** (`/upload`) - Upload new documents

### 👤 User Management
- **Profile Page** (`/profile`) - User profile management

## 🎨 UI Components

### Custom Components
- **Layout** - Main application layout with sidebar
- **Protected Routes** - Authentication-based routing
- **Form Components** - Consistent form styling

### Styling
- **Tailwind CSS** - Utility-first styling
- **Custom CSS Classes** - Component-specific styles
- **Responsive Design** - Mobile-first approach

## 🔌 API Integration

### Authentication
- JWT token-based authentication
- Automatic token refresh
- Protected route handling

### Document Management
- File upload with progress tracking
- Document CRUD operations
- Search and filtering
- Category management

### User Management
- Profile updates
- User preferences

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

The build artifacts will be stored in the `dist/` directory.

### Deployment Options

1. **Static Hosting** (Netlify, Vercel, GitHub Pages)
2. **Docker Container**
3. **Traditional Web Server** (Apache, Nginx)

### Docker Deployment

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

## 🧪 Testing

### Running Tests

```bash
npm run test
```

### Test Structure
- Unit tests for components
- Integration tests for hooks
- E2E tests for user flows

## 🔒 Security

- JWT token handling
- XSS protection
- CSRF protection
- Input validation
- Secure API communication

## 📊 Performance

- Code splitting with React.lazy
- Optimized bundle size
- Image optimization
- Caching strategies

## 🐛 Troubleshooting

### Common Issues

1. **Node.js Version**: Ensure you're using Node.js 20.19+ or 22.12+
2. **Backend Connection**: Verify FastAPI backend is running on port 8000
3. **CORS Issues**: Check backend CORS configuration
4. **Build Errors**: Clear node_modules and reinstall dependencies

### Debug Mode

Enable debug mode by setting:
```env
VITE_DEBUG=true
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🔗 Related Projects

- [EDMS Backend](../backend) - FastAPI backend service
- [EDMS Documentation](../docs) - Complete system documentation

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Contact the development team

---

Built with ❤️ for efficient document management.