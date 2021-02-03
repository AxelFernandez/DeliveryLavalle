release: python manage.py migrate --run-syncdb --settings=deliveryLavalle_site.settings.qa
web: gunicorn deliveryLavalle_site.wsgi --log-file -