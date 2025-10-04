"""
Guía paso a paso para probar todos los endpoints en Swagger UI
"""

print("""
🧪 GUÍA COMPLETA PARA PROBAR ENDPOINTS EN SWAGGER UI
================================================================

1. 📖 ABRIR SWAGGER UI:
   🔗 http://localhost:8000/docs

2. 🏥 PROBAR ENDPOINTS DE SALUD (Sin autenticación):
   
   ✅ GET / (Root)
   ✅ GET /health (Health check)  
   ✅ GET /db-test (Database test)

3. 🔐 REGISTRO Y AUTENTICACIÓN:
   
   📝 POST /api/v1/auth/register
   Datos de ejemplo:
   {
     "email": "admin@edms.com",
     "username": "admin",
     "first_name": "Admin",
     "last_name": "EDMS",
     "password": "admin123456",
     "phone": "+1234567890",
     "department": "IT",
     "position": "Administrator"
   }
   
   🔑 POST /api/v1/auth/login
   Datos de ejemplo:
   {
     "username": "admin@edms.com",
     "password": "admin123456"
   }
   
   ⚠️ IMPORTANTE: Copia el "access_token" de la respuesta

4. 🔒 AUTORIZACIÓN EN SWAGGER:
   
   - Haz clic en "Authorize" (🔒) arriba en Swagger UI
   - Escribe: Bearer tu_access_token_aquí
   - Haz clic en "Authorize"

5. 👤 PROBAR ENDPOINTS DE USUARIOS:
   
   ✅ GET /api/v1/users/me (Ver perfil)
   ✅ PUT /api/v1/users/me (Actualizar perfil)
   Datos de ejemplo:
   {
     "bio": "Administrador del sistema EDMS",
     "department": "Tecnología"
   }

6. 📄 PROBAR ENDPOINTS DE DOCUMENTOS:
   
   📤 POST /api/v1/documents/upload
   - Haz clic en "Choose File" y selecciona cualquier archivo
   - Completa los campos:
     * title: "Mi primer documento"
     * description: "Documento de prueba"
     * category: "test"
     * tags: "prueba,demo"
     * is_public: false
   
   📋 GET /api/v1/documents/ (Listar documentos)
   
   📄 GET /api/v1/documents/{id} (Ver documento específico)
   - Usa el ID del documento que subiste
   
   ✏️ PUT /api/v1/documents/{id} (Actualizar documento)
   Datos de ejemplo:
   {
     "title": "Documento actualizado",
     "description": "Descripción modificada"
   }

7. 🔍 PROBAR FILTROS DE BÚSQUEDA:
   
   📋 GET /api/v1/documents/ con parámetros:
   - search: "prueba"
   - category: "test"
   - limit: 5
   - skip: 0

================================================================
🎯 RESULTADOS ESPERADOS:

✅ Status 200: Operación exitosa
✅ Status 201: Recurso creado
❌ Status 400: Error en datos
❌ Status 401: No autorizado
❌ Status 403: Sin permisos
❌ Status 404: No encontrado

================================================================
🔗 ENLACES ÚTILES:

📖 Documentación: http://localhost:8000/docs
📚 ReDoc: http://localhost:8000/redoc
💚 Health: http://localhost:8000/health
🗄️ DB Test: http://localhost:8000/db-test

================================================================
""")

# Verificar que la API está ejecutándose
import requests
try:
    response = requests.get("http://localhost:8000/health", timeout=2)
    if response.status_code == 200:
        print("✅ API está ejecutándose en http://localhost:8000")
        print("🚀 ¡Ya puedes empezar a probar en Swagger UI!")
    else:
        print("⚠️ La API respondió pero con estado:", response.status_code)
except:
    print("❌ La API no está ejecutándose.")
    print("💡 Ejecuta: python main.py en el directorio backend")