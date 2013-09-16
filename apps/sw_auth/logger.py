"""
Simple Logger for authentication events
"""

from django.utils.log import getLogger

"""
 Notifiy an event with a msg
"""
def auth_notify(event, msg):
    logger = getLogger('swauth_notify')
    logger.info(event + ':' + msg)