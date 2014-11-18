from django.db import connection
from django.utils.log import getLogger
from django.conf import settings

logger = getLogger('dashboard')

DEBUG = settings.DEBUG

class NotEvaluableNow(Exception):
    pass

class DataSource(object):
    def __init__(self, definition):
        self.need_profile = definition.get('need_profile', False)
        self.require = definition.get('require', False)

class ClassDataSource(DataSource):
    
    def __init__(self, definition, provider):
        super(ClassDataSource, self).__init__(definition)
        self.provider = provider

class SqlDataSource(DataSource):

    def __init__(self, definition):
        super(SqlDataSource, self).__init__(definition)
        self.sql = definition['sql']
        self.template = definition.get('template', False)
    
    def _get_row(self, query):
        cursor = connection.cursor()
        cursor.execute(query)
        res = cursor.fetchone()
        cursor.close()
        desc = cursor.description
        if res is not None:
            res = dict(zip([col[0] for col in desc], res))
        return res
    
    def _get_sql(self):
        # Call a function if needed, else assume that string repr produces a SQL query
        if callable(self.sql):
            return self.sql()
        return str(self.sql)
        
    def get_for_participant(self, participant):
        """
         get value for a given participant (SurveyUser instance)
        """
        query = self._get_sql()
        # If template, use dict based string formating 
        if self.template:
            query = query % { 'user': participant.user_id, 'global_id':participant.global_id, 'survey_user_id': participant.id }
        else:
            # just add where clauses
            query += """ WHERE "user" = %d AND "global_id" = '%s'""" % (participant.user_id, participant.global_id )
        row = self._get_row(query)
        if DEBUG:
            logger.debug(query)
            logger.debug(row)
        return row

    def get_for_user(self, user):
        """
         get a row for a user account (django User instance)
        """
        query = self._get_sql() 
        if self.template:
            query = query % { 'user': user.id }
        else:
            query += """ WHERE "user" = %d""" % (user.id)
        row = self._get_row(query)
        if DEBUG:
            logger.debug(query)
            logger.debug(row)
        return row