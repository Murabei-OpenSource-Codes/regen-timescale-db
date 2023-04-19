"""
Module app.py.

Flask aplication to reload database.
"""
import os
import subprocess
import requests
import logging
from flask import Flask
from .kong import register_reload_db
app = Flask(__name__)
dispose_conections_url = os.environ.get(
    'DISPOSE_CONECTIONS')

#########################################
# Get app name and build reload end-point
app_name = os.environ.get('APP_NAME')
reload_route = "/reload-db/%s/" % app_name \
    if app_name is not None else "/reload-db/"
kong_api = os.environ.get('KONG_API')
service_url = os.environ.get('SERVICE_URL')
if kong_api is not None and service_url is not None:
    register_reload_db(
        api_gateway_url=kong_api, service_name=app_name,
        service_url=service_url, reload_route=reload_route)


def dispose_conections():
    """Call end-point to dispose connections from flask or Django or etc..."""
    if dispose_conections_url is not None:
        logging.warning('request app conections pool dispose')
        for i in range(20):
            requests.get(dispose_conections_url)


@app.route(reload_route)
def reload_database():
    """
    Reload database to original state.

    Drops the public schema and reload the orinal dump file of the database
    """
    password = os.environ.get('POSTGRES_PASSWORD')
    username = os.environ.get('POSTGRES_USER')
    database = os.environ.get('POSTGRES_DB')
    if database == '' or database is None:
        database = username

    base_psql = "PGPASSWORD={password} psql -h 0.0.0.0 -p 5432 -U " +\
        "{username} postgres"
    base_psql = base_psql.format(
        password=password, username=username, database=username)

    # Timescale pre-restore
    cmd_pre_restore = base_psql + (
        " -c 'SELECT timescaledb_pre_restore();'")
    with open(os.devnull, 'w') as fp:
        pipe = subprocess.Popen(cmd_pre_restore, stdout=fp, shell=True)
    ret_code = pipe.wait()

    # Not Allow conections to database that will be removed
    cmd_noconection_database = base_psql + (
        """ -c "UPDATE pg_database SET datallowconn = 'false' """
        """WHERE datname = '{database}';" """).format(
            database=database)
    with open(os.devnull, 'w') as fp:
        pipe = subprocess.Popen(
            cmd_noconection_database, stdout=fp, shell=True)
    ret_code = pipe.wait()

    # DROP all conections to server
    cmd_dropconection_database = base_psql + (
        ''' -c '''
        '''"SELECT pg_terminate_backend(pg_stat_activity.pid) '''
        '''FROM pg_stat_activity '''
        '''WHERE pid <> pg_backend_pid();"''')
    with open(os.devnull, 'w') as fp:
        pipe = subprocess.Popen(
            cmd_dropconection_database, stdout=fp, shell=True)
    ret_code = pipe.wait()

    # DROP database to recriate using backup
    cmd_drop_database = base_psql +\
        ''' -c "DROP DATABASE {database};"'''.format(
            database=database)
    with open(os.devnull, 'w') as fp:
        pipe = subprocess.Popen(cmd_drop_database, stdout=fp, shell=True)
    ret_code = pipe.wait()

    ###################
    # Backup database #
    # DROP all conections to server
    cmd_dropconection_database = base_psql + (
        ''' -c '''
        '''"SELECT pg_terminate_backend(pg_stat_activity.pid) '''
        '''FROM pg_stat_activity '''
        '''WHERE pid <> pg_backend_pid();"''')
    with open(os.devnull, 'w') as fp:
        pipe = subprocess.Popen(
            cmd_dropconection_database, stdout=fp, shell=True)
    ret_code = pipe.wait()

    # Recriate database using backup
    cmd_create_database = base_psql +\
        " -c 'create database {database} WITH TEMPLATE backup'".format(
            database=username)
    with open(os.devnull, 'w') as fp:
        pipe = subprocess.Popen(cmd_create_database, stdout=fp, shell=True)
    ret_code = pipe.wait()

    # Timescale post-restore
    cmd_pos_restore = base_psql + (
        " -c 'SELECT timescaledb_post_restore();'")
    with open(os.devnull, 'w') as fp:
        pipe = subprocess.Popen(cmd_pos_restore, stdout=fp, shell=True)
    ret_code = pipe.wait()

    # Dispose all conections from other services if needed
    dispose_conections()

    if ret_code > 0:
        return 'false'
    else:
        return 'true'
