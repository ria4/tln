## Features tln

- reduce main nav size on small screens


## Features critique

- reduce detail oeuvre size on narrow screens
- autocomplete + create for artists & tags
- list tags on oeuvre detail
- link to all cinemas on cinema detail
- navlink to all cinemas? to all tags?


## Features photos

- move logout link to 'tools' (see blog sidebar)


## Features todo

- focus on id_content/id_title for new item/list
- display /now link
- add list order, removed_at, last_updated_at
- add item order, removed_at
- display links to public lists from same author
- handle /todo page for unauthenticated users


## Features lajujabot

- handle ChatMigrated error
- handle unexpected reboots and reconnect errors


## Long term

- use ajax and icons with todo app
- migrate from zinnia to another cms
- logout with POST rather than GET
- bump to django 4.1
    - switch to redis cache
    - update critique collection asynchronously
    - cache much more pages


## Barely matters

- refactor critique views with CBVs or DRF
- override admin interfaces to remove useless content
- call sqip asynchronously
- ansible deployment (maybe)
