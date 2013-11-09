from datetime import date 
from django.conf import settings

# Number of the month to use as the first month of each season
# Before is the previous season
# A season is defined by the year of the first month of the project launching
SEASON_STARTING_MONTH = 11

def historical_table(year, name):
    
    try:
        HISTORICAL_TABLES = settings.HISTORICAL_TABLES
    except AttributeError:
        raise Exception("HISTORICAL_TABLES should be configured")
    
    try:
        tables = HISTORICAL_TABLES[str(year)]
        return tables[name]
    except:
        raise Exception("historical table '%s' is not defined for the season %d" % (name, year,))


def get_current_season():
    today = date.today()
    if today.month >= SEASON_STARTING_MONTH:
        return today.year
    else:
        return today.year - 1
