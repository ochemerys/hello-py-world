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

1. Create account in Docker Registry (if not created)

2. To create docker image, run in project root folder:

``` bash
  docker build -t hello-world-app .
```

3. Tag local image with the registry address:

``` bash
docker tag hello-world-app:latest {accountname}/hello-world-app:latest
```

Replace {accountname} with the name of the Deployment you want to delete.

4. Push the tagged image to the local Docker Registry:

``` bash
docker push {accountname}/hello-world-app:latest
```

Replace {accountname} with the name of the Deployment you want to delete.

5. Apply the Kubernetes deployment and autoscaler configurations:

``` bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f autoscaler.yaml
```

6. Verify deployments

``` bash
kubectl get deployments
# output
# NAME          READY   UP-TO-DATE   AVAILABLE   AGE
# hello-world   1/1     1            1           10m
```

7. Verify services

``` bash
kubectl get services
# output
# NAME                  TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
# hello-world-service   NodePort    10.110.130.229   <none>        8080:31036/TCP   11m
# kubernetes            ClusterIP   10.96.0.1        <none>        443/TCP          28m
```

8. Verify autoscaling

``` bash
kubectl get hpa
# output
# NAME                     REFERENCE                TARGETS         MINPODS   MAXPODS   REPLICAS   AGE
# hello-world-autoscaler   Deployment/hello-world   <unknown>/50%   2         5         0          25s
```

## Stop kubernetes service with autoscaling

### Identify and delete Horizontal Pod Autoscaler

To stop Kubernetes autoscaling for a particular service, you need to delete the HorizontalPodAutoscaler (HPA) resource associated with that service.

1. List HPAs: First, list all the HorizontalPodAutoscaler resources in your Kubernetes cluster to identify the one  you want to delete:

``` bash
kubectl get hpa
```

2. Delete HPA: Once you've identified the HPA you want to delete, use the following command to delete it:

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

2. Delete Deployment: Once you've identified the Deployment you want to delete, use the following command to delete it:

``` bash
kubectl delete deployment {deployment-name}
```

Replace {deployment-name} with the name of the Deployment you want to delete.
