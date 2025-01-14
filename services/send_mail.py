import requests
from decouple import config

def authenticate():
    # Obtenemos la URL del microservicio de notificaciones
    url = config("MICROSERVICE_NOTIFICATIONS_URL")
    
    # Nos autenticamos en el microservicio de notificaciones
    response_login = requests.post(
        url + "/login",
        json={
            "key": config("MICROSERVICE_NOTIFICATIONS_TOKEN")
        }
    )
    # Extraemos el token de la respuesta
    token = response_login.json()["token"]
    return token

def send_mail(destination: str, subject: str, body: str, token: str):
    url = config("MICROSERVICE_NOTIFICATIONS_URL")
    # Enviamos el correo
    response = requests.post(
        url + "/send-email",
        json={
            "destinatario": destination,
            "asunto": subject,
            "cuerpo": body
        },
        # Añadimos el token a los headers como Bearer token
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    
    
    