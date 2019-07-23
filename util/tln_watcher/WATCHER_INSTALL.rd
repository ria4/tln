apt install mailutils ssmtp

remplacer /etc/ssmtp/ssmtp.conf

placer tln_watcher.sh où tu veux, puis chmod +x

ajouter au crontab */5 * * * * /...../tln_watcher.sh
