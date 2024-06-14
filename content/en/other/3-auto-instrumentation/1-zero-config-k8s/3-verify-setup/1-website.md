---
title: Verify the PetClinic Website
linkTitle: 1. Verify PetClinic Website
weight: 1
---

To test the application you need to obtain the public IP address of the instance you are running on. You can do this by running the following command:

``` bash
curl http://ifconfig.me

```

You can validate if the application is running by visiting **http://<IP_ADDRESS>:81** (replace **<IP_ADDRESS>** with the IP address you obtained above). You should see the PetClinic application running.

![Pet shop](../../images/petclinic.png)

Make sure the application is working correctly by visiting the **All Owners** **(1)** and **Veterinarians** **(2)** tabs, you should get a list of names in each case.

{{% notice note %}}
As each service needs to start up and synchronize with the database, it may take a few minutes for the application to fully start up.
{{% /notice %}}

![owners](../../images/petclinic-owners.png)
