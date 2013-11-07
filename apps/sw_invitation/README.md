Invitation management application
================================

This app handles a gaming-oriented invitation feature for platform's users 
A user can invite his friends, by sending them an email with an invitation link to register 
and a key useable to register without the link.

Configuration
-------------
All config vars are in settings.py in the app, you can config them in global settings.py 
 
Invitation follow-up
--------------------

2 way to follow invitations:

 * an invitation key was used for registration (told to the app using signal feature, see Signal handling)
 * a user registred using a invited email

InvitationUsage log each invitation success (usable for gaming)
Invitation, also have a field "used", set to True when a user registred with an invited email (indeed, if the invited user
use a link, and does not register with the same email, this is not catched in this table).

Privacy Choices
---------------
It has been chosen to trace the number of success, rather than to trace the invitation itself.
The success logged is only related to the user who invited people, not on which email registered nor on the account
of the invited user.
Invited email could be removed at any time (delay depends on country, regulation authority agreements,...) 
  
Signal Handling
-----------------

The app catch a signal, "user_registered", from an account management application (django-registration for example)
If the account app handle the registration key, a parameter called "invitation_key" should be sended with the signal
