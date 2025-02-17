#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

cp /secrets/settings/99-local.py /opt/userportal/userportal/settings/99-local.py
mkdir -p /var/www/api/static
cp -r /opt/userportal/collected-static/* /var/www/api/static/
#REMOTE_USER=alikarim@alliancecan.ca affiliation=staff@alliancecan.ca /opt/userportal-env/bin/gunicorn --bind :8000 --workers $WORKERS --threads $THREADS --timeout 90 userportal.wsgi
/usr/sbin/sssd -i --logger=files &
REMOTE_USER=alikarim@alliancecan.ca affiliation=staff@alliancecan.ca /opt/userportal-env/bin/python /opt/userportal/manage.py runserver 0.0.0.0:8000
