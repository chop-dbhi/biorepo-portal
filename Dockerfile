FROM alpine:3.3

RUN apk add --update \
    bash \
    postgresql-dev \
    gcc \
    python3 \
    python3-dev \
    build-base \
    git \
    openldap-dev \
    linux-headers \
    pcre-dev \
    musl-dev \
    postgresql-dev \
    mailcap \
    vim \
  && rm -rf /var/cache/apk/* && \
  python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    rm -r /root/.cache &&\
    apk upgrade

RUN pip3 install "Django>=1.9.6,<1.10"
RUN pip3 install "django-environ>=0.4.0,<0.5"
RUN pip3 install "django-markdown-deux>=1.0.5,<1.1"
RUN pip3 install "django-session-security>=2.3.2,<2.4"
RUN pip3 install "django_redis>=4.4.3,<4.5"
RUN pip3 install "djangorestframework>=3.3.3,<3.4"
RUN pip3 install "djangorestframework-jwt>=1.5.0,<1.6"
RUN pip3 install "git+https://github.com/chop-dbhi/ehb-client.git@v2.0.3-alpha#egg=ehb_client"
RUN pip3 install "git+https://github.com/chop-dbhi/ehb-datasources.git@d38c2ae36df471bfd26d055efd073af3ea58cac7#egg=ehb_datasources"
RUN pip3 install "ldap3>=1.4.0,<1.5"
RUN pip3 install "gunicorn>=19,<20"
RUN pip3 install "psycopg2-binary"
RUN pip3 install "dj-static>=0.0.6,<0.1.0"
RUN pip3 install "python-json-logger==0.1.7"
RUN pip3 install "django-admin-tools"
RUN pip3 install "django-crispy-forms"
RUN pip3 install "requests"


ENV APP_ENV test
ADD . /opt/app/
ADD test.env_example /opt/app/test.env

CMD ["/opt/app/bin/run.sh"]

EXPOSE 8000
