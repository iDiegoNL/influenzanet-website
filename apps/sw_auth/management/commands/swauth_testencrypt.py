from django.core.management.base import NoArgsCommand

from ...utils import random_string, encrypt_user, decrypt_user

class Command(NoArgsCommand):
    
    def cipher(self,txt):
        ctxt = encrypt_user(txt)
        print "text  : %s" % txt
        print "cipher: %s (%d)" % (ctxt, len(ctxt))
        
        txt2 = decrypt_user(ctxt)
        print "res   : %s" % txt2
        if txt == txt2:
            print '=== OK ====' 
            return 1
        return 0
    
    def handle_noargs(self, **options): 
        N = 10000
        ok = 0
        for i in range(N):
            txt = random_string(30)
            ok += self.cipher(txt)
        
        print "OK = " + str(ok)