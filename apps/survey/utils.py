from django.conf import settings

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

def get_avatars_url():
    
    """
    Return the avatar configuration if activated, None otherwise 
    list :list of available avatars (list of the file number in the SURVEY_AVATARS directory (subdirectory of media)
    An avatar is just a 32x32 png image
    url: url to the avatar dir
    """
    
    SURVEY_AVATARS = getattr(settings, 'SURVEY_AVATARS', None)
    
    ## Path to the avatars files, relative to media directory
    if not SURVEY_AVATARS:
        return None
    return settings.MEDIA_URL + '/' + SURVEY_AVATARS.strip('/') + '/'
