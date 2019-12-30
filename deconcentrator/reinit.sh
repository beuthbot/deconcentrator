#! /bin/bash

bash down -v &&
bash up -d --scale=worker=3 &&
rm -vf deconcentrator/src/*/migrations/0*.py &&
bash management.sh exec uwsgi /mnt/deconcentrator/manage.py makemigrations &&
bash management.sh exec uwsgi /mnt/deconcentrator/manage.py migrate &&
bash management.sh exec uwsgi /mnt/deconcentrator/manage.py collectstatic --noinput &&
exec bash management.sh exec uwsgi /mnt/deconcentrator/manage.py createsuperuser


