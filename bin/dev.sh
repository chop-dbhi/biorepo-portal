#!/bin/sh

python /opt/app/manage.py migrate --noinput
python /opt/app/manage.py collectstatic --noinput

if [ "$(ls -A /opt/app)" ]; then
    exec /usr/bin/uwsgi --chdir /opt/app/ --die-on-term --http-socket 0.0.0.0:8000 -p 2 -b 32768 -T --master --max-requests 5000 --static-map /static=/opt/app/_site/static --static-map /static=/usr/local/lib/python2.7/site-packages/django/contrib/admin/static --module brp.wsgi:application
fi