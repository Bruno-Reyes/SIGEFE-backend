import requests
import socket
from decouple import config
from datetime import datetime
import sys

def check_connection(host, port):
    try:
        socket.create_connection((host, port), timeout=5)
        return True
    except (socket.timeout, socket.error):
        return False

def check_authentication(url, token):
    try:
        response = requests.post(
            f"{url}/login",
            json={"key": token},
            timeout=10
        )
        return response.status_code == 200, response.json() if response.status_code == 200 else None
    except Exception as e:
        return False, str(e)

def test_email_service():
    print("\n=== Diagnóstico del Servicio de Correos ===")
    print(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Cargar configuración
    try:
        url = config("MICROSERVICE_NOTIFICATIONS_URL")
        token = config("MICROSERVICE_NOTIFICATIONS_TOKEN")
        host = url.split("//")[1].split(":")[0]
        port = 8080
    except Exception as e:
        print("\n❌ Error al cargar la configuración:")
        print(f"   {str(e)}")
        sys.exit(1)

    # Verificar conexión básica
    print("\n1. Verificando conexión básica...")
    if check_connection(host, port):
        print("✅ Conexión básica exitosa")
    else:
        print("❌ No se puede establecer conexión con el servidor")
        print(f"   Host: {host}")
        print(f"   Puerto: {port}")
        return

    # Verificar autenticación
    print("\n2. Probando autenticación...")
    auth_success, auth_result = check_authentication(url, token)
    if auth_success:
        print("✅ Autenticación exitosa")
    else:
        print("❌ Error en la autenticación:")
        print(f"   {auth_result}")
        return

    # Probar envío de correo de prueba
    print("\n3. Intentando enviar correo de prueba...")
    try:
        test_token = auth_result.get("token")
        response = requests.post(
            f"{url}/send-email",
            json={
                "destinatario": "jhernandez.owl@gmail.com",  # Cambia esto por un correo válido
                "asunto": "Test de Conexión",
                "cuerpo": "Este es un correo de prueba para verificar la conexión."
            },
            headers={"Authorization": f"Bearer {test_token}"},
            timeout=15
        )
        if response.status_code == 200:
            print("✅ Envío de correo de prueba exitoso")
        else:
            print(f"❌ Error al enviar correo de prueba: {response.status_code}")
            print(f"   Respuesta: {response.text}")
    except Exception as e:
        print("❌ Error al intentar enviar correo de prueba:")
        print(f"   {str(e)}")

if __name__ == "__main__":
    try:
        test_email_service()
    except KeyboardInterrupt:
        print("\n\nDiagnóstico interrumpido por el usuario.")
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
    finally:
        print("\n=== Fin del diagnóstico ===")
