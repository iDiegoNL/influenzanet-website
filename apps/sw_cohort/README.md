Features 
==========

- Identify a group of participants
- A participant can register into a group using a token like a voucher-code to get a promotion

2 parts :

 * Cohorts (groups) :  defined by a title and a description (showed when the user want to register to the group).
 * Tokens : 1 to 30 characters, could be limited in number of usage or with an expiration date

- Tokens are pre-assigned to a cohort and, of course, must be unique
- A cohort could have as many as token as you want (everyone can have the same token or if your want a very secured registration, you can have only one token by participant).
- Privacy is (could be) preserved, at the end, you only know that a user is related to a cohort, but not which token was used.

In this version, a group is not defined by a query on participants data, but on the participant (voluntary) registration. 
The tokens must be delivered to the target participants by the team. 

Cohorts, Tokens can be managed in django admin site.

Installation
================

# in urls.py
urlpatterns += patterns('', 
    url(r'^cohort/', include('apps.sw_cohort.urls')),
)

# in settings.py

# add in INSTALLED_APPS = ( 
# ....    
	'apps.sw_cohort',
# ... )

# Then migrate
./python manage.py migrate

