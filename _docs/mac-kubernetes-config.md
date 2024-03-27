# Running Kubernetes Locally via Docker

On OS X, to make the API server accessible locally, setup a ssh tunnel.

``` bash
docker-machine ssh `docker-machine active` -N -L 8080:localhost:8080
```

(Optional) Create kubernetes cluster configuration:

``` bash
kubectl config set-cluster test-doc --server=http://localhost:8080
kubectl config set-context test-doc --cluster=test-doc
kubectl config use-context test-doc
```

## Test it out

List the nodes in your cluster by running:

``` bash
kubectl get nodes
# output
# NAME        STATUS    AGE
# 127.0.0.1   Ready     1h
```

## Run an application

``` bash
kubectl run nginx --image=nginx --port=80
```

Now run docker ps you should see nginx running. You may need to wait a few minutes for the image to get pulled.

## Expose it as a service

``` bush
kubectl expose deployment nginx --port=80
```

Run the following command to obtain the cluster local IP of this service we just created:

``` bush
ip=$(kubectl get svc nginx --template={{.spec.clusterIP}})
echo $ip
```

Hit the webserver with this IP:

``` bush
kubectl get svc nginx --template={{.spec.clusterIP}}
```

On OS X, since docker is running inside a VM, run the following command instead:

``` bash
docker-machine ssh `docker-machine active` curl $ip
```
