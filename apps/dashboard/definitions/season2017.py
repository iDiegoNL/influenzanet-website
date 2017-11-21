from ..datasource import DataSource, ClassDataSource, DEBUG, NotEvaluableNow

DATA_SOURCES_CHOICES = (
  ('loyalty', 'Loyalty for the 2011-2012 season'),
  ('participation','Participation for the weekly survey'),
  ('pioneer14','First person in town (2014)'),
  ('pioneer14dep','First person in department (2014)'),
  ('novice','is novice'),
  ('household_participation','Household participation'),
  ('household', 'Household'),
  ('profile','Profile data (intake)'),
  ('pregnant_pioneer','Pregnant is pionneer ?'),
  ('none','No data source (not computed)')
)


class NoviceDataSource(ClassDataSource):

    def get_for_participant(self, participant):
        loyalty = self.provider.get_for_participant('loyalty', participant)
        if loyalty is not None:
            return {'novice': False}
        return {'novice': True}

    def get_for_user(self, user):
        raise Exception("NoviceDataSource is not a user based badge")

class HouseholdDataSource(ClassDataSource):

    def get_for_participant(self, participant):
        raise Exception("HouseholdDataSource is not a participant based badge")

    def get_for_user(self, user):
        h = self.provider.get_for_user('household_participation', user)
        if h is None:
            raise NotEvaluableNow()
        has_weekly = h['household_1_weekly']
        nb = h['household_nb']
        h['household_2'] =  (nb == 2) & has_weekly
        h['household_3'] = (nb == 3) & has_weekly
        h['household_4'] = (nb == 4) & has_weekly
        h['household_5'] = (nb >= 5) & has_weekly
        return h

class PregnantProfileDataSource(ClassDataSource):

    def get_for_participant(self, participant):
        profile = self.provider.get_for_participant('profile', participant)
        if profile is None:
            raise NotEvaluableNow()
        h = {}
        return h

DATA_SOURCES_DEFINITIONS = {
   'loyalty': {
       'type': 'sql',
       'sql': 'select "first_season" > 0 as loyalty from grippenet_participation where survey_user_id=%(survey_user_id)s',
       'template': True,
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
    'pioneer14': {
        'type': 'sql',
        'sql': """select
            sum(case when "global_id"='%(global_id)s' then 0 else 1 end)=0 as pioneer14 from pollster_results_intake
            where "Q3"=(select "Q3" from pollster_results_intake where global_id='%(global_id)s' order by timestamp desc limit 1)
            """,
        'template': True,
        'need_profile': True,
    },
    'pioneer14dep': {
        'type': 'sql',
        'sql': """select
            sum(case when i."global_id"='%(global_id)s' then 0 else 1 end)=0 as "pioneer14dep" from pollster_results_intake i
            where left(i."Q3",2)=(select left("Q3",2) from pollster_results_intake where global_id='%(global_id)s' order by timestamp desc limit 1)
            """,
        'template': True,
        'need_profile': True,
    },
    'novice': {
        'type': 'class',
        'class': NoviceDataSource,
        'need_profile': True,
    },
    'household_participation': {
        'type': 'sql',
        'sql': 'select * from pollster_dashboard_badges_household',
        'require': ['household_participation'],
    },
    'household': {
        'type': 'class',
        'class': HouseholdDataSource,
        'require': ['household_participation'],
    },
    'profile': {
        'type': 'sql',
        'sql': """select
                    (case when "Q7"=1 then 1 else 0 end) as biking,
                    (case when "Q7"=0 then 1 else 0 end) as walking,
                    (case when "Q7"=4 then 1 else 0 end) as public_transport,
                    (case when "Q10"=0 and ("Q10c_0"::int=1 OR "Q18"=1) then 1 else 0 end) as prevention_grippe,
                    (case when "Q13"=6 then 1 else 0 end) as stop_tabac,
                    (case when "Q12"=0 then 1 else 0 end) as pregnant,
                    (case when ("Q12"=0) and ("Q13"=7) then 1 else 0 end) as pregnant_tabac
                    from pollster_results_intake where global_id='%(global_id)s' order by "timestamp" desc limit 1
               """,
        'template': True,
        'need_profile': True,
    },
    'pregnant': {
        'type': 'class',
        'class': PregnantProfileDataSource,
        'need_profile': True,
    },
    'pregnant_pioneer': {
        'type': 'sql',
        'sql': """select
            sum(case when "global_id"='%(global_id)s' then 0 else 1 end)=0 as pregnant_pioneer from pollster_results_intake
            where
                "Q3"=(select "Q3" from pollster_results_intake where global_id='%(global_id)s' order by timestamp desc limit 1)
                and "Q12"=0
            """,
        'template': True,
        'need_profile': True,
        'require': ['profile.pregnant']
    },

}