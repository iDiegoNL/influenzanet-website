from django.db import connection
from .models import UserBadge

class DataSource(object):
    def __init(self, sql):
        self.sql = sql
    
    def _get_query(self, query):
        cursor = connection.cursor()
        cursor.execute(query)
        res = cursor.fetchone()
        desc = cursor.description
        if res is not None:
            res = dict(zip([col[0] for col in desc], res))
    
    def get_for_person(self, person):
        """
         get value for a given person
        """
        query = self.sql + """ WHERE "user" = %d AND global_id = '%s'""" % (person.user_id, person.global_id)
        return self._get_query(query)

    def get_for_user(self, user):
        query = self.sql + """ WHERE "user" = %d AND global_id = '%s'""" % (user.user_id)
        return self._get_query(query)
    
class DataProvider(object):
    
    def __init__(self):
        self.sources = {}
        self.data_person = {}
        self.data_user = {}
        
    def register(self, name, dataSource):
        self.sources[name] = dataSource
    
    def get_for_user(self, name, user):
        source = self.sources[name]
    
