from Crypto.Cipher import AES
from os import urandom
from base64 import b64encode, b64decode
import struct

"""
AES-256 Cipher Algorithm using pyCrypto lib
Handle PKCS7 padding and initialization vector

Key should be a  base64 encoded 32 bytes string (256bits)

"""

class AES256:
    
    """
        key base64 encoded key (32 bytes/256 bits)
    """
    def __init__(self, key, mode=AES.MODE_CBC):
        self.block_size = 16
        self.key_size = 32
        self.key = b64decode(key)
        self.mode = mode
        self.debug = False

    """
     Encrypt a plain text 
     returns a base64 encoded ciphered structure :
       base64([size][IV][encrypted text])
       Size is long integer (8 bytes)
       IV initialization vector (16 bytes)
       text 
    """
    def encrypt(self, txt):
        # Remaining lenth to pad
        to_pad_len = (self.block_size - len(txt)) % self.block_size
        # Original length
        org_len = len(txt)
        txt = txt + chr(to_pad_len)*to_pad_len # PKCS7 padding
        # Initial vector
        iv = urandom(self.block_size)
        if self.debug:
            print "block: %d len:%d pad:%d "  % (self.block_size, org_len, to_pad_len) 
            print 'iv: ' + b64encode(iv)
            print 'txt : '+ txt
            
        aes = AES.new(self.key, self.mode, iv)
        ctxt = aes.encrypt(txt)
        # Cypher = length + IV + ciphered text in base64
        cypher = struct.pack('<Q', org_len) + iv + ctxt
        return b64encode(cypher)  
    """
     Decrypt a text
    """
    def decrypt(self, ctxt):
        ctxt = b64decode(ctxt)
        # n = size of long integer
        n = struct.calcsize('Q')
        # get the size of the original text
        size = struct.unpack('<Q', ctxt[0:n])[0]
        # get the initializing vector
        iv = ctxt[n:(n+16)]
        if self.debug:
            print "long %d o len: %d" % (n, size,)
            print 'iv: ' + b64encode(iv)
        # ciphered text
        ctxt = ctxt[(n+16): ]
        aes = AES.new(self.key, self.mode, iv)
        txt = aes.decrypt(ctxt)
        # avoid padding in resulting text
        return txt[0:size]
        