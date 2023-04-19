FROM postgis/postgis:15-3.3

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

RUN apt update
RUN apt upgrade
RUN apt install -y bash

###############################################
# Install flask dependencies to backup database
RUN apt install -y python3 python3-dev python3-distutils
RUN apt install -y python3-pip

# Install virtualenv
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3.8 get-pip.py
RUN pip3.8 install --upgrade pip

RUN apt install -y g++ python3-dev libffi-dev curl
RUN apt install -y python3 py3-pip
RUN pip3 install --upgrade pip setuptools==45

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
