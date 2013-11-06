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
```
urlpatterns += patterns('', 
    url(r'^cohort/', include('apps.sw_cohort.urls')),
)
```

in settings.py
 add 'apps.sw_cohort' in INSTALLED_APPS 

# Then migrate

```python
./python manage.py migrate
```

App integration with Participant management
============
The app provide an ajax service returning cohort registrations for all participants of 
the current user (django account).
It returns
 - subscribers = a list of cohort (id) for each participant (here indexed by their SurveyUser.id, @TODO use global_id instead)
 - cohorts = list of cohorts title (key is the cohort id, used in subscribers)

```js	
$.getJSON('/cohort/subscriptions', function(data) {
	var subscribers = data.subscribers;
	var cohorts = data.cohorts;
	if(subscribers) {
		# console.log(subscribers);
		for(var uid in subscribers) {
			var subs = subscribers[uid];
			title = '{%trans "Subscriptions for this user:"%}<br/>';
			for(var i=0; i < subs.length; ++i) {
				var c = subs[i];
				title += cohorts[c]+'<br/>';
			}
			// 
			$('#cohort-'+uid).attr('title',title).addClass("icon icon-cohort").tooltip();
		}
	}
});
```	
	
 

