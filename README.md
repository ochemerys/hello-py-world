# hello-py-world

Simple Python 3 containerized web application.

## Pred-Deployment

* Instal Python 3
* Install Docker

## Run app in Docker container

1. To create docker image, run in project root folder

``` bash
  docker build -t hello-world-app .
```

2. To run application in docker container:

``` bash
  docker run -p 8080:5000 hello-world-app
```

3. Open App in browser

Navigate it browser to <http://localhost:8080>

## Run MySQL as Azure MySQL Flexible Service


## Prepare MySQL database for application

1. Connect to MySQL:

``` bash
mysql -u <username> -p -h <hostname> -P 3306
```

2. Execute in MySQL terminal to create database and table:

``` sql
-- create database
create database hello_world_db;
show databases;

-- create table in new database
use hello_world_db;

CREATE TABLE files (
  id INT AUTO_INCREMENT PRIMARY KEY,
  filename VARCHAR(255),
  path VARCHAR(255)
);

show tables;

quit
```

