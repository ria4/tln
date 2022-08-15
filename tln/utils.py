"""
Various helpers
"""


def qs_update_param(req, query_param, val):
    """
    Given an HttpRequest, replace any 'query_param' parameter
    in the query string (if present) with a unique value 'val'.
    """
    query_dict = req.GET.copy()
    try:
        query_dict.pop(query_param)
    except KeyError:
        pass
    query_dict.setdefault(query_param, val)
    return query_dict.urlencode(safe="/")


def qs_update_loginfail(req, val):
    return qs_update_param(req, "loginfail", val)
