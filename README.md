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

## Run MySQL in container

1. Pull the MySQL Docker Image:

``` bash
docker pull mysql:latest
```

2. Run the MySQL Container:

``` bash
docker run -d -e MYSQL_ROOT_PASSWORD=my-secret-password mysql:latest
# if existing MqSQL is already running on port 3306, switch to another port 3307
docker run -d -p 3307:3306 -e MYSQL_ROOT_PASSWORD=my-secret-password mysql:latest

docker ps -a
```

## Prepare MySQL database for application

1. Connect to MySQL:

``` bash
docker exec -it <container_id> mysql -u root -p
```

``` bash
mysql -u app_admin -p -h <hostname> -P 3306
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

