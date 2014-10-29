
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
