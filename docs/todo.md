## Cleaning

- detail oeuvre size on narrow screens


## CSS tweaks

- all done!


## Features critique

- autocomplete + create for artists & tags
- list tags on oeuvre detail
- link to all cinemas on cinema detail
- navlink to all cinemas? to all tags?
- link /now to a list of my public lists


## Features todo

- models
    - add list last_updated_at
    - add list removed_at
    - add item removed_at
- item add view
    - no list select dropdown
    - pre-populate list id
- list detail
    - display public lists
    - show account name if not author
- rework html tags in templates
- style up views


## Long term

- migrate from zinnia to another cms
- bump to django 4.0
    - switch to redis cache
    - update critique collection asynchronously
    - cache much more pages


## Barely matters

- refactor critique views with CBVs or DRF
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
