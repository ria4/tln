import hashlib

from urllib.parse import urlparse, urlunparse
from django.http import QueryDict


def md5_2(s):
    h = hashlib.md5()
    h.update(s)
    h2 = hashlib.md5()
    h2.update(h.digest())
    return h2.digest()    

def update_query_param(url, attr, val):
    (scheme, netloc, path, params, query, fragment) = urlparse(url)
    query_dict = QueryDict(query).copy()
    query_dict[attr] = val
    query = query_dict.urlencode(safe="/")
    return urlunparse((scheme, netloc, path, params, query, fragment))

def remove_query_param(url, attr):
    (scheme, netloc, path, params, query, fragment) = urlparse(url)
    query_dict = QueryDict(query).copy()
    query_dict.pop(attr, None)
    query = query_dict.urlencode(safe="/")
    return urlunparse((scheme, netloc, path, params, query, fragment))
