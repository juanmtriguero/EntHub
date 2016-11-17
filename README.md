# EntHub

EntHub es la abreviatura de "Entertainment Hub" (centro de entretinimiento). Es una red social de ocio desarollada en Django para apuntar, comentar y compartir con amigos películas, series, juegos, libros, etc.

**NOTA: Actualmente se encuentra en desarrollo**

## Contraseñas

Durante el desarrollo, las contraseñas se almacenan en un archivo `passwords.py` que no está en el control de versiones y es ignorado por `.gitignore`. Al descargar el código, hay que crear dicho archivo en el directorio raíz del proyecto (el mismo en el que se encuentra el archivo `settings.py`). El archivo debe ser rellenado de la siguiente forma:

```
EMAIL_HOST_USER = 'your_email_user'
EMAIL_HOST_PASSWORD = 'your_password'
```