## Cleaning

- enforce one-line oeuvrespan when len < 30 (?)
- select mtype on loading oeuvre empty form
- delete tag if count=0 after oeuvre deletion
- detail oeuvre size on narrow screens


## Todo app

- models
    - remove item description
    - add list last_updated_at
- item add view
    - no list select dropdown
    - no description field
    - pre-populate list id
- list detail
    - display public lists
    - show account name if not author
- rework html tags in templates
- style up views


## CSS tweaks

- all done!


## Features

- autocomplete + create for artists & tags
- list tags on oeuvre detail
- link to all cinemas on cinema detail
- navlink to all cinemas? to all tags?
- link /now to a list of my public lists


## Long term

- migrate from zinnia to another cms
- bump to django 4.0
    - switch to redis cache
    - update critique collection asynchronously
    - cache much more pages
- refactor critique views with CBVs or DRF


## Barely matters

- override admin interfaces to remove useless content
- call sqip asynchronously
- ansible deployment (maybe)


## Miscellaneous

- add links to bitwarden base
- cold-store bitwarden base & clean up keepass
- article updates v3
- article dataviz seances, cinemas, words
- sync dotfiles
- import this list into todo app
