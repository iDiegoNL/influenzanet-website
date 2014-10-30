from django.db import connection

import re

def get_db_type(connection):
    db = None
    if connection.settings_dict['ENGINE'] == "django.db.backends.sqlite3":
        db = "sqlite"
    elif connection.settings_dict['ENGINE'] == "django.db.backends.postgresql":
        db = "postgresql"
    elif connection.settings_dict['ENGINE'] == "django.db.backends.postgresql_psycopg2":
        db = "postgresql"
    elif connection.settings_dict['ENGINE'] == "django.db.backends.mysql":
        db = "mysql"
    return db

DB_TYPE = get_db_type(connection)

def get_cursor():
    """
        return a cursor on default connexion
        Use this function to avoid error warning (connection.cursor is not reacheable)
    """
    return connection.cursor()


def sql_param(name):
    """
        Transform a param name to 
    """
    if DB_TYPE == "postgresql":
        return '%(' + name +')s'
    return ':' + name

sql_name = connection.ops.quote_name

def quote_query(query):
    """
        Create a db engine specific query from a template quoting names with the proper fashion
        object names to quote (column names) should be in {{name}} for column name
    """
    def qn(matches):
        return sql_name(matches.group(1))
    
    return re.sub(r"\{\{(\w+)\}\}",qn, query)