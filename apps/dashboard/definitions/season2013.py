from functools import partial
from ..utils import historical_table

DATA_SOURCES_CHOICES = (
  ('loyalty1', 'Loyalty for the 2011-2012 season'),                     
  ('loyalty2', 'Loyalty for the 2012-2013 season'),                     
  ('loyalty3', 'Loyalty for the 2013-2014 season'),                     
  ('participation','Participation for the weekly survey'),
  ('pioneer','First person in town'),
  ('none','No data source (not computed)')                      
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
   'loyalty3': {
       'type': 'sql',
       'sql': partial(loyalty_sql_provider, year=2013, name='loyalty3')        
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
