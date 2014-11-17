from ..datasource import DataSource, DEBUG

DATA_SOURCES_CHOICES = (
  ('loyalty', 'Loyalty for the 2011-2012 season'),                     
  ('participation','Participation for the weekly survey'),
  ('pioneer14','First person in town (2014)'),
  ('none','No data source (not computed)')                      
) 

class NoviceDataSource(DataSource):
    
    def __init__(self, definition, provider):
        super(NoviceDataSource, self).__init__(definition)
        self.provider = provider
    
    def get_for_participant(self, participant):
        loyalty = self.provider.get_for_participant('loyalty', participant)
        if loyalty is not None:
            return {'novice': False}
        return {'novice': True}
        
    def get_for_user(self, user):
        raise Exception("NoviceDataSource is not a user based badge")


DATA_SOURCES_DEFINITIONS = {
   'loyalty': {
       'type': 'sql',
       'sql': 'select "first_season" > 0 as loyalty from grippenet_participation where survey_user_id=%(survey_user_id)',
       'template': True,        
    },
   'participation': {
       'type': 'sql',
       'sql': 'select * from pollster_dashboard_badges_2014'        
    },
    'has_profile': {
        'type': 'sql',
        'sql': 'select count(id) > 0 as has_profile from pollster_results_intake'
    },
    # -- Is there anyone else in the same town as me
    #    select sum(case when "global_id"='471fbd68-977f-4f59-a4d1-7b73e666408d' then 0 else 1 end)=0 from pollster_results_intake
    #    where "Q3"=(select "Q3" from pollster_results_intake where global_id='471fbd68-977f-4f59-a4d1-7b73e666408d' order by timestamp desc limit 1) 
    'pioneer14': {
        'type': 'sql',
        'sql': """select 
            sum(case when "global_id"='%(global_id)s' then 0 else 1 end)=0 as pioneer from pollster_results_intake 
            where "Q3"=(select "Q3" from pollster_results_intake where global_id='%(global_id)s' order by timestamp desc limit 1)
            """,
        'template': True,
        'need_profile': True,
    },
    'novice': {
        'type': 'class',
        'class': NoviceDataSource,
        'need_profile': True,
    }
}
