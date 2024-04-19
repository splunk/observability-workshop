---
title: Verify the PetClinic Website
linkTitle: 1. Verify the PetClinic Webiste
weight: 1
---

To test the application you need to obtain the public IP address of the instance you are running on. You can do this by running the following command:

``` bash
curl http://ifconfig.me

```

You can validate if the application is running by visiting `http://<IP_ADDRESS>:81` (replace `<IP_ADDRESS>` with the IP address you obtained above). You should see the PetClinic application running.

## UPDATE SCREENSHOTS TO BE THE SAME WIDTH

![Pet shop](../../images/petclinic.png)

Make sure the application is working correctly by visiting the **All Owners** **(1)** and **Veterinarians** **(2)** tabs, you should get a list of names in each case.

![owners](../../images/pet-clininc-owners.png)

 If you're familiar with the Standard version, you will notice a slightly longer response time due to the architecture used.
