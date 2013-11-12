from django.db import connection
from .utils import get_current_season, historical_table
from django.utils.log import getLogger
from django.contrib.auth.models import User
from django.conf import settings
from functools import partial

logger = getLogger('dashboard')

DEBUG = settings.DEBUG

DATA_SOURCES_CHOICES = (
  ('loyalty1', 'Loyalty for the 2011-2012 season'),                     
  ('loyalty2', 'Loyalty for the 2012-2013 season'),                     
  ('participation','Participation for the weekly survey'),
  ('pioneer','First person in town')                      
) 

def loyalty_sql_provider(year, name):
    table = historical_table(year, 'weekly')
    query = "SELECT COUNT(*) > 0 as %s FROM %s " % (name, table,)
    return query

DATA_SOURCES_DEFINITIONS = {
   'loyalty1': {
       'type': 'sql',
       'sql': partial(loyalty_sql_provider, year=2011, name='loyalty1')        
    },
   'loyalty2': {
       'type': 'sql',
       'sql': partial(loyalty_sql_provider, year=2012, name='loyalty2')        
    },
   'participation': {
       'type': 'sql',
       'sql': 'select * from pollster_dashboard_badges'        
    },
    'has_profile': {
        'type': 'sql',
        'sql': 'select count(id) > 0 as has_profile from pollster_results_intake'
    },
    # -- Is there anyone else in the same town as me
    #    select sum(case when "global_id"='471fbd68-977f-4f59-a4d1-7b73e666408d' then 0 else 1 end)=0 from pollster_results_intake
    #    where "Q3"=(select "Q3" from pollster_results_intake where global_id='471fbd68-977f-4f59-a4d1-7b73e666408d' order by timestamp desc limit 1) 
    'pioneer': {
        'type': 'sql',
        'sql': """select 
            sum(case when "global_id"='%(global_id)s' then 0 else 1 end)=0 as pioneer from pollster_results_intake 
            where "Q3"=(select "Q3" from pollster_results_intake where global_id='%(global_id)s' order by timestamp desc limit 1)
            """,
        'template': True,
        'need_profile': True,
    },
}

DS_HAS_PROFILE = 'has_profile'


class NotEvaluableNow(Exception):
    pass


class DataSource(object):

    def __init__(self, definition):
        self.sql = definition['sql']
        self.template = definition.get('template', False)
        self.need_profile = definition.get('need_profile', False)
    
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
            query = query % { 'user': participant.user_id, 'global_id':participant.global_id }
        else:
            # just add where clauses
            query += """ WHERE "user" = %d AND "global_id" = '%s'""" % (participant.user_id, participant.global_id )
        if DEBUG:
            logger.debug(query)
        return self._get_row(query)

    def get_for_user(self, user):
        """
         get a row for a user account (django User instance)
        """
        query = self._get_sql() 
        if self.template:
            query = query % { 'user': user.user_id }
        else:
            query += """ WHERE "user" = %d""" % (user.user_id)
        if DEBUG:
            logger.debug(query)
        return self._get_row(query)
    
    
class BadgeProvider(object):
    """
    Provide data access to update badge status
    This provider is dependent of a given user or participant (uses a cache)
    A datasource could be used for several badges (query is computed once and could produce several column
    The column for a badge state should have the name of the column in the query
    """
    
    def __init__(self):
        self.sources = {}
        self.data_participant = {}
        self.data_user = {}
        
        # register datasources
        for name in DATA_SOURCES_DEFINITIONS:
            definition = DATA_SOURCES_DEFINITIONS[name]
            ds = DataSource(definition)
            self.sources[name] = ds
     
    def get_for_user(self, name, user):
        
        if self.data_user.has_key(name):
            return self.data_user[name]
        
        try:
            source = self.sources[name]
        except KeyError:
            raise Exception("Unknown data source %s" % name)
        
        if DEBUG:
            logger.debug(u'Fetching %s for user %d' % (name,user.id))
        data = source.get_for_user(user)
        
        # Cache the value (even it is
        self.data_user[name] = data
        
        return data

    def get_for_participant(self, name, participant):
        """
         get data for a participant instance (SurveyUser)
        """
        
        if self.data_participant.has_key(name):
            return self.data_participant[name]
        
        try:
            source = self.sources[name]
        except KeyError:
            raise Exception("Unknown data source %s" % name)
        
        if source.need_profile and name != DS_HAS_PROFILE:
            if DEBUG:
                logger.debug('Fetching profile for participant %d' % participant.id)
            profile = self.get_for_participant(DS_HAS_PROFILE, participant)
            if not profile['has_profile']:
                logger.debug('No profile for this participant, raise NotEvaluableNow')
                raise NotEvaluableNow()
        
        if DEBUG:
            logger.debug(u'Fetching %s for participant %d' % (name, participant.id))
        data = source.get_for_participant(participant)
        
        # Cache the value (even it is an empty value)
        self.data_participant[name] = data   
        
        return data         
        
    def update(self, badge, attribute_to):
        dsname = badge.datasource
        if isinstance(attribute_to, User):
            b = self.get_for_user(dsname, attribute_to)
        else:
            b = self.get_for_participant(dsname, attribute_to)
        if b:
            try:
                badge_name = badge.name
                state = b[badge_name]
                if DEBUG:
                    logger.debug('badge %s has state %d' % (badge_name, state))
                return state
            except KeyError:
                raise Exception("Unknown column '%s' for datasource '%s' " % (badge_name, dsname))
        
        # no data, assume the badge is not attributed
        return False 