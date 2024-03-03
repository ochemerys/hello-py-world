# hello-py-world

Simple Python 3 containerized web application.

## Pred-Deployment

* Install Docker with Kubernetes.
* Instal Python 3 and set virtual environment. (optional)

## Run app in Docker container

1. To create docker image, run in project root folder:

``` bash
  docker build -t hello_world_app .
```

1. To run application in docker container:

``` bash
  docker run -p 8080:5000 hello_world_app
```

1. Open App in browser by navigating to <http://localhost:8080>

## Deploy app in Kubernetes pod with autoscaling

Note: To insure Kubernetes services are running:

``` bash
kubectl cluster-info
# output
# Kubernetes control plane is running at https://kubernetes.docker.internal:6443
```

``` bash
kubectl get services
# output:
# NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
# kubernetes   ClusterIP   X.X.X.X    <none>        443/TCP   6m11s
```

1. Create local Docker Registry (if not created): 
   To run a Docker Registry container locally by executing the following command:

``` bash
docker run -d -p 8888:5000 --name registry registry:2

```

1. To create docker image, run in project root folder:

``` bash
  docker build -t hello-world-app .
```

1. Tag local image with the registry address (localhost:8888):

``` bash
docker tag hello-world-app:latest localhost:8888/hello-world-app:latest
```

1. Push the tagged image to the local Docker Registry:

``` bash
docker push localhost:8888/hello-world-app:latest
```

1. Apply the Kubernetes deployment and autoscaler configurations:

``` bash
kubectl apply -f deployment.yaml
kubectl apply -f autoscaler.yaml
```

## Stop kubernetes service with autoscaling

### Identify and delete Horizontal Pod Autoscaler

To stop Kubernetes autoscaling for a particular service, you need to delete the HorizontalPodAutoscaler (HPA) resource associated with that service.

1. List HPAs: First, list all the HorizontalPodAutoscaler resources in your Kubernetes cluster to identify the one  you want to delete:

``` bash
kubectl get hpa
```

1. Delete HPA: Once you've identified the HPA you want to delete, use the following command to delete it:

``` bash
kubectl delete hpa {hpa-name}
```

Replace {hpa-name} with the name of the HPA you want to delete. This will stop autoscaling for the specified service.

### Identify and delete

To stop containers in Kubernetes, you typically delete the Deployment, that manages the pods containing those containers.

1. List Deployments: First, list all the Deployments in your Kubernetes cluster to identify the one you want to delete:

``` bash
kubectl get deployments
```

1. Delete Deployment: Once you've identified the Deployment you want to delete, use the following command to delete it:

``` bash
kubectl delete deployment {deployment-name}
```

Replace {deployment-name} with the name of the Deployment you want to delete.

