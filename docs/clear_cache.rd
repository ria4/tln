Les chunks cinemas et seances (pour les années avant 2022) sont mis en cache indéfiniment.
Les modifs dans la base de données ne seront donc pas directement répercutées sur le site.
Il faut d'abord vider le cache (avec la commande custom) :

$ vtln
$ ./manage.py clearcache

Ou bien utiliser directement l'alias bash :

$ recache

Un nouveau cache sera créé au prochain chargement des pages concernées.
