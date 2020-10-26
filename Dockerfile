# Dockerfile - this is a comment. Delete me if you want.
FROM python:3.6
COPY . /app
WORKDIR /app
#RUN pip install -r requirements.txt
#RUN pip install -e .
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=/app/fxprofile
ENV HOST=0.0.0.0

RUN pip install -r requirements.txt
RUN pip install -e .
#ENTRYPOINT ["flask"]
#CMD ["run"]
#ENTRYPOINT FLASK_APP=profile flask run --host=0.0.0.0 --port=$PORT
#ENTRYPOINT FLASK_APP=fxprofile waitress-serve --port $PORT --call "fxprofile:create_app"
# install dependencies


EXPOSE 5000
#ENTRYPOINT waitress-serve --port $PORT --call "fxprofile:create_app"
ENTRYPOINT /app/start.sh
