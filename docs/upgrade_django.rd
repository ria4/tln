* sqlite3, libsqlite3-0 & libsqlite3-tcl have been backported to debian 9 version because of django 2.0.9 bug
* once upgraded to django 2.1, restore the sqlite3 debian10-lts packages


pip install pip-review
pip review --local --interactive

pip uninstall -y `pip freeze`
pip install -r requirements.txt

makemigrations / migrate admin, auth, photologue

rm -rf critique/migrations/ ; ./manage.py makemigrations critique ; ./manage.py migrate critique
echo 'import sql_migrate' | ./manage.py shell

remove django<3 commands from zinnia & tagging



add PNG support
