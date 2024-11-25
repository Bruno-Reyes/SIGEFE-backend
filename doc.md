# Documentacion de urls

## Ruta base

http://localhost:8000/api/

## Modulos

- auth/

  - token/

    **Method: POST**

    ### REQUEST

    ```json
    {
      "email": "aspirante@example.com",
      "password": "contraseña_segura"
    }
    ```

    ### RESPONSE

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
