# Dockerfile - this is a comment. Delete me if you want.
FROM python:3.6
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install -e .
#RUN export FLASK_APP=profile
EXPOSE 5000
#ENTRYPOINT ["flask"]
#CMD ["run"]
ENTRYPOINT FLASK_APP=profile flask run --host=0.0.0.0

