# The Biorepository Portal Project

[![CircleCI](https://circleci.com/gh/chop-dbhi/biorepo-portal/tree/master.svg?style=svg)](https://circleci.com/gh/chop-dbhi/biorepo-portal/tree/master)
[![ReadTheDocs](https://readthedocs.org/projects/biorepository-portal/badge/?version=latest)](http://biorepository-portal.readthedocs.io/en/latest/)

For more information and further documentation please see [here](http://biorepository-portal.readthedocs.io/en/latest/)


## Quickstart

#### Requirements

* [Docker](https://www.docker.com/)
* [Docker Compose](https://www.docker.com/products/docker-compose)

The Biorepository Portal contains a [docker-compose](https://www.docker.com/products/docker-compose) file which defines a `brp` service to quickly spin up a demonstration instance of the portal. This demo consists of the Portal itself, redis, as well as a companion instance of [electronic Honest Broker](https://github.com/chop-dbhi/ehb-service).

Run:

`docker-compose up brp`

Demonstration accounts for both the Portal and the eHB have a user name of `admin@email.chop.edu` and a password of `Chopchop1234` (case sensitive).

## Installation


#### Requirements

* Python >= 3.4

#### Recommended

* Postgres >= 9.4, < 10
* Redis >= 3.0.5

*To build front-end components*

* Node >= 5.4.0 [[instructions](https://nodejs.org/en/download/current/)]
* npm >= 3.3.12 (packaged with Node)

## Contributions

Please lint all code contributions using flake8 according to the `.flake8` configuration file found in the root of this repository.

Please write tests for contributions when applicable and run the included test suite before submitting a pull request.

### Testing

Install the required python packages. Best practice is to do this in a virtual environment, which must be using [Python 3](#install-python-3). A [PostgreSQL 9](#install-postgresql-9) `pg_config` binary must be available in your `PATH`.

```
pip install -r requirements.txt -r requirements-dev.txt
```

Create a local configuration file. This file assumes you have a [PostgreSQL 9](#install-postgresql-9) server running on port 5432 and a [Redis](#install-redis) server running on port 6379.

```
cp test.env_example test.env
```

Point the Django configuration at the test configuration file.

```
export APP_ENV=test
```

Run the unit tests.

```
./manage.py test
```

There should only be 5 failing tests, which all relate to LDAP integration.

## Helpful Hints

### Install Python 3

Install `pyenv` and `pyenv-virtualenv` (on macOS using Homebrew).

```
brew install pyenv pyenv-virtualenv
```

Initialize `pyenv`. You may (probably) want to add this line to your shell setup script.

```
eval "$(pyenv init -)"
```

Install Python 3.

```
pyenv install 3.6.5
```

Create a virtual environment.

```
pyenv virtualenv 3.6.5 biorepo-portal
```

Activate that virtual environment for the current directory.

```
pyenv local biorepo-portal
```


### Install PostgreSQL 9

For macOS, there is a handy application named [Postgres](https://postgresapp.com/) which does all the setup for you. It can be installed using Homebrew.

```
brew cask install postgres
```

When you first open the application, click the little icon on the bottom to expand a side-drawer that will allow you to add a database, since you don't want to use the default version 10 database you are offered. From there it is pretty easy to initialize and start a new version 9 database.

Use the following to make the PostgreSQL 9 binaries available in your PATH before, for example, installing the required `psycopg2` python package dependency. You may want to add this line to your shell setup script.

```
export PATH=/Applications/Postgres.app/Contents/Versions/9.6/bin:$PATH
```

### Install Redis

On macOS using Homebrew.

```
brew install redis
```

Start a Redis server.

```
redis-server /usr/local/etc/redis.conf
```
