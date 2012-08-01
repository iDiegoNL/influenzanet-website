from django.core.management.base import NoArgsCommand

from ...crypto import AES256
from ...utils import random_string
from base64 import b64decode, b64encode
from django.conf import settings

class Command(NoArgsCommand):
    
    def cipher(self,aes, txt):
        
        ctxt = aes.encrypt(txt)
        print "text  : %s" % txt
        print "cipher: %s (%d)" % (ctxt, len(ctxt))
        
        txt2 = aes.decrypt(ctxt)
        print "res   : %s" % txt2
        if txt == txt2:
            print '=== OK ====' 
            return 1
        return 0
    
    def handle_noargs(self, **options):
        
        key = settings.SWAUTH_AES_KEY
        
        aes = AES256(key)
        
        N = 10000
        ok = 0
        for i in range(N):
            txt = random_string(30)
            ok += self.cipher(aes, txt)
        
        print "OK = " + str(ok)