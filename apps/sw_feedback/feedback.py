
from urllib2 import urlopen, HTTPError
import json  
def feeback_token(site):
    url = "https://websenti.u707.jussieu.fr/feedback/?action=token&site=%s&version=0.1" % site
    try:
        r = urlopen(url)
        result = r.read()
        if r.getcode() == 202:
            result = json.loads(result)
            return result
    except HTTPError, e:
        print url
        print e
    return None
    
    
    