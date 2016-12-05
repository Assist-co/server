rm db.sqlite3
python manage.py migrate
python manage.py loaddata seed.json
python manage.py runserver
