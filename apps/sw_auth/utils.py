
from django.utils.http import int_to_base36
from datetime import date
from random import choice
    
allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'    
         
def get_timestamp():
    (date.today() - date(2001,1,1)).days()
    
def create_token():
    timestamp = get_timestamp()
    ts36 = int_to_base36(timestamp)
    token = ''.join([choice(allowed_chars) for i in range(32)])
    token += '-' + ts36
    return token



def parse_token(token):
    try:
        ts_b36, hash = token.split("-")
    except ValueError:
      return False