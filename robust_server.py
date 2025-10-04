"""
SOLUCIÓN FINAL - Servidor de registro ultra robusto para EDMS
"""
import socket
import threading
import json
import hashlib
import pymysql
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import re

class EDMSRegistrationServer:
    def __init__(self, host='localhost', port=8003):
        self.host = host
        self.port = port
        self.socket = None
        self.running = False
        
        # Configuración de base de datos
        self.db_config = {
            'host': 'localhost',
            'user': 'edms_user',
            'password': 'edms_password_2024',
            'database': 'edms_db',
            'port': 3306
        }
    
    def hash_password(self, password):
        """Hash simple de contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def get_db_connection(self):
        """Obtener conexión a la base de datos"""
        return pymysql.connect(**self.db_config)
    
    def register_user(self, user_data):
        """Registrar un nuevo usuario"""
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # Verificar si el usuario ya existe
            cursor.execute(
                "SELECT id FROM users WHERE email = %s OR username = %s",
                (user_data['email'], user_data['username'])
            )
            
            if cursor.fetchone():
                cursor.close()
                conn.close()
                return {"error": "User already exists", "status": 400}
            
            # Hash de la contraseña
            hashed_password = self.hash_password(user_data['password'])
            
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
            
            return {
                "id": user_id,
                "email": user_data['email'],
                "username": user_data['username'],
                "first_name": user_data['first_name'],
                "last_name": user_data['last_name'],
                "is_active": True,
                "status": 201
            }
            
        except Exception as e:
            return {"error": str(e), "status": 500}
    
    def send_response(self, client_socket, status_code, content_type, body):
        """Enviar respuesta HTTP"""
        response = f"HTTP/1.1 {status_code}\r\n"
        response += f"Content-Type: {content_type}\r\n"
        response += "Access-Control-Allow-Origin: *\r\n"
        response += "Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n"
        response += "Access-Control-Allow-Headers: Content-Type\r\n"
        response += f"Content-Length: {len(body)}\r\n"
        response += "\r\n"
        response += body
        
        client_socket.send(response.encode())
    
    def handle_request(self, client_socket, request):
        """Manejar petición HTTP"""
        try:
            lines = request.split('\r\n')
            request_line = lines[0]
            method, path, _ = request_line.split(' ')
            
            print(f"📡 {method} {path}")
            
            if method == "OPTIONS":
                self.send_response(client_socket, "200 OK", "text/plain", "OK")
                return
            
            if method == "GET":
                if path == "/health":
                    body = json.dumps({"status": "healthy", "service": "EDMS Registration"})
                    self.send_response(client_socket, "200 OK", "application/json", body)
                elif path == "/":
                    body = json.dumps({"message": "EDMS Registration Server", "status": "running"})
                    self.send_response(client_socket, "200 OK", "application/json", body)
                else:
                    self.send_response(client_socket, "404 Not Found", "text/plain", "Not Found")
                return
            
            if method == "POST" and path == "/api/v1/auth/register":
                # Encontrar el cuerpo de la petición
                content_length = 0
                for line in lines:
                    if line.lower().startswith('content-length:'):
                        content_length = int(line.split(':')[1].strip())
                        break
                
                if content_length > 0:
                    body_start = request.find('\r\n\r\n') + 4
                    body = request[body_start:body_start + content_length]
                    
                    try:
                        user_data = json.loads(body)
                        print(f"🔍 Registrando usuario: {user_data.get('email', 'unknown')}")
                        
                        # Validar campos requeridos
                        required_fields = ['email', 'username', 'first_name', 'last_name', 'password']
                        for field in required_fields:
                            if field not in user_data:
                                error_body = json.dumps({"error": f"Missing field: {field}"})
                                self.send_response(client_socket, "400 Bad Request", "application/json", error_body)
                                return
                        
                        # Registrar usuario
                        result = self.register_user(user_data)
                        
                        if result.get('status') == 201:
                            result.pop('status')
                            body = json.dumps(result)
                            self.send_response(client_socket, "201 Created", "application/json", body)
                            print(f"✅ Usuario registrado: {user_data['email']}")
                        else:
                            status = result.pop('status', 500)
                            body = json.dumps(result)
                            status_text = "Bad Request" if status == 400 else "Internal Server Error"
                            self.send_response(client_socket, f"{status} {status_text}", "application/json", body)
                            
                    except json.JSONDecodeError:
                        error_body = json.dumps({"error": "Invalid JSON"})
                        self.send_response(client_socket, "400 Bad Request", "application/json", error_body)
                else:
                    error_body = json.dumps({"error": "Empty body"})
                    self.send_response(client_socket, "400 Bad Request", "application/json", error_body)
            else:
                self.send_response(client_socket, "404 Not Found", "text/plain", "Not Found")
                
        except Exception as e:
            print(f"❌ Error handling request: {e}")
            error_body = json.dumps({"error": "Internal server error"})
            self.send_response(client_socket, "500 Internal Server Error", "application/json", error_body)
    
    def handle_client(self, client_socket):
        """Manejar cliente"""
        try:
            request = client_socket.recv(4096).decode()
            if request:
                self.handle_request(client_socket, request)
        except Exception as e:
            print(f"❌ Error with client: {e}")
        finally:
            client_socket.close()
    
    def start(self):
        """Iniciar servidor"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            self.running = True
            
            print(f"🚀 EDMS Registration Server iniciado")
            print(f"📡 Servidor disponible en: http://{self.host}:{self.port}")
            print(f"📋 Health check: http://{self.host}:{self.port}/health")
            print(f"🔗 Registro: http://{self.host}:{self.port}/api/v1/auth/register")
            print("⏹️  Presiona Ctrl+C para detener")
            
            while self.running:
                try:
                    client_socket, address = self.socket.accept()
                    thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                    thread.daemon = True
                    thread.start()
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    if self.running:
                        print(f"❌ Error accepting connection: {e}")
                        
        except Exception as e:
            print(f"❌ Error starting server: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Detener servidor"""
        self.running = False
        if self.socket:
            self.socket.close()
        print("🛑 Servidor detenido")

if __name__ == "__main__":
    server = EDMSRegistrationServer(port=8003)
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo servidor...")
        server.stop()