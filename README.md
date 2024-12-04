# Instrucciones de instalacion BACKEND

## Instalacion

* Crear un entorno de ejecucion con conda o virtualenv

* Con el entorno activado, instalar las dependencias 

```bash
pip install -r requirements.txt
```

* Si ya lo tienes instalado y te pide una libreria nueva, solamente vuelve a ejecutar el comando anterior

## Ejecucion

* Para esta fase, debes eliminar el archivo db.sqllite3

* Ejecuta los siguientes comandos para crear las migrationes 

```bash
python manage.py makemigrations
python manage.py migrate
```

* Los siguientes comandos son para poblar la BD
```bash
python manage.py shell < utils/poblar_db.py
```

* Finalmente, ejecutamos el servidor
```bash
python manage.py runserver
```