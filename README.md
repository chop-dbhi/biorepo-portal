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

* Python 2.7+

#### Recommended

* Postgres 9.4+
* Redis 3.0.5+

*To build front-end components*

* Node 5.4.0+ [[instructions](https://nodejs.org/en/download/current/)]
* npm 3.3.12+ (packaged with Node)

*To Enable Logstash integration*

* `pip install python-logstash`

```bash
# Retrieve source code
git clone https://github.com/chop-dbhi/biorepo-portal.git
cd biorepo-portal
# Retrieve javascript dependencies
npm install
# Build bundle
npm run build

```

## Configuration

What follows is a step by step walkthrough describing the configuration of a Protocol for data entry in the Biorepository Portal.

In this walkthrough our example study will have two datasources (Nautilus LIMs and REDCap).

#### Defining Datasources

#### Defining Organizations

#### Defining a Protocol

#### Creating Protocol Datasource


## Contributions

Please lint all code contributions using flake8 according to the `.flake8` configuration file found in the root of this repository.

Please write tests for contributions when applicable and run the included test suite before submitting a pull request.

Tests can be run with the following command: `./manage.py test`
