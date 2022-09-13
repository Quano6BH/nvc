#Getting started
waitress-serve --port={{port}} --host={{host}} --call flaskr:create_app

or 

set FLASK_APP=flaskr //windows
export FLASK_APP=flaskr//linux
flask run