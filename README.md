# hello-py-world

Simple Python 3 containerized web application.

## Pred-Deployment

* Instal Python 3
* Install Docker

## Run app in Docker container

1. To create docker image, run in project root folder

``` bash
  docker build -t hello_world_app .
```

1. To run application in docker container:

``` bash
  docker run -p 8080:5000 hello_world_app
```

## Open App in browser

Navigate it browser to <http://localhost:8080>
