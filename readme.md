1) Para instalar reqs
    - pip install -r requirements.txt

2) Para correr migrations:
    - python api/manage.py makemigrations
    - python api/manage.py migrate

3) Para correr el servidor:
    - crear config de run server en pycharm (con puerto 8001) (hay que habilitar y configurar soporte django en el pycharm)
        captura: http://prntscr.com/dlocr9
    - o
    - python api/manage.py runserver 127.0.0.1:8001

4) Para correr la interfaz:
    - cd gui
    - python -m SimpleHTTPServer

5) Para ejecutar pasos:
    - Tener corriendo mongod.exe


Para usar la herramienta se debe tener el paso 1, 2, 3, 4 y 5.

El paso 1 es solo necesario cuando se agregan nuevas librerias
El paso 2 es solo necesario cuando cambia el modelo