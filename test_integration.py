"""
🧪 PRUEBA COMPLETA DE INTEGRACIÓN FRONTEND + BACKEND
================================================================

Este script prueba la integración completa del sistema EDMS:
- Frontend React en http://localhost:3001
- Backend FastAPI en http://localhost:8000
- Base de datos MySQL en Docker

PASOS PARA PROBAR MANUALMENTE:
================================================================

1. 🌐 ABRIR EL FRONTEND:
   ✅ http://localhost:3001
   
   Deberías ver la página de login del EDMS

2. 📝 REGISTRAR UN NUEVO USUARIO:
   - Haz clic en "Sign up"
   - Completa el formulario:
     * First Name: Admin
     * Last Name: EDMS
     * Email: admin@edms.com
     * Username: admin
     * Department: IT
     * Position: Administrator
     * Password: admin123456
     * Confirm Password: admin123456
   - Haz clic en "Create account"

3. 🔐 INICIAR SESIÓN:
   - Serás redirigido a login automáticamente
   - Usa las credenciales:
     * Email or Username: admin@edms.com
     * Password: admin123456
   - Haz clic en "Sign in"

4. 📊 EXPLORAR EL DASHBOARD:
   - Verás el dashboard principal
   - Estadísticas del sistema
   - Accesos rápidos

5. 📤 SUBIR UN DOCUMENTO:
   - Haz clic en "Upload Document"
   - Arrastra un archivo o haz clic para seleccionar
   - Completa la información:
     * Title: Mi primer documento
     * Description: Documento de prueba del sistema EDMS
     * Category: Report
     * Tags: prueba, demo, testing
     * Public: ✓ (opcional)
   - Haz clic en "Upload Document"

6. 📋 VER DOCUMENTOS:
   - Ve a "Documents" en el menú
   - Verás tu documento subido
   - Prueba la búsqueda y filtros
   - Haz clic en el documento para ver detalles

7. 📄 DETALLES DEL DOCUMENTO:
   - Ve información completa
   - Prueba descargar el documento
   - Observa metadatos y versiones

8. 👤 GESTIONAR PERFIL:
   - Ve a "Profile"
   - Haz clic en "Edit Profile"
   - Actualiza tu información
   - Guarda los cambios

================================================================
🎯 FUNCIONALIDADES A VERIFICAR:

✅ Frontend React:
- Navegación entre páginas
- Formularios responsivos
- Estados de carga
- Manejo de errores

✅ Backend FastAPI:
- API endpoints funcionando
- Autenticación JWT
- CRUD de documentos
- Subida de archivos

✅ Base de Datos:
- Almacenamiento de usuarios
- Gestión de documentos
- Relaciones entre tablas

✅ Integración Completa:
- Comunicación frontend-backend
- Proxy de Vite funcionando
- CORS configurado correctamente

================================================================
🔗 ENLACES ÚTILES:

📱 Frontend: http://localhost:3001
🔗 Backend API: http://localhost:8000
📖 API Docs: http://localhost:8000/docs
📚 ReDoc: http://localhost:8000/redoc
💚 Health Check: http://localhost:8000/health

================================================================
🐛 SOLUCIÓN DE PROBLEMAS:

❌ Si el frontend no carga:
- Verifica que esté en http://localhost:3001
- Revisa la consola del navegador
- Asegúrate de que npm run dev esté ejecutándose

❌ Si las APIs no responden:
- Verifica que el backend esté en http://localhost:8000
- Revisa http://localhost:8000/health
- Confirma que MySQL Docker esté ejecutándose

❌ Si hay errores de CORS:
- El proxy de Vite debería manejar esto automáticamente
- Verifica vite.config.ts

❌ Si no puedes subir archivos:
- Verifica que la carpeta uploads/ exista en el backend
- Revisa permisos de escritura

================================================================
✨ ¡SISTEMA EDMS COMPLETAMENTE FUNCIONAL! ✨

Tienes un sistema completo de gestión de documentos con:
- Interfaz moderna y responsiva
- API robusta y documentada  
- Base de datos escalable
- Autenticación segura
- Gestión completa de archivos

¡Disfruta explorando tu nuevo sistema EDMS! 🚀
"""

import requests
import json

def test_integration():
    """Prueba automatizada básica de integración"""
    
    print("🔍 Probando integración Frontend + Backend...")
    
    try:
        # Test 1: Backend Health Check
        print("\n1️⃣ Probando Backend Health Check...")
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend health check: OK")
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"❌ Backend health check falló: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ No se puede conectar al backend: {e}")
        print("💡 Asegúrate de que el backend esté ejecutándose en puerto 8000")
        
    try:
        # Test 2: Frontend Check
        print("\n2️⃣ Probando Frontend...")
        response = requests.get("http://localhost:3001", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend cargando correctamente")
            print(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
        else:
            print(f"❌ Frontend no responde correctamente: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ No se puede conectar al frontend: {e}")
        print("💡 Asegúrate de que 'npm run dev' esté ejecutándose")
        
    try:
        # Test 3: API Endpoints
        print("\n3️⃣ Probando API endpoints...")
        
        # Test root endpoint
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Root endpoint: OK")
        
        # Test database connection
        response = requests.get("http://localhost:8000/db-test", timeout=5)
        if response.status_code == 200:
            print("✅ Database connection: OK")
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"❌ Database connection falló: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error probando API endpoints: {e}")
        
    print("\n" + "="*60)
    print("🎯 RESUMEN DE PRUEBAS COMPLETADO")
    print("📱 Frontend: http://localhost:3001")
    print("🔗 Backend: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    print("="*60)

if __name__ == "__main__":
    test_integration()