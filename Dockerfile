FROM python:3.8
RUN apt-get update \
 && apt-get install wget

RUN echo ls opt

RUN apt-get -y install \
    bash \
#    postgresql-dev \
    gcc \
#    python3 \
#    python3-dev \
#    build-base \
    git \
#    openldap-dev \
#    linux-headers \
#    pcre-dev \
    musl-dev \
#    postgresql-dev \
#    mailcap \
    vim
#  && rm -rf /var/cache/apk/* && \
#  python3 -m ensurepip && \
#    rm -r /usr/lib/python*/ensurepip &&

RUN pip install --upgrade pip setuptools && \
    rm -r /root/.cache
#    apk upgrade
RUN pwd
RUN ls opt
RUN ls
RUN mkdir -p /opt/app

#RUN mkdir -p /opt/app/
# COPY requirements.txt /opt/app/

COPY . /opt/app/
#RUN pip3 install -r /opt/app/requirements.txt
RUN pip install -r /opt/app/requirements.txt

ENV APP_ENV test
ADD . /opt/app/
ADD test.env_example /opt/app/test.env

CMD ["/opt/app/bin/run.sh"]

EXPOSE 8000
