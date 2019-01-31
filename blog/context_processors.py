def entry_default(req):
    # this will prevent useless debug exceptions to be raised
    return {"author": None, "category": None, "tag": {"name": ""}}
