#! /bin/bash

bash down -v &&
bash prepare &&
find deconcentrator -type d -name migrations -exec find '{}' -type f -print0 \; | xargs -0 rm -v 
find deconcentrator -type d -name migrations -print0 | xargs -0 git checkout -- 
bash up --build -d --scale=worker=3 &&
bash management.sh exec uwsgi /mnt/deconcentrator/manage.py makemigrations &&
bash management.sh exec uwsgi /mnt/deconcentrator/manage.py migrate &&
bash management.sh exec uwsgi /mnt/deconcentrator/manage.py collectstatic --noinput &&
exec bash management.sh exec uwsgi /mnt/deconcentrator/manage.py createsuperuser


