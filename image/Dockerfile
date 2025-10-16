FROM postgis/postgis:17-master

########################
# ENV DISPOSE_CONECTIONS
# ENV APP_NAME
# ENV KONG_API
# ENV SERVICE_URL
########################

ENV FLASK_APP="app/app.py"
ENV POSTGRES_EXTRA_ARGS=""

EXPOSE 5432
EXPOSE 5000

RUN apt-get update
RUN apt-get -y upgrade

########################################
# Install pgvector used on some projects
RUN apt-get install -y postgresql-17-pgvector

###############################################
# Install flask dependencies to backup database
RUN apt-get install -y g++ python3-dev libffi-dev curl
RUN apt-get install -y python3 python3-pip python3-virtualenv
RUN virtualenv env
ENV PATH="/env/bin:$PATH"

COPY requirements/ /requirements
RUN pip3 install -r requirements/python_requirements.txt

#######################################
# Copy Flask App to reload the database
COPY app/ /app
RUN chmod 777 -R app
RUN chown postgres:postgres -R app

#####################################################
# Copia os scripts para a criação da base de backup #
COPY docker-entrypoint-initdb.d/* /docker-entrypoint-initdb.d/
RUN chown -R postgres:postgres docker-entrypoint-initdb.d/

#########################
# Return user to Postgres
USER postgres
