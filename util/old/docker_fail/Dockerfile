FROM python:3.5-stretch

RUN apt-get update && apt-get upgrade -y && apt-get autoremove

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN django-admin startproject tln

WORKDIR /tln
RUN mkdir util

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4 && \
    echo "deb http://repo.mongodb.org/apt/debian stretch/mongodb-org/4.0 main" | tee /etc/apt/sources.list.d/mongodb-org-4.0.list && \
    apt-get update && apt-get install -y mongodb-org

COPY util/mongo_docker.sh util/critique.2019-07-23.gz util/
RUN chmod 777 util/mongo_docker.sh
CMD util/mongo_docker.sh

COPY util/critique.2019-07-23.gz util/
WORKDIR /tln/util
CMD mongorestore --gzip --archive=critique.2019-07-23.gz
WORKDIR /tln

#RUN python manage.py startapp blog && python manage.py startapp boch && python manage.py startapp django_comments_custom && python manage.py startapp home && python manage.py startapp photos
COPY blog ./blog
COPY boch ./boch
COPY django_comments_custom ./django_comments_custom
COPY home ./home
COPY net ./net
COPY photos ./photos
COPY static ./static
COPY tln ./tln

COPY critique/templates critique/templates
COPY critique/templatetags critique/templatetags
COPY critique/admin.py critique/apps.py critique/context_processors.py critique/forms.py critique/__init__.py critique/models.py critique/tests.py critique/urls.py critique/views.py critique/
RUN find . -name '*.pyc' -delete

#RUN rm -r */migrations
RUN find */migrations/* ! -name '__init__.py' -delete
COPY db.sqlite3 util/db.sqlite3.old
#COPY db.sqlite3 .
RUN python manage.py makemigrations && python manage.py migrate
COPY util/fix_broken_sqlite3.py util/
RUN python util/fix_broken_sqlite3.py util/db.sqlite3.old db.sqlite3
COPY util/fix_photologue_models.py /usr/local/lib/python3.5/site-packages/photologue/models.py

EXPOSE 8000
STOPSIGNAL SIGINT
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver"]
