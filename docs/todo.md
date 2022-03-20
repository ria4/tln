## Cleaning

* namespace urls in views & templates
* add `__str__` methods to models


## CSS tweaks

* equalize ul left padding between ff & chrome
* also equalize line-heights
    - navigation sidebar
    - galleries description (inside p or not)
        - #gallery-description font-size may be useless
* check on sidebar bullets size on mobile


## Features

* override oeuvre `save`-ing to refresh cache
* more concise title alt & imdb id & tags
* display music by tag (ambient, electronic, now...)
* focus to first form field after critique admin code


## Long term

* call asqip asynchronously
* rework critique models (`date_from`, `date_to`...)
* rewrite critique with class-based views
* migrate from zinnia to another cms
* override default admin interfaces to remove useless content


## Stability

* ansible deployment (maybe)
* write tests (mayyybe)
