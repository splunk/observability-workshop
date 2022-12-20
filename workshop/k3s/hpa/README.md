# HPA

## Deploy PHP/Apache

```
kubectl apply -f php-apache.yaml
```

## Setup HPA

Create an autoscaling deployment for CPU

```
kubectl autoscale deployment php-apache --cpu-percent=80 --min=1 --max=4
```

## Create infinite-calls pod

```
kubectl apply -f infinite-calls.yaml
```

## Scale infinite-calls

```
kubectl scale deployment/infinite-calls --replicas 4
```

## Stop the load test

```
kubectl delete -f infinite-calls.yaml
```

