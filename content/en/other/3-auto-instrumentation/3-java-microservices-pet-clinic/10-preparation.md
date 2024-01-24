---
title: Preparation of the Pet Clinic application. 
linkTitle: 10. Preparation
weight: 10
---

## 1. Deploying the prebuilt containers into Kubernetes

The first thing we need to set up is ... well, an application. The first deployment of our application will be using prebuilt containers to give us the base scenario: a Java microservices-based application running in Kubernetes.

So let's deploy our application:
{{< tabs >}}
{{% tab title="kubectl apply" %}}

```bash
kubectl apply -f ~/workshop/petclinic/petclinic-deploy.yaml
```

{{% /tab %}}
{{% tab title="kubectl apply Output" %}}

```text
deployment.apps/config-server created
service/config-server created
deployment.apps/discovery-server created
service/discovery-server created
deployment.apps/api-gateway created
service/api-gateway created
service/api-gateway-external created
deployment.apps/customers-service created
service/customers-service created
deployment.apps/vets-service created
service/vets-service created
deployment.apps/visits-service created
service/visits-service created
deployment.apps/admin-server created
service/admin-server created
service/petclinic-db created
deployment.apps/petclinic-db created
configmap/petclinic-db-initdb-config created
deployment.apps/petclinic-loadgen-deployment created
configmap/scriptfile created
```

{{% /tab %}}
{{< /tabs >}}

<!-- {{% notice title="In case of error Unable to read /etc/rancher/k3s/k3s.yaml" style="warning" %}}
In rare occasions, you may encounter the above error at this point, this is due to incorrect file permission on the Kubernetes config file. This can easily be resolved by running the following command:

``` bash
sudo chmod 777 /etc/rancher/k3s/k3s.yaml
```

{{% /notice %}} -->
At this point we can verify the deployment by checking if the Pods are running:
{{< tabs >}}
{{% tab title="kubectl get pods" %}}

```bash
kubectl get pods
```

{{% /tab %}}
{{% tab title="kubectl get pods Output" %}}

```text
NAME                                           READY   STATUS    RESTARTS   AGE
config-server-7645d4449f-kdwh6                 1/1     Running   0          86s
petclinic-db-64d998bb66-n2464                  1/1     Running   0          85s
discovery-server-6f4c756dff-nx8tl              1/1     Running   0          86s
admin-server-8f67bdf56-tcpkl                   1/1     Running   0          85s
customers-service-74f5cf6d6f-nhkxh             1/1     Running   0          86s
vets-service-6869959674-nb67v                  1/1     Running   0          86s
visits-service-6f9d987c85-4476j                1/1     Running   0          85s
api-gateway-6ddcf94c5f-k2ccg                   1/1     Running   0          86s
petclinic-loadgen-deployment-994b69695-8rd9k   1/1     Running   0          85s
```

{{% /tab %}}
{{< /tabs >}}

Make sure the output of get pods matches the output as shown above. This may take a minute or so, try again until all services are shown as **RUNNING**.  

Once they are running, the application will take a few minutes to  fully start up, create the database and synchronize all the services, so let's get the actual source code for the application downloaded in the mean-time.

## 2. Downloading the Spring Microservices PetClinic Application

 For this exercise, we will use the Spring microservices PetClinic application. This is a very popular sample Java application built with the Spring framework (Springboot) and we are using a version witch actual microservices.

First, clone the PetClinic GitHub repository, as we will need this later in the workshop to compile, build, package and containerize the application:

```bash
cd ~
git clone https://github.com/hagen-p/spring-petclinic-microservices.git
```

Change into the `spring-petclinic` directory:

```bash
cd ~/spring-petclinic-microservices
```

Next, run the script that will use the `maven` command to compile/build the PetClinic microservices:
{{< tabs >}}
{{% tab title="Running maven" %}}

```bash
./mvnw clean install -DskipTests
```

{{% /tab %}}
{{% tab title="Maven Output" %}}

```text
[INFO] ------------------------------------------------------------------------
[INFO] Reactor Summary:
[INFO]
[INFO] spring-petclinic-microservices 0.0.1 ............... SUCCESS [  0.552 s]
[INFO] spring-petclinic-admin-server ...................... SUCCESS [ 16.125 s]
[INFO] spring-petclinic-customers-service ................. SUCCESS [  6.204 s]
[INFO] spring-petclinic-vets-service ...................... SUCCESS [  1.791 s]
[INFO] spring-petclinic-visits-service .................... SUCCESS [  1.696 s]
[INFO] spring-petclinic-config-server ..................... SUCCESS [  1.466 s]
[INFO] spring-petclinic-discovery-server .................. SUCCESS [  1.797 s]
[INFO] spring-petclinic-api-gateway 0.0.1 ................. SUCCESS [ 13.999 s]
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 45.431 s
[INFO] Finished at: 2024-01-10T13:56:53Z
[INFO] ------------------------------------------------------------------------
```

{{% /tab %}}
{{< /tabs >}}

{{% notice style="info" %}}
This will take a few minutes the first time you run, `maven` will download a lot of dependencies before it compiles the application. Future builds will be a lot quicker.
{{% /notice %}}

## 3. Set up a local Docker Repository

Once we have our Auto instrumentation up and running, we are going to use show some  of the additional instrumentation features of Opentelemetry Java. This will be the first time we will touch the source code and add some annotations to it to get even more valuable data from our Java application. Kubernetes will need to pull these new images from somewhere, so let's setup a local repository, so Kubernetes can pull these local images.

{{< tabs >}}
{{% tab title="Install Docker Repository" %}}

```bash
docker run -d -p 5000:5000 --restart=always --name registry registry:2 
```

{{% /tab %}}
{{% tab title="Docker Output" %}}

``` text
Unable to find image 'registry:2' locally
2: Pulling from library/registry
c926b61bad3b: Pull complete 
5501dced60f8: Pull complete 
e875fe5e6b9c: Pull complete 
21f4bf2f86f9: Pull complete 
98513cca25bb: Pull complete 
Digest: sha256:0a182cb82c93939407967d6d71d6caf11dcef0e5689c6afe2d60518e3b34ab86
Status: Downloaded newer image for registry:2
a7d52001836504cf1724e9817ad6167a4458a9e73d33a82f11f33681fe2d6c3e
```

{{% /tab %}}
{{< /tabs >}}

We can see if the repository is up and running by checking the inventory with the below command, it should return an empty list 
**{"repositories":[]}**

```bash
 curl -X GET http://localhost:5000/v2/_catalog 
```

## 4. Check the Petshop Website

To test the application you need to obtain the public IP address of the instance you are running on. You can do this by running the following command:

```bash
curl ifconfig.me

```

You will see an IP address returned, make a note of this as we will need it to validate that the application is running.

You can validate if the application is running by visiting `http://<IP_ADDRESS>:81` (replace `<IP_ADDRESS>` with the IP address you obtained earlier). You should see the PetClinic application running.  

![Pet shop](../images/petclinic.png)
Make sure the application is working correctly by visiting the **All Owners** and **Veterinarians** tabs, you should get a list of names in each case. If your familiar with the Standard version, you will notice a slightly longer response time due to the architecture used.

We now have our application running in Kubernetes, without an OpenTelemetry Collector deployed, so there is no Observability data in **Splunk Observability Cloud** yet.
Lets go and fix that.
