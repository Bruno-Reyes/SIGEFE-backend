#!/bin/bash

# Actualizar el fichero de requirements.txt
cd ..

pip freeze > requirements.txt

# Subir los cambios al repositorio
git add .

# Añadir un mensaje al commit
git commit -m $1

# Subir los cambios al repositorio
git push origin $2

echo "Cambios agregados al repositorio con éxito"
echo "Mensaje de commit: $1"
echo "Rama: $2"

echo "Happy coding!"