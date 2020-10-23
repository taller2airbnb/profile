# Profile - Flask App

## Development container mode

*docker-compose build*

Crea los cotainers.

*docker-compose up*

Levanta un container con la postegres db y otro con la web (además se crean las tablas). 

## Docker - Heroku

*docker build -t taller2airbnb-profile:latest .*

Y usa su variable de ambiente para pegarle a la db de heroku.

Para ejecutar los test
coverage run -m unittest discover
Para el % de coverage
coverage report -m