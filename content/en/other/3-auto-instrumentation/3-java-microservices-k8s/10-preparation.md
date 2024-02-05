---
title: Preparation of the Pet Clinic application. 
linkTitle: 10. Preparation
weight: 10
---

## 1. Validate the settings for your workshop

The instructor will provide you with the log in information for the instance that we will using during the workshop.
When you first log into your instance, you wil be greeted by the Splunk Logo as shown below:

```text
❯ ssh -p 2222 ubuntu@[IP-ADRESS]

███████╗██████╗ ██╗     ██╗   ██╗███╗   ██╗██╗  ██╗    ██╗  
██╔════╝██╔══██╗██║     ██║   ██║████╗  ██║██║ ██╔╝    ╚██╗ 
███████╗██████╔╝██║     ██║   ██║██╔██╗ ██║█████╔╝      ╚██╗
╚════██║██╔═══╝ ██║     ██║   ██║██║╚██╗██║██╔═██╗      ██╔╝
███████║██║     ███████╗╚██████╔╝██║ ╚████║██║  ██╗    ██╔╝ 
╚══════╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝    ╚═╝  
Last login: Mon Feb  5 11:04:54 2024 from [Redacted]
Waiting for cloud-init status...
Your instance is ready!
ubuntu@java-workshop-1 ~ $ 
```

If this isn't shown, or you see an error, log out and give it a minute or so, then try to log in again as the instance might not have finished the initial boot sequence. If it still does not show the above Welcome page, reach out to your Instructor.

Next, let's ensure your instance is configured correctly, we need to confirm that the required environment variables for this workshop are set correctly. In your terminal run the following command:

``` bash
. ~/workshop/petclinic/scripts/check_env.sh
```

In the output check the following environment variables are present and have actual valid values set:

```text
ACCESS_TOKEN = [Redacted]
REALM = [Realm]
RUM_TOKEN = [Redacted]
HEC_TOKEN = [Redacted]
HEC_URL = https://[...]/services/collector/event
INSTANCE = [Your workshop name]
```

Please make a note of the `INSTANCE` environment variable value as this is the reference to you workshop instance and we will need it later to filter data in the **Splunk Observability Suite** UI.

For this workshop, **all** of the above are required. If any have values missing, please contact your instructor.

## 2. Deploying the prebuilt containers into Kubernetes

The second thing we need to do, well ..., is to set up our application. The first deployment of our application will be using prebuilt containers to give us the base scenario: a regular Java microservices-based application running in Kubernetes.

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
In rare occasions, you may encounter the above error at this point.  please lpg out and back in, and verify the above env variables are all set correctly. If not please, please contact your instructor.

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
cd ~;git clone https://github.com/hagen-p/spring-petclinic-microservices.git
```

Change into the `spring-petclinic` directory:

```bash
cd ~/spring-petclinic-microservices
```

Next, lets test the download and run the script that will use the `maven` command to compile/build the PetClinic microservices:
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

## 3. Verify the local Docker Repository

Once we have our Auto instrumentation up and running with the existing containers, we are going to build our own containers to show some of the additional instrumentation features of Opentelemetry Java. Only then we will touch the  config files or the source code. We will add some annotations to it to get even more valuable data from our Java application and enable the injection of trace data into  the logs. 

once we build these containers, Kubernetes will need to pull these new images from somewhere. To enable this we have created a local repository, so Kubernetes can pull those local images.

We can see if the repository is up and running by checking the inventory with the below command, it should return an empty list  
**{"repositories":[]}**

```bash
 curl -X GET http://localhost:9999/v2/_catalog 
```

If this is not up, reach out to your Instructor for a replacement instance.

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
