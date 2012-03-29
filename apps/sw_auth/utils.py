
from django.utils.http import int_to_base36, base36_to_int
from datetime import date
from random import choice
             
def get_timestamp():
    (date.today() - date(2001,1,1)).days()

def random_string(length, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'):
    return ''.join([choice(allowed_chars) for i in range(length)])

def create_token():
    timestamp = get_timestamp()
    ts36 = int_to_base36(timestamp)
    token = random_string(32)
    token += '-' + ts36
    return token

def get_token_age(token):
    ts36,r = token.split("-")
    timestamp = base36_to_int(ts36)
    now = get_timestamp()
    return now - timestamp