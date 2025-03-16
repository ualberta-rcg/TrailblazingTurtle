FROM ubuntu:24.04

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y tzdata && apt install -y python3.12 python3-pip python3-dev python3.12-venv libpq-dev nginx libmysqlclient-dev pkg-config build-essential git libsasl2-dev libldap2-dev libssl-dev gettext wget

WORKDIR /opt/userportal

COPY requirements.txt ./

RUN python3 -m venv /opt/userportal-env && \
    /opt/userportal-env/bin/pip install --upgrade pip && \
    /opt/userportal-env/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

RUN patch /opt/userportal-env/lib/python3.12/site-packages/ldapdb/backends/ldap/base.py < /opt/userportal/ldapdb.patch

# Temporarily remove db version check to support mariadb server on EL8 without appstream enabled
RUN patch /opt/userportal-env/lib/python3.12/site-packages/django/db/backends/base/base.py < /opt/userportal/dbcheck.patch

RUN /opt/userportal-env/bin/python manage.py collectstatic --noinput && /opt/userportal-env/bin/python manage.py compilemessages

RUN cd /opt && wget http://www.w3.org/TR/xmlenc-core1/xenc-schema-11.xsd

RUN apt install -y automake autoconf libtool libtool-bin gcc libltdl7 libltdl-dev libxml2 libxml2-dev libxslt1.1 libxslt1-dev openssl libssl3 libssl-dev libnspr4 libnspr4-dev libnss3 libnss3-dev libnss3-tools libgnutls30 libgcrypt20 libgcrypt20-dev help2man man2html gtk-doc-tools && cd /opt && git clone https://github.com/lsh123/xmlsec.git && cd xmlsec && ./autogen.sh && make && make install && apt remove -y automake autoconf libtool libtool-bin gcc libltdl-dev libxml2-dev libxslt1-dev libssl-dev libnspr4-dev libnss3-dev libgcrypt20-dev help2man man2html gtk-doc-tools build-essential git && apt autoremove -y && apt install -y mariadb-client sssd && apt clean

EXPOSE 8000
CMD ["./run-django-production.sh"]
