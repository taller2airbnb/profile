[![codecov](https://codecov.io/gh/taller2airbnb/profile/branch/main/graph/badge.svg?token=I719YMGKSD)](https://codecov.io/gh/taller2airbnb/profile)


# Profile Services - Flask App - API

## Webserver Local

Exportar variables de ambiente según config elegida:

- *export APP_SETTINGS=config.TestingWithDBConfig*

Levantar a través de:

- *waitress-serve --call profileapp:create_app*

## Development container mode

- *docker-compose build*

Crea los cotainers.

- *docker-compose up*

Levanta un container con la postegres db y otro con la web (además se crean las tablas). 

## Docker - Heroku

- *docker build -t taller2airbnb-profile:latest .*

Y usa su variable de ambiente para pegarle a la db de heroku.

## Testing
### En caso de no tener postgres instalado:
- docker-compose build db
- docker-compose up db
### Levantar mock server para google token
- docker-compose build google
- docker-compose up google
###Para ejecutar los test
- coverage run -m pytest
### Para el % de coverage
- coverage report -m