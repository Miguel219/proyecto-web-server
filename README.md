
# proyecto-web TWITTER
* Este proyecto es una integración de 2 repositorios
https://github.com/Miguel219/proyecto-web-server para el backend DJANGO
https://github.com/sorozcov/proyecto-web-front-end para el frontend REACT NATIVE EXPO
* El proyecto es una representación del funcionamiento de Twitter

## Comandos para instalar las dependencias del proyecto:
## Repositorio Backend
* Descargar repositorio https://github.com/Miguel219/proyecto-web-server
* Crear base de datos en Postgres llamada ProyectoWeb (Puede utilizar la consola o pgadmin)
* Abrir archivo /mysite/mysite/setting.py
* En el archivo anterior modificar user, password,host y port para configuración con postgres. Por lo general host y port son predeterminados. El usuario y contraseña debes cambiarla a tu establecido con postgres.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ProyectoWeb',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
* pip install virtualenv
* virtualenv venv   (Crear virtualenv para correr el servidor en la carpeta principal)
* ./venv/Scripts/Activate (Activar virtualenv)
* pip install -r requirements.txt (Instalar dependencias de python)
* cd mysite 
* python manage.py migrate (Migraciones de django)
* python manage.py makemigrations (Migraciones de django)
* python manage.py runserver 0.0.0.0:8000 (Correr el servidor en tu red wifi. Para acceder necesitaremos tu ip)


## Repositorio Frontend
* Descargar repositorio https://github.com/sorozcov/proyecto-web-front-end
* Correr en el cmd ipconfig para obtener tu ip4address.
* Colocar tu ip4address en archivo src/sagas/settings/apibaseurl/
* Modificar ip4 a tu ip para poder correr el servidor en tu net y poder conectarlo con React Native
let ip4 = 'tu_ip_4';
* Luego necesitamos descargar expo para poder ejecutar nuestro programa en nuestra compu
* npm install -g expo-cli (https://docs.expo.io/get-started/installation/)
* Descargar la aplicación de Expo Client en cualquier celular android o ios (https://play.google.com/store/apps/details?id=host.exp.exponent&hl=es_GT o https://apps.apple.com/us/app/expo-client/id982107779)
* Luego de esto ya podemos iniciar a ejecutar nuestro proyecto
* yarn install (En la carpeta principal para instalar dependencias)
* yarn start
* Se generá un codigo QR
* Escaneamos el código con la aplicación y podremos probar la aplicación completa

# Nota importante:
Deben estar corriendo simultáneamente ambos proyectos para que todo funcione.
Video explicativo del readme.md 

## Proyecto Realizado por
* Universidad del Valle de Guatemala
* Silvio Orozco 18282 https://github.com/sorozcov/
* José Castañeda 18161 https://github.com/Miguel219/