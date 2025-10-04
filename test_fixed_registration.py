import requests
import json

def test_fixed_registration():
    url = "http://localhost:8001/api/v1/auth/register"
    
    # Datos del usuario para probar
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
    
    print("🧪 Probando servidor de registro arreglado...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(user_data, indent=2)}")
    
    try:
        response = requests.post(url, json=user_data, timeout=10)
        print(f"\n📊 Respuesta del servidor:")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ ¡Registro exitoso!")
            user_info = response.json()
            print(f"Usuario creado: {json.dumps(user_info, indent=2)}")
            return True
        elif response.status_code == 400:
            print("⚠️  Usuario ya existe o datos inválidos:")
            try:
                error_data = response.json()
                print(f"Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error Text: {response.text}")
        else:
            print(f"❌ Error {response.status_code}:")
            try:
                error_data = response.json()
                print(f"Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error Text: {response.text}")
                
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión: No se puede conectar al servidor en puerto 8001")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    
    return False

if __name__ == "__main__":
    success = test_fixed_registration()
    if success:
        print("\n🎉 ¡El problema de registro ha sido solucionado!")
        print("💡 Puedes intentar registrarte nuevamente en la aplicación web.")
    else:
        print("\n😔 El problema persiste. Revisa los logs del servidor.")