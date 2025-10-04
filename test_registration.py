"""
Prueba del endpoint de registro
"""
import requests
import json

def test_registration():
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
    
    print("🧪 Probando registro de usuario...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(user_data, indent=2)}")
    
    try:
        response = requests.post(url, json=user_data, timeout=10)
        print(f"\n📊 Respuesta del servidor:")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 201:
            print("✅ Registro exitoso!")
            print(f"Response: {response.json()}")
        else:
            print("❌ Error en el registro:")
            try:
                error_data = response.json()
                print(f"Error JSON: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error Text: {response.text}")
                
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        print("💡 Verifica que el backend esté ejecutándose en puerto 8000")

if __name__ == "__main__":
    test_registration()