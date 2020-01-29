## Archivage du site

* Site hébergé sur tln
* Rsync quotidien (code + media + db) sur minuscheri
* Code sur https://github.com/ria4/tln et sur miroirs
* Archive complète ponctuelle sur miroirs

#### Crontab tln

```
@reboot /usr/local/bin/uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data --daemonize /home/ria/tln/net/uwsgi-emperor.log
```

#### Crontab tln (sudo)

```
0 3 * * * rsync -az --delete-after /home/ria/tln -e "ssh -p 1992" root@minuscheri.com:/home/DATA/oriane_bak
```


## Archivage des photos

* Sur miroirs : conserver les dossiers courants et les photos des galeries
* Sur tln : importer les photos des galeries via l'interface web
* Sur minuscheri : tout copier
* Sur disque 42 : tout copier


## Marquage Darktable

* Label rouge : fichier corrompu 
* Label jaune : photo parue dans une galerie privée
* Label vert : photo parue dans une galerie publique
* Label bleu : light painting
* Label fuschia : élément pour composition HDR
