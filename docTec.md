# Profile Service - BackEnd

## Documentación técnica

Dentro de los requerimientos se encuentran:

Base de datos postgres - SQL Alchemy

flasgger para Swagger

flask_mail para mail desde GMail y recover token

waitress para usarlo como Web Server.

flask_cors CORS

### Errores como Clases.

ProfileAppException -> APIKeyError -> APIKeyNotExistent

ProfileAppException -> ProfileError -> ProfileNotExistentByDescription
ProfileAppException -> ProfileError -> ProfileNotExistentById

ProfileAppException -> UsersError -> UserNotExistentError
ProfileAppException -> UsersError -> UserIsNotAnAdminError
ProfileAppException -> UsersError -> UserIdentifierAlreadyTaken
ProfileAppException -> UsersError -> UserPasswordMustNotBeEmpty
ProfileAppException -> UsersError -> UserPasswordInvalid
ProfileAppException -> UsersError -> UserMailInvalid
ProfileAppException -> UsersError -> EmptyModifySchema
ProfileAppException -> UsersError -> UserTypeNotExistentError
ProfileAppException -> UsersError -> UserGoogleValidateFailed
ProfileAppException -> UsersError -> UserIsNotGoogleUserError
ProfileAppException -> UsersError -> UserIsGoogleUserError
ProfileAppException -> UsersError -> UserIsBlockedError
ProfileAppException -> UsersError -> UserTokenRecoverError
ProfileAppException -> UsersError -> UserTokenRecoverExpiredError


## Instalación y configuración

### Webserver Local

Exportar variables de ambiente según configuración elegida:

```sh
export APP_SETTINGS=config.TestingWithDBConfig
```

Levantar a través de:

```sh
waitress-serve --call profileapp:create_app
```

### Development container mode

Levantar containers con la postegres db, otro con la app web (además se crean las tablas) y un server para mockear el Google Server.

```sh
docker-compose build
docker-compose up
```

### Docker - Heroku

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

## Definición de arquitectura

SERVER <-> POSTGRES DB


## Especificación de API REST: OpenAPI