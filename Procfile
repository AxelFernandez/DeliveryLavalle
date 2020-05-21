release: python manage.py migrate --run-syncdb --settings=deliveryLavalle_site.settings.production
web: gunicorn Ahorcadov2.wsgi --log-file -