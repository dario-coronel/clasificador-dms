import requests
import json

def test_robust_registration():
    print("🧪 Probando servidor robusto de registro...")
    
    # Test 1: Health check
    try:
        health_response = requests.get("http://localhost:8003/health", timeout=5)
        print(f"✅ Health check: {health_response.status_code}")
        print(f"   Response: {health_response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test 2: Registration
    url = "http://localhost:8003/api/v1/auth/register"
    test_user = {
        "email": "robust@test.com",
        "username": "robustuser",
        "first_name": "Robust",
        "last_name": "User",
        "password": "testpass123",
        "phone": "+1-555-9999",
        "department": "Testing",
        "position": "QA"
    }
    
    try:
        print(f"\n🔍 Probando registro...")
        print(f"📡 URL: {url}")
        
        response = requests.post(url, json=test_user, timeout=10)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 201:
            print("🎉 ¡REGISTRO EXITOSO!")
            user_data = response.json()
            print(f"👤 Usuario creado:")
            print(f"   ID: {user_data['id']}")
            print(f"   Email: {user_data['email']}")
            print(f"   Username: {user_data['username']}")
            print(f"   Nombre: {user_data['first_name']} {user_data['last_name']}")
            return True
            
        elif response.status_code == 400:
            error_data = response.json()
            if "already exists" in error_data.get('error', ''):
                print("✅ Usuario ya existe (el servidor funciona correctamente)")
                return True
            else:
                print(f"⚠️ Error de validación: {error_data}")
                return False
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error en registro: {e}")
        return False

if __name__ == "__main__":
    success = test_robust_registration()
    
    if success:
        print("\n🎉 ¡ÉXITO TOTAL!")
        print("✅ El servidor de registro está funcionando perfectamente")
        print("🌐 Ya puedes usar la aplicación web:")
        print("   1. Ve a http://localhost:3000/register")
        print("   2. Llena el formulario de registro")
        print("   3. El registro funcionará correctamente")
        print("\n🔧 Para iniciar el frontend:")
        print("   cd C:\\Clases\\Clasificador-DMS\\frontend")
        print("   npm run dev")
    else:
        print("\n❌ Aún hay problemas con el registro")
        print("🔧 Verifica que el servidor esté ejecutándose")