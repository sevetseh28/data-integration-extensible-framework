Para instalar reqs
    - pip install -r requirements.txt

Para correr migrations:
    - python api/manage.py makemigrations
    - python api/manage.py migrate

Para correr el servidor:
    - crear config de run server en pycharm (con puerto 8001) (hay que habilitar y configurar soporte django en el pycharm)
        captura: http://prntscr.com/dlocr9
    - o
    - python api/manage.py runserver 127.0.0.1:8001

Para correr la interfaz:
    - cd gui
    - python -m SimpleHTTPServer

Para ejecutar pasos:
    - Tener corriendo mongod.exe