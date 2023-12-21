---
title: Code to Kubernetes - Python
linkTitle: 3. Code to Kubernetes
weight: 3
---

## Code to Kubernetes - Python

**Objective:** Understand activities to instrument a python application and run it on Kubernetes.

- Verify the code
- Containerize the app
- Deploy the container in Kubernetes

**Note:** these steps do not involve Splunk

**Duration:** 15 Minutes

## 1. Verify the code - Review service

Navigate to the review directory

``` bash
cd /home/ubuntu/realtime_enrichment/flask_apps/review/
```

Inspect review.py (realtime_enrichment/flask_apps/review)

``` bash
cat review.py
```

``` python
from flask import Flask, jsonify
import random
import subprocess

review = Flask(__name__)
num_reviews = 8635403
num_reviews = 100000
reviews_file = '/var/appdata/yelp_academic_dataset_review.json'

@review.route('/')
def hello_world():
    return jsonify(message='Hello, you want to hit /get_review. We have ' + str(num_reviews) + ' reviews!')

@review.route('/get_review')
def get_review():
    random_review_int = str(random.randint(1,num_reviews))
    line_num = random_review_int + 'q;d'
    command = ["sed", line_num, reviews_file] # sed "7997242q;d" <file>
    random_review = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    return random_review.stdout

if __name__ == "__main__":
    review.run(host ='0.0.0.0', port = 5000, debug = True)
```

Inspect requirements.txt

``` text
Flask==2.0.2
```

Create a virtual environment and Install the necessary python packages

``` bash
cd /home/ubuntu/realtime_enrichment/workshop/flask_apps_start/review/

pip freeze #note output
pip install -r requirements.txt
pip freeze #note output
```

Start the REVIEW service. **Note:** You can stop the app with control+C

``` bash
python3 review.py

 * Serving Flask app 'review' (lazy loading)
 * Environment: production
         ...snip...
 * Running on http://10.160.145.246:5000/ (Press CTRL+C to quit)
 * Restarting with stat
127.0.0.1 - - [17/May/2022 22:46:38] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [17/May/2022 22:47:02] "GET /get_review HTTP/1.1" 200 -
127.0.0.1 - - [17/May/2022 22:47:58] "GET /get_review HTTP/1.1" 200 -
```

Verify that the service is working

- Open a new terminal and ssh into your ec2 instance. Then use the curl command in your terminal.

``` bash
curl http://localhost:5000
```

- Or hit the URL `http://{Your_EC2_IP_address}:5000` and `http://{Your_EC2_IP_address}:5000/get_review` with a browser

``` bash
curl localhost:5000
{
  "message": "Hello, you want to hit /get_review. We have 100000 reviews!"
}

curl localhost:5000/get_review
{"review_id":"NjbiESXotcEdsyTc4EM3fg","user_id":"PR9LAM19rCM_HQiEm5OP5w","business_id":"UAtX7xmIfdd1W2Pebf6NWg","stars":3.0,"useful":0,"funny":0,"cool":0,"text":"-If you're into cheap beer (pitcher of bud-light for $7) decent wings and a good time, this is the place for you. Its generally very packed after work hours and weekends. Don't expect cocktails. \n\n-You run into a lot of sketchy characters here sometimes but for the most part if you're chilling with friends its not that bad. \n\n-Friendly bouncer and bartenders.","date":"2016-04-12 20:23:24"}
```

{{% notice title="Workshop Question" style="tip" icon="question" %}}

- What does this application do?
- Do you see the yelp dataset being used?
- Why did the output of pip freeze differ each time you ran it?
- Which port is the REVIEW app listening on? Can other python apps use this same port?

{{% /notice %}}

## 2. Create a REVIEW container

To create a container image, you need to create a Dockerfile, run docker build to build the image referencing the Docker file and push it up to a remote repository so it can be pulled by other sources.

