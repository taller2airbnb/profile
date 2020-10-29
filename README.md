# Profile Services - Flask App - API

## Webserver Local

Exportar variables de ambiente según config elegida:

*export APP_SETTINGS=config.TestingWithDBConfig*

Levantar a través de:

*waitress-serve --call profileapp:create_app*

## Development container mode

*docker-compose build*

Crea los cotainers.

*docker-compose up*

Levanta un container con la postegres db y otro con la web (además se crean las tablas). 

## Docker - Heroku

*docker build -t taller2airbnb-profile:latest .*

Y usa su variable de ambiente para pegarle a la db de heroku.

## Testing
###Para ejecutar los test
coverage run -m unittest discover
### Para el % de coverage
coverage report -m