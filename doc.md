# Documentacion de urls

## Ruta base

http://localhost:8000/api/

## Modulos

- auth/

  - token/

    #### **Method: POST**

    #### REQUEST

    ```json
    {
      "email": "aspirante@example.com",
      "password": "contraseña_segura"
    }
    ```

    #### RESPONSE

    ```json
    {
      "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMjg0NDY0MywiaWF0IjoxNzMyMjM5ODQzLCJqdGkiOiJiNTA4NDFkNTk2MGM0MWMzOGY3MmM3NmUxMGIwM2ZlNiIsInVzZXJfaWQiOiJhc3BpcmFudGVAZXhhbXBsZS5jb20ifQ.wGe1__qWOXZpC6_LSVzu9OQ4vqPMUgFbpGamaES2AKc",
      "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMyMjQwNzQzLCJpYXQiOjE3MzIyMzk4NDMsImp0aSI6IjllMTU3Njg0MWNkZjQ1MWFiZDYyNWI4OWRlZDdjNzU1IiwidXNlcl9pZCI6ImFzcGlyYW50ZUBleGFtcGxlLmNvbSJ9.f2j88bu1XuLvLM6q-kpkspewlGQZr0T6iUH0xZCTjWw",
      "payload": {
        "email": "aspirante@example.com",
        "tipo_usuario": "aspirante_lec",
        "exp": 1732240743
      }
    }
    ```

- captacion/
  - convocatorias/
    ### **Method: GET**

    #### **Headers: 'Bearer' Access Token**

    #### REQUEST
    None
    

    #### RESPONSE

    ```json
    [{
        "id": 1,
        "lugar_convocatoria": "Aguascalientes",
        "fecha_limite_registro": "2025-01-01",
        "fecha_entrega_resultados": "2025-01-15",
        "max_participantes": 249
    },
    {
        "id": 2,
        "lugar_convocatoria": "Baja California",
        "fecha_limite_registro": "2025-01-01",
        "fecha_entrega_resultados": "2025-01-15",
        "max_participantes": 115
    }]
    ```

    ### **Method: POST**

    #### **Headers: Bearer Access Token**

    #### REQUEST
    ```json
    {
    "lugar_convocatoria": "Aguascalientes",
    "fecha_limite_registro": "25-12-12", (YYYY-MM-DD)
    "fecha_entrega_resultados": "25-12-24", (YYYY-MM-DD)
    "max_participantes": "10"
    }
    ```

    #### RESPONSE
    ```json
    {
    "id": 33,
    "lugar_convocatoria": "Aguascalientes",
    "fecha_limite_registro": "2023-12-12",
    "fecha_entrega_resultados": "2023-12-24",
    "max_participantes": 10
    }
    ```

