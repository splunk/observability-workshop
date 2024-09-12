---
title: Rebuild PetClinic
linkTitle: 2. Rebuild PetClinic
weight: 2
hidden: true
---

Before we can build the new services with the updated log format we need to add the OpenTelemetry dependency that handles field injection to the `pom.xml` of our services:
{{< tabs >}}
{{% tab title="Adding OTel dependencies" %}}

```bash
. ~/workshop/petclinic/scripts/add_otel.sh
```

{{% /tab %}}
{{% tab title="Output" %}}

```text
Dependencies added successfully in spring-petclinic-admin-server
Dependencies added successfully in spring-petclinic-api-gateway
Dependencies added successfully in spring-petclinic-config-server
Dependencies added successfully in spring-petclinic-discovery-server
Dependencies added successfully in spring-petclinic-customers-service
Dependencies added successfully in spring-petclinic-vets-service
Dependencies added successfully in spring-petclinic-visits-service
Dependency addition complete!
```

{{% /tab %}}
{{< /tabs >}}

The Services are now ready to be built, so run the script that will use the `maven` command to compile/build/package the PetClinic microservices:

{{% notice note %}}
Note the `-P buildDocker`, this will build the new containers and take 3-5 minutes to complete.
{{% /notice %}}

{{< tabs >}}
{{% tab title="Running maven" %}}

```bash
./mvnw clean install -D skipTests -P buildDocker
```

{{% /tab %}}
{{% tab title="Maven Output" %}}

```text
...
Successfully tagged quay.io/phagen/spring-petclinic-api-gateway:latest
[INFO] Built quay.io/phagen/spring-petclinic-api-gateway
[INFO] ------------------------------------------------------------------------
[INFO] Reactor Summary:
[INFO] 
[INFO] spring-petclinic-microservices 0.0.1 ............... SUCCESS [  0.770 s]
[INFO] spring-petclinic-admin-server ...................... SUCCESS [01:03 min]
[INFO] spring-petclinic-customers-service ................. SUCCESS [ 29.031 s]
[INFO] spring-petclinic-vets-service ...................... SUCCESS [ 22.145 s]
[INFO] spring-petclinic-visits-service .................... SUCCESS [ 20.451 s]
[INFO] spring-petclinic-config-server ..................... SUCCESS [ 12.260 s]
[INFO] spring-petclinic-discovery-server .................. SUCCESS [ 14.174 s]
[INFO] spring-petclinic-api-gateway 0.0.1 ................. SUCCESS [ 29.832 s]
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 03:14 min
[INFO] Finished at: 2024-01-02T12:43:20Z
[INFO] ------------------------------------------------------------------------
```

{{% /tab %}}
{{< /tabs >}}

Given that Kubernetes needs to pull these freshly built images from somewhere, we are going to store them in the repository we tested earlier. To do this, run the script that will push the newly built containers into our local repository:

{{< tabs >}}
{{% tab title="pushing Containers" %}}

```bash
. ~/workshop/petclinic/scripts/push_docker.sh 
```

{{% /tab %}}
{{% tab title="Docker Push Output (partial)" %}}

```text
The push refers to repository [localhost:5000/spring-petclinic-vets-service]
0391386bcb2a: Preparing
bbb67f51a186: Preparing
105351d0ada3: Preparing
49cfeae6cb9f: Preparing
b4da5101fcde: Preparing
49cfeae6cb9f: Pushed
e742c14be110: Mounted from spring-petclinic-visits-service
540aa741fede: Mounted from spring-petclinic-visits-service
a1dfe59d4939: Mounted from spring-petclinic-visits-service
1e99e92c46bf: Mounted from spring-petclinic-visits-service
f5aa38537736: Mounted from spring-petclinic-visits-service
d2210512edb4: Mounted from spring-petclinic-visits-service
8e87ff28f1b5: Mounted from spring-petclinic-visits-service
local: digest: sha256:42337b2a4ff7d0ac9b7c2cf3c70aa20b7b52d092f1e05d351e031dd7fad956fc size: 3040
The push refers to repository [localhost:5000/spring-petclinic-customers-service]
15d54d9adca8: Preparing
886f6def5b35: Preparing
1575ae90e858: Preparing
ccc884d92d18: Preparing
b4da5101fcde: Preparing
ccc884d92d18: Pushed
e742c14be110: Mounted from spring-petclinic-vets-service
540aa741fede: Mounted from spring-petclinic-vets-service
a1dfe59d4939: Mounted from spring-petclinic-vets-service
1e99e92c46bf: Mounted from spring-petclinic-vets-service
f5aa38537736: Mounted from spring-petclinic-vets-service
d2210512edb4: Mounted from spring-petclinic-vets-service
8e87ff28f1b5: Mounted from spring-petclinic-vets-service
local: digest: sha256:3601c6e7f58224001946058fb0400483fbb8f1b0ea8a6dbaf403c62b4c1908be size: 3042
```

{{% /tab %}}
{{< /tabs >}}

The containers should now be stored in the local repository, let's confirm by checking the catalog:

{{< tabs >}}
{{% tab title="Check Catalog" %}}

```bash
curl -X GET http://localhost:9999/v2/_catalog
```

{{% /tab %}}
{{% tab title="Catalog Output" %}}

``` json
{"repositories":["spring-petclinic-admin-server","spring-petclinic-api-gateway","spring-petclinic-config-server","spring-petclinic-customers-service","spring-petclinic-discovery-server","spring-petclinic-vets-service","spring-petclinic-visits-service"]}
```

{{% /tab %}}
{{< /tabs >}}
