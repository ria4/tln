import hashlib


def md5_2(s):
    h = hashlib.md5()
    h.update(s)
    h2 = hashlib.md5()
    h2.update(h.digest())
    return h2.digest()    
