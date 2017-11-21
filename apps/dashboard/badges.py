from django.contrib.auth.models import User
from .datasource import DataSource, SqlDataSource, NotEvaluableNow, logger, DEBUG

from .definitions.season2017 import DATA_SOURCES_CHOICES, DATA_SOURCES_DEFINITIONS #keep DATA_SOURCE_CHOICES, imported in models

DS_HAS_PROFILE = 'has_profile'

class BadgeProvider(object):
    """
    Badge provider computes the state of a badge, using a named datasource
    A badge only knows : a data source name, and field name in the result from the data source

    A provider instance is made for given user or participant (data are cached for the curent user)

    A datasource can be used for several badges (query is computed once and could produce several column
    The column for a badge state should have the name of the column in the query
    """

    def __init__(self):
        self.sources = {}
        self.data_participant = {}
        self.data_user = {}

        # register datasources
        for name in DATA_SOURCES_DEFINITIONS:
            definition = DATA_SOURCES_DEFINITIONS[name]
            type = definition['type']
            ds = None
            if type == 'sql':
                ds = SqlDataSource(definition)
            if type == 'class':
                klass = definition['class']
                ds =  klass(definition, self)
            self.sources[name] = ds

    def get_for_user(self, source_name, user):

        if self.data_user.has_key(source_name):
            return self.data_user[source_name]

        try:
            source = self.sources[source_name]
        except KeyError:
            raise Exception("Unknown data source %s" % source_name)

        if DEBUG:
            logger.debug(u'Fetching %s for user %d' % (source_name,user.id))
        data = source.get_for_user(user)

        # Cache the value (even it is
        self.data_user[source_name] = data

        return data

    def get_for_participant(self, source_name, participant):
        """
         get data for a participant instance (SurveyUser)
        """
        if DEBUG:
            logger.debug('get "%s" for participant %d' % (source_name, participant.id))

        if self.data_participant.has_key(source_name):
            logger.debug('"%s" found in cache' % (source_name))
            return self.data_participant[source_name]

        try:
            source = self.sources[source_name]
        except KeyError:
            raise Exception("Unknown data source %s" % source_name)

        if source.need_profile and source_name != DS_HAS_PROFILE:
            if DEBUG:
                logger.debug('Fetching profile for participant %d' % participant.id)
            profile = self.get_for_participant(DS_HAS_PROFILE, participant)
            if profile is None or not profile['has_profile']:
                if DEBUG:
                    logger.debug('No profile for this participant, raise NotEvaluableNow')
                raise NotEvaluableNow()

        if source.require:
            """
             list of required flag in data
             require list is defined : source_name.variable_name
             The value should be True (or evaluable as is) to fill the requirement
             raise an NotEvaluableNow exception is any requirement is not satisfied
            """
            if DEBUG:
                logger.debug('Fetching requirements for participant %d' % participant.id)
            for r in source.require:
                r_source, r_var = r.split('.')
                if r_source == source_name:
                    raise Exception('Unable to require same source')
                if r_var is None or r_source is None:
                    raise Exception('Unable to require "',str(r),", not a complete spec")
                r_data = self.get_for_participant(r_source, participant)
                if r_data is None:
                    raise NotEvaluableNow()
                try:
                    r_value = r_data.get(r_var)
                except KeyError:
                    raise Exception('Unable to find '+ r_var+' in data source '+ r_source)
                if not r_value:
                    raise NotEvaluableNow()
        if DEBUG:
            logger.debug(u'Fetching %s for participant %d' % (source_name, participant.id))
        data = source.get_for_participant(participant)

        # Cache the value (even it is an empty value)
        self.data_participant[source_name] = data

        return data

    def update(self, badge, attribute_to):
        """
         Get a badge state from its data source
        """
        dsname = badge.datasource
        if dsname == 'none':
            # Special datasource used for 'fake' badge
            # That should not been computed by this way
            raise NotEvaluableNow()
        # Get the data row from the data source
        if isinstance(attribute_to, User):
            b = self.get_for_user(dsname, attribute_to)
        else:
            b = self.get_for_participant(dsname, attribute_to)
        if b:
            try:
                # The state of the badge should be in the column named as the badge's name
                badge_name = badge.name
                state = b[badge_name]
                if DEBUG:
                    logger.debug('badge %s has state %d' % (badge_name, state))
                return state
            except KeyError:
                raise Exception("Unknown column '%s' for datasource '%s' " % (badge_name, dsname))

        # no data, assume the badge is not attributed
        return False
