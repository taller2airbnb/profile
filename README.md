# profile

flask create-db
flask run


docker build -t taller2airbnb-profile:latest .

docker run -e PORT=5000 -e APP_SETTINGS="config.DevelopmentConfig" -p 5000:5000 taller2airbnb-profile

docker-compose run web bash 
y luego
flask create-db

docker exec -it profile_db_1 psql -U postgres