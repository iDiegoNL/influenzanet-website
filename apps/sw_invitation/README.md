Invitation management application
================================

This app handles a gaming-oriented invitation feature for platform's users 
A user can invite his friends, by sending them an email with an invitation link to register and a key useable to register without the link

Configuration
-------------

 * SW_INVITATION_TOKEN_LENGTH : size of the random part of the key generated for each user (default is 5) 
 * SW_INVITATION_TOKEN_PREFIX : Add a prefix to each key
 * SW_INVITATION_EMAIL_INVITATION : Path (relative to templates directory) of the template files for the email (at leat 2 files are excepted, [template_path].txt, [template_path]_subject.txt. One .html file could be provided to add an html-based part to the invitation email)
 * SW_INVITATION_SIGNAL_MODULE : module full qualified name to get the "user_registered" signal, for example "registration.signals"
 
Invitation follow-up
--------------------

2 way to follow invitations:

 * an invitation key was used for registration (told to the app using signal feature, see Signal handling)
 * a user registred using a invited email
  
Signal Handling
-----------------

The app catch a signal, "user_registered", from an account management application (django-registration for example)
If the account app handle the registration key, a parameter called "invitation_key" should be sended with the signal
