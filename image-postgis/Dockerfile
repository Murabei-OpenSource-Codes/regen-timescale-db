FROM postgis/postgis:15-3.3-alpine

########################
# ENV DISPOSE_CONECTIONS
# ENV APP_NAME
# ENV KONG_API
# ENV SERVICE_URL
# ENV DISPOSE_CONECTIONS
########################

ENV FLASK_APP app/app.py
ENV POSTGRES_EXTRA_ARGS=""

EXPOSE 5432
EXPOSE 5000

RUN apk update
RUN apk upgrade --available
RUN apk add bash su-exec

###############################################
# Install flask dependencies to backup database
RUN apk add g++ python3-dev libffi-dev curl
RUN apk add python3 py3-pip
RUN pip3 install --upgrade pip setuptools==67.7.0

COPY requirements/ /requirements
RUN pip3 install -r requirements/python_requirements.txt
###############################################

COPY app/ /app
RUN chmod 777 -R app
RUN chown postgres:postgres -R app

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod 777 /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

COPY start_container.bash /start_container.bash
COPY wait-for-kong.bash /wait-for-kong.bash
RUN chmod +x ./start_container.bash
RUN chmod +x ./wait-for-kong.bash

#####################################################
# Copia os scripts para a criação da base de backup #
COPY docker-entrypoint-initdb.d/* /docker-entrypoint-initdb.d/
#####################################################

CMD ["./start_container.bash"]