- [Create a Dockerfile](https://docs.docker.com/get-started/02_our_app/)
- Creating a Dockerfile typically requires you to consider the following:
  - Identify an appropriate container image
    - ubuntu vs. python vs. alpine/slim
    - ubuntu - overkill, large image size, wasted resources when running in K8
    - this is a python app, so pick an image that is optimized for it
    - [avoid alpine for python](https://lih-verma.medium.com/alpine-makes-python-docker-builds-way-too-50-slower-and-images-double-2-larger-61d1d43cbc79)
  - Order matters
    - you're building layers.
    - re-use the layers as much as possible
    - have items that change often towards the end
  - [Other Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

Dockerfile for review

``` dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY ./review.py /app
EXPOSE 5000
CMD [ "python", "review.py" ]
```

Create a container image (locally)
Run ‘docker build’ to build a local container image referencing the Dockerfile

{{< tabs >}} {{% tab title="docker build" %}}

``` bash
docker build -f Dockerfile -t localhost:8000/review:0.01 .
```

{{% /tab %}} {{% tab title="docker build Output" %}}

``` text
[+] Building 35.5s (11/11) FINISHED
 => [internal] load build definition from Dockerfile                              0.0s
         ...snip...
 => [3/5] COPY requirements.txt /app                                              0.0s
 => [4/5] RUN pip install -r requirements.txt                                     4.6s
 => [5/5] COPY ./review.py /app                                                   0.0s
 => exporting to image                                                            0.2s
 => => exporting layers                                                           0.2s
 => => writing image sha256:61da27081372723363d0425e0ceb34bbad6e483e698c6fe439c5  0.0s
 => => naming to docker.io/localhost:8000/review:0.1                                   0.0
```

{{% /tab %}}{{< /tabs >}}

Push the container image into a container repository
Run ‘docker push’ to place a copy of the REVIEW container to a remote location

{{< tabs >}} {{% tab title="docker push" %}}

``` bash
docker push localhost:8000/review:0.01
```

{{% /tab %}} {{% tab title="docker push Output" %}}

``` text
The push refers to repository [docker.io/localhost:8000/review]
02c36dfb4867: Pushed
         ...snip...
fd95118eade9: Pushed
0.1: digest: sha256:3651f740abe5635af95d07acd6bcf814e4d025fcc1d9e4af9dee023a9b286f38 size: 2202
```

{{% /tab %}}{{< /tabs >}}

Verify that the image is in Docker Hub. The same info can be found in Docker Desktop

{{< tabs >}} {{% tab title="get catalog" %}}

``` bash
curl -s http://localhost:8000/v2/_catalog
```

{{% /tab %}} {{% tab title="get catalog Output" %}}

``` text
{"repositories":["review"]}
```

{{% /tab %}}{{< /tabs >}}

## 3. Run REVIEW in Kubernetes

Create K8 deployment yaml file for the REVIEW app

Reference: [Creating a Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#creating-a-deployment)

review.deployment.yaml

``` yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: review
  labels:
    app: review
spec:
  replicas: 1
  selector:
    matchLabels:
      app: review
  template:
    metadata:
      labels:
        app: review
    spec:
      imagePullSecrets:
      - name: regcred
      containers:
      - image: localhost:8000/review:0.01
        name: review
        volumeMounts:
        - mountPath: /var/appdata
          name: appdata
      volumes:
      - name: appdata
        hostPath:
          path: /var/appdata
```

Notes regarding review.deployment.yaml:

- labels - K8 uses labels and selectors to tag and identify resources
  - In the next step, we'll create a service and associate it to this deployment using the label
- replicas = 1
  - K8 allows you to scale your deployments horizontally
  - We'll leverage this later to add load and increase our ingestion rate
- regcred provides this deployment with the ability to access your dockerhub credentials which is necessary to pull the container image.
- The volume definition and volumemount make the yelp dataset visible to the container

Create a K8 service yaml file for the review app.

Reference: [Creating a service:](https://kubernetes.io/docs/concepts/services-networking/service/#defining-a-service)

review.service.yaml

``` yaml
apiVersion: v1
kind: Service
metadata:
  name: review
spec:
  type: NodePort
  selector:
    app: review
  ports:
    - port: 5000
      targetPort: 5000
      nodePort: 30000
```

Notes about review.service.yaml:

- the selector associates this service to pods with the label app with the value being review
- the review service exposes the review pods as a network service
  - other pods can now ping 'review' and they will hit a review pod.
  - a pod would get a review if it ran `curl http://review:5000`
- NodePort service
  - the service is accessible to the K8 host by the nodePort, 30000
  - Another machine that has this can get a review if it ran `curl http://<k8 host ip>:30000`

Apply the review deployment and service

``` bash
kubectl apply -f review.service.yaml -f review.deployment.yaml
```

Verify that the deployment and services are running:

{{< tabs >}} {{% tab title="kubectl get deployments" %}}

``` bash
kubectl get deployments
```

{{% /tab %}}{{% tab title="kubectl get deployments output" %}}

``` text
NAME                                                    READY   UP-TO-DATE   AVAILABLE   AGE
review                                                  1/1     1            1           19h
```

{{% /tab %}}{{< /tabs >}}

{{< tabs >}} {{% tab title="kubectl get services" %}}

``` bash
kubectl get services
```

{{% /tab %}}{{% tab title="kubectl get services output" %}}

``` text
NAME                       TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                         AGE
review                     NodePort    10.43.175.21    <none>        5000:30000/TCP                  154d

```

{{% /tab %}}{{< /tabs >}}

{{< tabs >}} {{% tab title="curl localhost" %}}

``` bash
curl localhost:30000
```

{{% /tab %}}{{% tab title="curl localhost Output" %}}

``` text
{
  "message": "Hello, you want to hit /get_review. We have 100000 reviews!"
}
```

{{% /tab %}}{{< /tabs >}}

{{< tabs >}} {{% tab title="get review" %}}

``` bash
curl localhost:30000/get_review
```

{{% /tab %}}{{% tab title="get review Output" %}}

``` text
{"review_id":"Vv9rHtfBrFc-1M1DHRKN9Q","user_id":"EaNqIwKkM7p1bkraKotqrg","business_id":"TA1KUSCu8GkWP9w0rmElxw","stars":3.0,"useful":1,"funny":0,"cool":0,"text":"This is the first time I've actually written a review for Flip, but I've probably been here about 10 times.  \n\nThis used to be where I would take out of town guests who wanted a good, casual, and relatively inexpensive meal.  \n\nI hadn't been for a while, so after a long day in midtown, we decided to head to Flip.  \n\nWe had the fried pickles, onion rings, the gyro burger, their special burger, and split a nutella milkshake.  I have tasted all of the items we ordered previously (with the exception of the special) and have been blown away with how good they were.  My guy had the special which was definitely good, so no complaints there.  The onion rings and the fried pickles were greasier than expected.  Though I've thought they were delicious in the past, I probably wouldn't order either again.  The gyro burger was good, but I could have used a little more sauce.  It almost tasted like all of the ingredients didn't entirely fit together.  Something was definitely off. It was a friday night and they weren't insanely busy, so I'm not sure I would attribute it to the staff not being on their A game...\n\nDon't get me wrong.  Flip is still good.  The wait staff is still amazingly good looking.  They still make delicious milk shakes.  It's just not as amazing as it once was, which really is a little sad.","date":"2010-10-11 18:18:35"}
```

{{% /tab %}}{{< /tabs >}}

{{% notice title="Workshop Question" style="tip" icon="question" %}}
What changes are required if you need to make an update to your Dockerfile now?
{{% /notice %}}
