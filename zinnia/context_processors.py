"""Context Processors for Zinnia"""
from zinnia import __version__


def version(request):
    """
    Add version of Zinnia to the context.
    """
    return {'ZINNIA_VERSION': __version__}


def entry_default(req):
    # this will prevent useless debug exceptions to be raised
    return {"author": None, "category": None, "tag": {"name": ""}}
