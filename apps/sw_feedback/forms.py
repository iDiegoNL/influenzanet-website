
from django.forms import Form, CharField,EmailField, ValidationError
from random import randint, choice

def create_captcha_value():
    v1 = randint(0, 9)
    v2 = randint(0, 9)
    op = choice(('+','-', '*'))
    value = {
     '+': lambda a,b: a+b,
     '-': lambda a,b: a-b,
     '*': lambda a,b: a*b
    }[op](v1,v2)
    label = '%d %s %d' % (v1,op,v2)
    print '%s = %d' % (label, value)
    return (label, value)

class CaptchaField(CharField):
    
    def __init__(self):
        self.to_check = None
        CharField.__init__(self, required=True)
    
    def newValue(self):
        cc = create_captcha_value()
        self.label = cc[0]
        return cc[1]
    def setValue(self, value):
        self.to_check = value
    
    def validate(self, value):
        CharField.validate(self, value)
        if(self.to_check is not None):
            print '%s vs %s' % (self.to_check, value)
            if(not self.to_check == value):
                raise ValidationError("Invalid captcha value")
            
class TellAFriendForm(Form):
    email = EmailField(required=True)
    subject = CharField(max_length=100)
    message = CharField()
    captcha = CaptchaField()

    def updateCaptcha(self):
        return self.fields['captcha'].newValue()    
    
    def initCaptcha(self, value):
        self.fields['captcha'].setValue(value)
    