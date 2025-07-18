## `crontab -e`

```
@reboot /usr/local/bin/uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data --daemonize /home/ria/tln/net/uwsgi-emperor.log
@reboot . /home/ria/.bash_secrets; /home/ria/.virtualenvs/lajujabot/bin/python /opt/lajujabot/main.py -c /opt/lajujabot/config.json
@reboot mkdir /tmp/oeuvres_img && chmod 755 /tmp/oeuvres_img
0 4 * * * wget --spider https://oriane.ink/critique/rencontres/ 2>/dev/null
*/30 * * * * /home/ria/.virtualenvs/dyndns_ovh-jcypVYJ1/bin/python3 /opt/dyndns_ovh/dyndns_ovh.py
```


## `sudo crontab -e`

```
0 3 * * * rsync -az --delete-after /home/ria/tln backup:/data/oriane_bak
0 3 * * * rsync -az --delete-after /opt/lajujabot backup:/data/oriane_bak
0 4 * * 1 rsync -az /home/ria/.bashrc backup:/data/oriane_bak/configs
0 4 * * 1 rsync -az /home/ria/.bash_aliases backup:/data/oriane_bak/configs
0 4 * * 1 rsync -az /home/ria/.bash_secrets backup:/data/oriane_bak/configs
0 4 * * 1 rsync -az /etc/ssh/ssh_config backup:/data/oriane_bak/configs
0 4 * * 1 rsync -az /etc/vim/vimrc backup:/data/oriane_bak/configs
```
