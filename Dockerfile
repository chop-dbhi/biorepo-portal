FROM python:3.8
RUN apt-get update \
 && apt-get install wget

RUN echo ls opt

RUN apt-get -y install \
    bash \
    gcc \
    git \
    musl-dev \
    vim

RUN pip install --upgrade pip setuptools && \
    rm -r /root/.cache
RUN pwd
RUN ls opt
RUN ls
RUN mkdir -p /opt/app

COPY . /opt/app/
RUN pip install -r /opt/app/requirements.txt

ENV APP_ENV test
ADD . /opt/app/
ADD test.env_example /opt/app/test.env

CMD ["/opt/app/bin/run.sh"]

EXPOSE 8000
