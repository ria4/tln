## Cleaning

* namespace urls in views & templates
* use `path` instead of `url`
* override default admin interfaces to remove useless content
* add `__str__` methods to models
* use `require_safe` on appropriate views
* reroute non-trailing urls in upm59 mirror


## Features

* override oeuvre `save`-ing to refresh cache
* add `date_from` & `date_to` to oeuvres
* display music by tag (ambient, electronic, now...)


## Tests

* write tests (maybe)
