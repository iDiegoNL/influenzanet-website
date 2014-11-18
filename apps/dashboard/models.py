from django.db import models
from django.contrib.auth.models import User
from apps.survey.models import SurveyUser
from .badges import BadgeProvider, DATA_SOURCES_CHOICES
from .utils import get_current_season
from .datasource import NotEvaluableNow

ATTRIBUTE_TO_USER = 'U'
ATTRIBUTE_TO_PARTICIPANT = 'P'

BADGE_ATTRIBUTION_CHOICES = (
 (ATTRIBUTE_TO_USER, 'User'),
 (ATTRIBUTE_TO_PARTICIPANT,'Participant'),                
)        

CURRENT_SEASON = get_current_season()

class Badge(models.Model):
    """ Badge Definition """
    
    # Internal name
    # used to get the property from datasource as a datasource can provide several results for kind of badge
    name = models.CharField(max_length=64, unique=True)

    # Label to give a name to the badge showed to the user
    label = models.TextField()

    description = models.TextField()
    
    # Name of a registred Datasource for badge
    # A data source
    datasource = models.CharField(max_length=64, choices=DATA_SOURCES_CHOICES)
    
    attribute_to = models.CharField(max_length=1, choices=BADGE_ATTRIBUTION_CHOICES)
               
    # If defined, depends on one season
    # Take the value of the year of the season starting (see SEASON_STARTING_MONTH in badges)
    season = models.IntegerField(null=True, blank=True, default=None)
    season.help_text = 'If has a value, this badge is specific for a season and wont be recomputed after the next september of (season+1)'
    
    # Should only be computed once and the result stored, no recomputing needed or possible
    compute_once = models.BooleanField(default=False)
    
    # Should show this badge (will be always hidden if false)
    visible = models.BooleanField(default=True)
           
    def can_compute(self):
        if self.season:
            season = CURRENT_SEASON
            if season != self.season:
                return False
        return True
    
class UserBadgeManager(models.Manager):
    
    def __init__(self):  
        super(UserBadgeManager, self).__init__()
        self._badges = None
        
    def get_badges(self, indexed=False):
        """
         get the badge list
         if indexed, return a dictionnary index by id (for lookup)
        """
        if self._badges is None:
            bb = []
            for b in list(Badge.objects.all()):
                if b.can_compute():
                    bb.append(b)  
            self._badges = bb
        if indexed:
            badges = {  }
            names = {}
            for b in self._badges:
                badges[ b.id ] = b
                names[ b.name ] = b
            return (badges, names)
        return self._badges
    
    def get_attributed_badges(self, user=None, participant=None):
        """
            Get attributed badges
        """
        if user is not None:
            user_badges = self.filter(user=user, participant=None)
        
        if participant is not None:
            user_badges = self.filter(participant=participant)
        
        return user_badges
        
    def update_badges_for(self, participant=None, user=None, fake=False):
        
        """
        Perform a badge update for a participant
        """
        
        provider = BadgeProvider()
        
        badges = self.get_badges()
        
        if participant:
            attributed_badges = self.get_attributed_badges(participant=participant)
            attribute_to = ATTRIBUTE_TO_PARTICIPANT
            who = participant
        else:
            attributed_badges = self.get_attributed_badges(user)
            attribute_to = ATTRIBUTE_TO_USER
            who = user
        
        attributed_badges = [ b.badge_id for b in attributed_badges  ]
        
        new_badges = []
        for badge in badges:
            if badge.attribute_to != attribute_to:
                continue
            if badge.id in attributed_badges:
                # Already attributed, no "update" for a badge
                continue
            try:
                has_badge = provider.update(badge, who)
            except NotEvaluableNow:
                # Some datasource can raise it if preconditions are not filled up
                continue
            if badge.compute_once:
                # Always attribute the badge to the user
                attribute_badge = True
                # Store the computed value (has the badge or not)
                # in the badge state
                state = True if has_badge else False # force to be boolean
            else:
                # Only attribute badge with a state to True
                # If attributed, the badge state is always "True" (showed) for this badge
                # If state is False, the badge is not attributed, and will be recomputed next time
                state = True
                attribute_badge = has_badge
            if attribute_badge:
                if state:
                    # Only attribute badge with state true (attributed)
                    new_badges.append(badge.id)
                if not fake:
                    b = UserBadge()
                    if attribute_to == ATTRIBUTE_TO_USER:
                        b.user_id = user.id
                        b.participant = None
                    else:
                        b.participant = participant
                        b.user_id = participant.user_id
                    b.state = state
                    b.badge = badge
                    b.save()
                
        return {'new': new_badges, 'old': attributed_badges }    
    
    def update_badges(self, participant, fake=False):
        p = self.update_badges_for(participant=participant, fake=fake)
        u = self.update_badges_for(user=participant.user, fake=fake)
        first =  len(p['new']) > 0 and len(p['old']) == 0
        return {'participant':p['new'], 'user': u['new'], 'first': first}

        
class UserBadge(models.Model):
    """
     Badges attributed to account user and participant
     if participant is not set, this is a user account based badge
    """
    user = models.ForeignKey(User)
    participant = models.ForeignKey(SurveyUser, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    badge = models.ForeignKey(Badge)
    
    ## Badge state 
    # Badge is won if state is true. 
    # Some badge could have been attributed with a state set to false, if the value cannot be recomputed
    # later (or do not need to for perf reason).
    # In this case, the badge is attributed and remains hidden for the participant.
    state = models.BooleanField() 
    
    class Meta:
        unique_together = (("user","participant","badge"))
    
    objects = UserBadgeManager()