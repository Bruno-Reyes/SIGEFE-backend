from decouple import config
import requests

token = None

def obtener_token():
    url = config('NOTIFICATIONS_SERVER_URL')+'/login'
    payload = {"key": config('NOTIFICATIONS_SERVER_KEY')}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)

    # Verifica el código de estado de la respuesta
    if response.status_code == 200:
        try:
            data = response.json()
            
            return data.get("token")
        except ValueError as e:
            print("Error al decodificar JSON:", e)
    else:
        print(f"Error: {response.status_code}, Respuesta: {response.text}")

def enviar_email(email:str, subject:str, message:str):
    token = obtener_token()
    
    url = config('NOTIFICATIONS_SERVER_URL')+'/send-email'
    payload = {
        "destinatario": email,
        "cuerpo": message,
        "asunto": subject
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    # Verifica el código de estado de la respuesta
    if response.status_code == 200:
        return True