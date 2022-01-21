## Cleaning

* no robots on tmp directory
* namespace urls in views & templates
* override default admin interfaces to remove useless content
* add `__str__` methods to models
* use `require_safe` on appropriate views

## CSS tweaks

* equalize ul left padding between ff & chrome
* also equalize line-heights
    - navigation sidebar
    - galleries description (inside p or not)
        - #gallery-description font-size may be useless
* check on sidebar bullets size on mobile


## Features

* override oeuvre `save`-ing to refresh cache
* add `date_from` & `date_to` to oeuvres
* more concise title alt & imdb id & tags
* display music by tag (ambient, electronic, now...)
* focus to first form field after critique admin code


## Stability

* ansible deployment (maybe)
* write tests (mayyybe)
