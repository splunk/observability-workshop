---
title: Verifying both Kubernetes and the PetClinic Microservices application
linkTitle: 20. Verify Kubernetes and PetClinic
weight: 20
---

## 1. Verify the installation by checking Metrics and Logs

Once the installation is completed, you can login into the  **Splunk Observability Cloud** with the URL provided by the Instructor.

First, Navigate to **Kubernetes Navigator** view in the **Infrastructure** ![infra](../images/infra-icon.png?classes=inline&height=25px) section to see the metrics from your cluster in the **K8s nodes** pane. Change the *Time* filter to the last 15 Minutes (-15m) to focus on the latest data.

Use the regular filter option at the top of the Navigator and select `k8s.cluster.name` **(1)** and type or select the cluster name of your workshop instance (you can get the unique part from your cluster name by using the `INSTANCE` from the output from the shell script you ran earlier). (You can also select your cluster by clicking on its image in the cluster pane.)
You should now only have your cluster visible **(2)**.

![Navigator](../images/navigator.png)

You should see metrics **(3)** of your cluster and the log events **(4)** chart should start to be populated with log line events coming from your cluster. Click on one of the bars to peek at the log lines coming in from you cluster.

![logs](../images/k8s-peek-at-logs.png)

Also, a `Mysql` pane **(5)** should appear, when you click on that pane, you can see the MySQL related metrics from your database.

![mysql metrics](../images/mysql-metrics.png)

Once you see data flowing in from your host (`metrics and logs`) and MySQL shows `metrics` as well we can move on to the actual PetClinic application.
## 2. Check the Petshop Website

To test the application you need to obtain the public IP address of the instance you are running on. You can do this by running the following command:

```bash
curl ifconfig.me

```

You will see an IP address returned, make a note of this as we will need it to validate that the application is running.

You can validate if the application is running by visiting `http://<IP_ADDRESS>:81` (replace `<IP_ADDRESS>` with the IP address you obtained earlier). You should see the PetClinic application running.  

![Pet shop](../images/petclinic.png)

Make sure the application is working correctly by visiting the **All Owners** **(1)** and **Veterinarians**  **(2)**tabs, you should get a list of names in each case.

![owners](../images/pet-clininc-owners.png)

 If you're familiar with the Standard version, you will notice a slightly longer response time due to the architecture used.
