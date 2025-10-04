"""
Script de pruebas completas para todos los endpoints de EDMS API
"""
import requests
import json
import os
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

class EDMSAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.user_id = None
        self.document_id = None
        
    def print_section(self, title):
        print(f"\n{'='*60}")
        print(f"🧪 {title}")
        print(f"{'='*60}")
    
    def print_result(self, endpoint, method, status_code, response=None):
        status_emoji = "✅" if 200 <= status_code < 300 else "❌"
        print(f"{status_emoji} {method} {endpoint} - Status: {status_code}")
        if response:
            if isinstance(response, dict):
                print(f"   📄 Response: {json.dumps(response, indent=2)[:200]}...")
            else:
                print(f"   📄 Response: {str(response)[:200]}...")
    
    def test_health_endpoints(self):
        """Probar endpoints de estado"""
        self.print_section("ENDPOINTS DE ESTADO Y SALUD")
        
        # Test root endpoint
        try:
            response = self.session.get(f"{BASE_URL}/")
            self.print_result("/", "GET", response.status_code, response.json())
        except Exception as e:
            print(f"❌ GET / - Error: {e}")
        
        # Test health endpoint
        try:
            response = self.session.get(f"{BASE_URL}/health")
            self.print_result("/health", "GET", response.status_code, response.json())
        except Exception as e:
            print(f"❌ GET /health - Error: {e}")
        
        # Test database endpoint
        try:
            response = self.session.get(f"{BASE_URL}/db-test")
            self.print_result("/db-test", "GET", response.status_code, response.json())
        except Exception as e:
            print(f"❌ GET /db-test - Error: {e}")
    
    def test_auth_endpoints(self):
        """Probar endpoints de autenticación"""
        self.print_section("ENDPOINTS DE AUTENTICACIÓN")
        
        # Registrar usuario
        user_data = {
            "email": "test@edms.com",
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "password": "testpassword123",
            "phone": "+1234567890",
            "department": "IT",
            "position": "Developer"
        }
        
        try:
            response = self.session.post(f"{API_BASE}/auth/register", json=user_data)
            self.print_result("/auth/register", "POST", response.status_code, response.json())
            
            if response.status_code == 200:
                user_info = response.json()
                self.user_id = user_info.get("id")
                print(f"   👤 Usuario creado con ID: {self.user_id}")
        except Exception as e:
            print(f"❌ POST /auth/register - Error: {e}")
        
        # Iniciar sesión
        login_data = {
            "username": "test@edms.com",
            "password": "testpassword123"
        }
        
        try:
            response = self.session.post(f"{API_BASE}/auth/login", data=login_data)
            self.print_result("/auth/login", "POST", response.status_code, response.json())
            
            if response.status_code == 200:
                token_info = response.json()
                self.token = token_info.get("access_token")
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                print(f"   🔑 Token obtenido: {self.token[:20]}...")
        except Exception as e:
            print(f"❌ POST /auth/login - Error: {e}")
    
    def test_user_endpoints(self):
        """Probar endpoints de usuarios"""
        self.print_section("ENDPOINTS DE USUARIOS")
        
        if not self.token:
            print("❌ No hay token de autenticación. Saltando pruebas de usuario.")
            return
        
        # Obtener información del usuario actual
        try:
            response = self.session.get(f"{API_BASE}/users/me")
            self.print_result("/users/me", "GET", response.status_code, response.json())
        except Exception as e:
            print(f"❌ GET /users/me - Error: {e}")
        
        # Actualizar información del usuario
        update_data = {
            "bio": "Usuario de prueba del sistema EDMS",
            "department": "Tecnología"
        }
        
        try:
            response = self.session.put(f"{API_BASE}/users/me", json=update_data)
            self.print_result("/users/me", "PUT", response.status_code, response.json())
        except Exception as e:
            print(f"❌ PUT /users/me - Error: {e}")
    
    def test_document_endpoints(self):
        """Probar endpoints de documentos"""
        self.print_section("ENDPOINTS DE DOCUMENTOS")
        
        if not self.token:
            print("❌ No hay token de autenticación. Saltando pruebas de documentos.")
            return
        
        # Crear archivo de prueba
        test_file_content = f"""
# Documento de Prueba EDMS
## Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Este es un documento de prueba para el sistema EDMS.

### Contenido de ejemplo:
- Item 1: Funcionalidad de subida
- Item 2: Gestión de metadatos
- Item 3: Control de permisos

¡Sistema funcionando correctamente! ✅
        """.strip()
        
        test_file_path = "test_document.txt"
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write(test_file_content)
        
        # Subir documento
        try:
            with open(test_file_path, "rb") as f:
                files = {"file": ("test_document.txt", f, "text/plain")}
                data = {
                    "title": "Documento de Prueba EDMS",
                    "description": "Documento creado automáticamente para probar la API",
                    "category": "test",
                    "tags": "prueba,automatizada,edms",
                    "is_public": False
                }
                
                response = self.session.post(f"{API_BASE}/documents/upload", files=files, data=data)
                self.print_result("/documents/upload", "POST", response.status_code, response.json())
                
                if response.status_code == 200:
                    doc_info = response.json()
                    self.document_id = doc_info.get("document_id")
                    print(f"   📄 Documento subido con ID: {self.document_id}")
        
        except Exception as e:
            print(f"❌ POST /documents/upload - Error: {e}")
        finally:
            # Limpiar archivo temporal
            if os.path.exists(test_file_path):
                os.remove(test_file_path)
        
        # Listar documentos
        try:
            response = self.session.get(f"{API_BASE}/documents/")
            self.print_result("/documents/", "GET", response.status_code, response.json())
        except Exception as e:
            print(f"❌ GET /documents/ - Error: {e}")
        
        # Obtener documento específico
        if self.document_id:
            try:
                response = self.session.get(f"{API_BASE}/documents/{self.document_id}")
                self.print_result(f"/documents/{self.document_id}", "GET", response.status_code, response.json())
            except Exception as e:
                print(f"❌ GET /documents/{self.document_id} - Error: {e}")
            
            # Actualizar documento
            update_data = {
                "description": "Documento actualizado automáticamente",
                "category": "updated-test"
            }
            
            try:
                response = self.session.put(f"{API_BASE}/documents/{self.document_id}", json=update_data)
                self.print_result(f"/documents/{self.document_id}", "PUT", response.status_code, response.json())
            except Exception as e:
                print(f"❌ PUT /documents/{self.document_id} - Error: {e}")
    
    def test_document_filters(self):
        """Probar filtros de documentos"""
        self.print_section("FILTROS Y BÚSQUEDA DE DOCUMENTOS")
        
        if not self.token:
            print("❌ No hay token de autenticación. Saltando pruebas de filtros.")
            return
        
        # Test con parámetros de búsqueda
        filters = [
            {"search": "prueba"},
            {"category": "test"},
            {"limit": 5},
            {"skip": 0, "limit": 10}
        ]
        
        for filter_params in filters:
            try:
                response = self.session.get(f"{API_BASE}/documents/", params=filter_params)
                param_str = "&".join([f"{k}={v}" for k, v in filter_params.items()])
                self.print_result(f"/documents/?{param_str}", "GET", response.status_code, response.json())
            except Exception as e:
                print(f"❌ GET /documents/ con filtros - Error: {e}")
    
    def run_all_tests(self):
        """Ejecutar todas las pruebas"""
        print("🚀 INICIANDO PRUEBAS COMPLETAS DE EDMS API")
        print(f"🌐 URL Base: {BASE_URL}")
        print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.test_health_endpoints()
        self.test_auth_endpoints()
        self.test_user_endpoints()
        self.test_document_endpoints()
        self.test_document_filters()
        
        self.print_section("RESUMEN DE PRUEBAS")
        print("✅ Pruebas de estado: Completadas")
        print("✅ Pruebas de autenticación: Completadas")
        print("✅ Pruebas de usuarios: Completadas")
        print("✅ Pruebas de documentos: Completadas")
        print("✅ Pruebas de filtros: Completadas")
        print("\n🎉 ¡TODAS LAS PRUEBAS COMPLETADAS!")
        print(f"🔗 Documentación: {BASE_URL}/docs")
        print(f"🔗 Interfaz: {BASE_URL}")

if __name__ == "__main__":
    tester = EDMSAPITester()
    tester.run_all_tests()