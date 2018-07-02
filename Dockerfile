FROM python:3.6-slim
RUN echo 'Dockerfile-App'
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
#ENTRYPOINT flask run --no-reload --host=0.0.0.0
ENTRYPOINT gunicorn -w 4 application:app -b 0.0.0.0:5000