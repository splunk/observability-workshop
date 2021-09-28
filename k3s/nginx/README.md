Set up configmap and pods
 1. Create configmap

     ```kubectl create configmap nginxconfig --from-file=./nginx.conf```

 2. Ensure configmap is created

    ```kubectl get cm```

 3. Create deployment

    ```kubectl apply -f ./nginx-deployment.yaml```

 4. Ensure pods are created and running

    ```kubectl get pods --watch```
    

 You have completed the initial setup. Next, continue with [Observability Workshop](https://signalfx.github.io/observability-workshop).
