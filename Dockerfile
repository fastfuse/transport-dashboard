FROM python:3.6
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
ENTRYPOINT flask run --no-reload --host=0.0.0.0
#ENTRYPOINT gunicorn -w 4 application:app



#FROM python:3
#
#EXPOSE 8000
#ENV PYTHONUNBUFFERED=0
#RUN useradd -ms /bin/bash dc
#RUN chgrp -R 0 /home/dc && chmod -R g=u /home/dc
#ENV APP_HOME /home/dc
#WORKDIR $APP_HOME
#ADD requirements.txt requirements.txt
#RUN pip install -r requirements.txt
#COPY . .
#USER dc
#RUN python manage.py collectstatic --no-input
#ENTRYPOINT python manage.py makemigrations && python manage.py migrate && uwsgi --ini uwsgi.ini
