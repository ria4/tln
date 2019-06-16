import hashlib

from urllib.parse import urlparse, urlunparse
from django.http import QueryDict


def md5_2(s):
    h = hashlib.md5()
    h.update(s)
    h2 = hashlib.md5()
    h2.update(h.digest())
    return h2.digest()    

def remove_query_param(url, attr):
    (scheme, netloc, path, params, query, fragment) = urlparse(url)
    query_dict = QueryDict(query).copy()
    query_dict.pop(attr, None)
    query = query_dict.urlencode()
    return urlunparse((scheme, netloc, path, params, query, fragment))
