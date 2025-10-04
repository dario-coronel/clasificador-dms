"""
Script de depuración avanzada para el endpoint de registro
"""
import requests
import json
import traceback

def debug_registration():
    url = "http://localhost:8000/api/v1/auth/register"
    
    # Datos del formulario que está fallando
    user_data = {
        "email": "admin@edms.com",
        "username": "admin",
        "first_name": "Administrador",
        "last_name": "IT",
        "password": "admin123456",
        "phone": "+1 (555) 123-4567",
        "department": "IT",
        "position": "Manager"
    }
    
    print("🔍 DEBUG: Probando endpoint de registro...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(user_data, indent=2)}")
    
    # Primero verificar que el servidor esté disponible
    try:
        print("\n1️⃣ Verificando conectividad del servidor...")
        health_response = requests.get("http://localhost:8000/", timeout=5)
        print(f"✅ Servidor responde: {health_response.status_code}")
    except Exception as e:
        print(f"❌ Error de conectividad: {e}")
        return
    
    # Verificar endpoint de health si existe
    try:
        print("\n2️⃣ Verificando endpoint de health...")
        health_response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"✅ Health check: {health_response.status_code}")
    except:
        print("⚠️  No hay endpoint de health disponible")
    
    # Verificar endpoint de docs
    try:
        print("\n3️⃣ Verificando documentación...")
        docs_response = requests.get("http://localhost:8000/docs", timeout=5)
        print(f"✅ Docs disponibles: {docs_response.status_code}")
    except:
        print("⚠️  Docs no disponibles")
    
    # Ahora probar el registro
    print("\n4️⃣ Probando registro de usuario...")
    try:
        response = requests.post(url, json=user_data, timeout=10)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📊 Headers: {dict(response.headers)}")
        
        if response.status_code == 201:
            print("✅ Registro exitoso!")
            print(f"Response: {response.json()}")
        elif response.status_code == 422:
            print("❌ Error de validación:")
            try:
                error_data = response.json()
                print(f"Detalles: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error Text: {response.text}")
        elif response.status_code == 400:
            print("❌ Error de solicitud:")
            try:
                error_data = response.json()
                print(f"Detalles: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error Text: {response.text}")
        elif response.status_code == 500:
            print("❌ Error interno del servidor:")
            print(f"Error Text: {response.text}")
            print("🔧 Revisa los logs del servidor para más detalles")
        else:
            print(f"❌ Error inesperado ({response.status_code}):")
            try:
                error_data = response.json()
                print(f"Error JSON: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error Text: {response.text}")
                
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión: No se puede conectar al servidor")
        print("💡 Verifica que el backend esté ejecutándose en puerto 8000")
    except requests.exceptions.Timeout:
        print("❌ Error de timeout: El servidor no responde en el tiempo esperado")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        traceback.print_exc()

    # Probar también con diferentes datos para ver si es un problema específico
    print("\n5️⃣ Probando con datos simplificados...")
    simple_data = {
        "email": "test@test.com",
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(url, json=simple_data, timeout=10)
        print(f"📊 Simple test - Status Code: {response.status_code}")
        if response.status_code != 201:
            print(f"Simple test error: {response.text}")
        else:
            print("✅ Simple test exitoso - El problema puede estar en los datos específicos")
    except Exception as e:
        print(f"❌ Simple test también falló: {e}")

if __name__ == "__main__":
    debug_registration()