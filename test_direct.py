import requests
import json

def test_direct():
    url = "http://localhost:8001/api/v1/auth/register"
    
    # Datos simplificados para la prueba
    user_data = {
        "email": "newuser@test.com",
        "username": "newuser",
        "first_name": "New",
        "last_name": "User",
        "password": "password123"
    }
    
    print("🔍 Probando conexión directa al servidor...")
    
    try:
        # Primero verificar que el servidor responda
        health_response = requests.get("http://localhost:8001/health", timeout=5)
        print(f"✅ Health check: {health_response.status_code}")
        
        # Ahora probar el registro
        print(f"📡 Enviando POST a: {url}")
        response = requests.post(url, json=user_data, timeout=10)
        
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 201:
            print("🎉 ¡REGISTRO EXITOSO!")
            user_info = response.json()
            print(f"Usuario creado: {json.dumps(user_info, indent=2)}")
            return True
        elif response.status_code == 400:
            print("⚠️  Usuario puede que ya exista:")
            print(f"Response: {response.text}")
        else:
            print(f"❌ Error {response.status_code}:")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor en puerto 8001")
        print("💡 Verifica que el servidor esté ejecutándose")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return False

if __name__ == "__main__":
    success = test_direct()
    if success:
        print("\n🎉 El servidor de registro está funcionando correctamente!")
    else:
        print("\n😞 Hay un problema con el servidor de registro")