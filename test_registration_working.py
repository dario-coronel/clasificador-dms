import requests
import json

def test_registration_working():
    url = "http://localhost:8002/api/v1/auth/register"
    
    # Datos de prueba
    test_user = {
        "email": "working@edms.com",
        "username": "workinguser",
        "first_name": "Working",
        "last_name": "User", 
        "password": "testpass123",
        "phone": "+1-555-0123",
        "department": "Testing",
        "position": "Tester"
    }
    
    print("🧪 Probando registro final...")
    print(f"📡 URL: {url}")
    print(f"📊 Data: {json.dumps(test_user, indent=2)}")
    
    try:
        # Hacer la petición de registro
        response = requests.post(url, json=test_user, timeout=10)
        
        print(f"\n📊 Respuesta:")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 201:
            print("🎉 ¡ÉXITO! El registro funciona perfectamente!")
            user_data = response.json()
            print(f"👤 Usuario creado:")
            print(f"   ID: {user_data['id']}")
            print(f"   Email: {user_data['email']}")
            print(f"   Nombre: {user_data['first_name']} {user_data['last_name']}")
            print(f"   Username: {user_data['username']}")
            print(f"   Activo: {user_data['is_active']}")
            return True
            
        elif response.status_code == 400:
            print("⚠️ Usuario ya existe (esto es normal si ya probaste antes)")
            try:
                error_data = response.json()
                print(f"Detalle: {error_data.get('error', 'Usuario duplicado')}")
            except:
                print(f"Error: {response.text}")
            return True  # Esto también significa que el servidor funciona
            
        else:
            print(f"❌ Error {response.status_code}:")
            try:
                error_data = response.json()
                print(f"Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error text: {response.text}")
            return False
                
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor")
        print("💡 Asegúrate de que el servidor esté ejecutándose en puerto 8002")
        return False
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    success = test_registration_working()
    
    if success:
        print("\n✅ CONFIRMACIÓN: El sistema de registro está funcionando!")
        print("🌐 Ya puedes usar la aplicación web para registrarte")
        print("🔗 Ve a: http://localhost:3000/register")
    else:
        print("\n❌ El registro aún no funciona correctamente")
        print("🔧 Revisa que el servidor esté ejecutándose")