"""
Script para probar la conexión a MySQL
"""
import pymysql

def test_mysql_connection():
    print("🔍 Probando conexión a MySQL...")
    
    try:
        # Configuración de conexión
        config = {
            'host': 'localhost',
            'port': 3307,
            'user': 'edms_user',
            'password': 'edms_password123',
            'database': 'edms_db',
            'charset': 'utf8mb4'
        }
        
        print(f"Conectando a: {config['user']}@{config['host']}:{config['port']}/{config['database']}")
        
        # Probar conexión
        connection = pymysql.connect(**config)
        
        with connection.cursor() as cursor:
            # Probar consulta básica
            cursor.execute("SELECT 'Conexión exitosa!' as status, VERSION() as version")
            result = cursor.fetchone()
            print(f"✅ {result[0]}")
            print(f"📋 MySQL Version: {result[1]}")
            
            # Mostrar tablas
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"📊 Tablas en la BD: {len(tables)}")
            for table in tables:
                print(f"  - {table[0]}")
        
        connection.close()
        print("✅ Conexión cerrada correctamente")
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print("\n🔧 Verificaciones:")
        print("1. ¿Está ejecutándose MySQL? -> docker ps")
        print("2. ¿Puerto correcto? -> 3307")
        print("3. ¿Credenciales correctas? -> edms_user/edms_password123")

if __name__ == "__main__":
    test_mysql_connection()