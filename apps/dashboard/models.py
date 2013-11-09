from django.db import models
from django.contrib.auth.models import User
from apps.survey.models import SurveyUser
from .badges import BadgeProvider, DATA_SOURCES_CHOICES
from .utils import get_current_season

ATTRIBUTE_TO_USER = 'U'
ATTRIBUTE_TO_PARTICIPANT = 'P'

BADGE_ATTRIBUTION_CHOICES = (
 (ATTRIBUTE_TO_USER, 'User'),
 (ATTRIBUTE_TO_PARTICIPANT,'Participant'),                
)

class Badge(models.Model):
    """ Badge Definition """
    
    # Internal name
    # used to get the property from datasource as a datasource can provide several results for kind of badge
    name = models.CharField(max_length=64)

    # Label to give a name to the badge showed to the user
    label = models.TextField()

    description = models.TextField()
    
    # Name of a registred Datasource for badge
    # A data source
    datasource = models.CharField(max_length=64, choices=DATA_SOURCES_CHOICES)
    
    attribute_to = models.CharField(max_length=1, choices=BADGE_ATTRIBUTION_CHOICES)
               
    # If defined, depends on one season
    # Take the value of the year of the season starting (see SEASON_STARTING_MONTH in badges)
    season = models.IntegerField(null=True, default=None)
    season.help_text = 'If has a value, this badge is specific for a season and wont be recomputed after the next september of (season+1)'
    
    def is_for_user(self):
        return self.attribute_to == ATTRIBUTE_TO_USER
    
    def is_for_participant(self):
        return self.attribute_to == ATTRIBUTE_TO_PARTICIPANT
        
    def can_compute(self):
        if self.season:
            season = get_current_season()
            if season != self.season:
                return False
        return True
    
class UserBadgeManager(models.Manager):
        
    def get_badges(self):
        badges = list(Badge.objects.all())
        return badges
    
    def get_attributed_badges(self, user=None, participant=None):
        """
            Get attributed badges
        """
        if user is not None:
            user_badges = self.filter(user=user, participant=None)
        
        if participant is not None:
            user_badges = self.filter(participant=participant)
        
        # Create a lookup with badge id
        olds = {}
        for o in user_badges:
            olds[o.badge_id] = o
        return olds
        
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
        
        new_badges = []
        for badge in badges:
            if badge.attribute_to != attribute_to:
                continue
            if attributed_badges.has_key(badge.id):
                # Already attributed, no "update" for a badge
                continue
            has_badge = provider.update(badge, who)
            if not fake and has_badge:
                b = UserBadge()
                if attribute_to == ATTRIBUTE_TO_USER:
                    b.user_id = user.id
                    b.participant = None
                else:
                    b.participant = participant.id
                    b.user_id = participant.user_id
                b.badge = badge
                b.save()
                new_badges += badge
        return new_badges    
    
    def update_badges(self, participant, fake=False):
        p = self.update_badges_for(participant=participant, fake=fake)
        u = self.update_badges_for(user=participant.user, fake=fake)
        return {'participant':p, 'user': u }

        
class UserBadge(models.Model):
    user = models.ForeignKey(User)
    participant = models.ForeignKey(SurveyUser, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    badge = models.ForeignKey(Badge)
    
    objects = UserBadgeManager()