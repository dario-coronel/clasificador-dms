"""
Servidor mínimo solo para registro - Sin FastAPI
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import hashlib
import pymysql
from datetime import datetime
import urllib.parse

class RegistrationHandler(BaseHTTPRequestHandler):
    
    def do_OPTIONS(self):
        """Handle preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = json.dumps({"status": "healthy"})
            self.wfile.write(response.encode())
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = json.dumps({"message": "EDMS Registration Server", "status": "running"})
            self.wfile.write(response.encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/api/v1/auth/register':
            try:
                # Leer datos del request
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                user_data = json.loads(post_data.decode('utf-8'))
                
                print(f"🔍 [REGISTER] Processing: {user_data.get('email', 'unknown')}")
                
                # Validar datos requeridos
                required_fields = ['email', 'username', 'first_name', 'last_name', 'password']
                for field in required_fields:
                    if field not in user_data:
                        self.send_error_response(400, f"Missing required field: {field}")
                        return
                
                # Conectar a la base de datos
                conn = pymysql.connect(
                    host='localhost',
                    user='edms_user',
                    password='edms_password_2024',
                    database='edms_db',
                    port=3306
                )
                cursor = conn.cursor()
                
                # Verificar si el usuario ya existe
                cursor.execute(
                    "SELECT id FROM users WHERE email = %s OR username = %s",
                    (user_data['email'], user_data['username'])
                )
                
                if cursor.fetchone():
                    cursor.close()
                    conn.close()
                    self.send_error_response(400, "User already exists")
                    return
                
                # Hash de la contraseña
                hashed_password = hashlib.sha256(user_data['password'].encode()).hexdigest()
                
                # Insertar usuario
                now = datetime.now()
                cursor.execute("""
                    INSERT INTO users (email, username, first_name, last_name, password_hash, 
                                      phone, department, position, is_active, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    user_data['email'],
                    user_data['username'],
                    user_data['first_name'],
                    user_data['last_name'],
                    hashed_password,
                    user_data.get('phone'),
                    user_data.get('department'),
                    user_data.get('position'),
                    True,
                    now,
                    now
                ))
                
                user_id = cursor.lastrowid
                conn.commit()
                cursor.close()
                conn.close()
                
                # Respuesta exitosa
                response_data = {
                    "id": user_id,
                    "email": user_data['email'],
                    "username": user_data['username'],
                    "first_name": user_data['first_name'],
                    "last_name": user_data['last_name'],
                    "is_active": True
                }
                
                self.send_response(201)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = json.dumps(response_data)
                self.wfile.write(response.encode())
                
                print(f"✅ [SUCCESS] User registered: {user_data['email']}")
                
            except Exception as e:
                print(f"❌ [ERROR] Registration failed: {e}")
                self.send_error_response(500, str(e))
        else:
            self.send_response(404)
            self.end_headers()
    
    def send_error_response(self, code, message):
        """Send error response"""
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        error_response = json.dumps({"error": message})
        self.wfile.write(error_response.encode())

def run_server():
    server_address = ('', 8002)  # Puerto 8002 para evitar conflictos
    httpd = HTTPServer(server_address, RegistrationHandler)
    print("🚀 Starting minimal registration server on port 8002...")
    print("📡 Server available at: http://localhost:8002")
    print("📋 Health check: http://localhost:8002/health")
    print("🔗 Registration: http://localhost:8002/api/v1/auth/register")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()