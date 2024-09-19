---
title: Building the Spring PetClinic Application
linkTitle: 2. Building PetClinic
weight: 2
---

The first thing we need to set up APM is... well, an application. For this exercise, we will use the Spring PetClinic application. This is a very popular sample Java application built with the Spring framework (Springboot).

First, clone the PetClinic GitHub repository, and then we will compile, build, package and test the application:

```bash
git clone https://github.com/spring-projects/spring-petclinic
```

Change into the `spring-petclinic` directory:

<!--
```bash
cd spring-petclinic && git checkout 276880e
```
-->

```bash
cd spring-petclinic
```

Using Docker, start a MySQL database for PetClinic to use:

```bash
docker run -d -e MYSQL_USER=petclinic -e MYSQL_PASSWORD=petclinic -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=petclinic -p 3306:3306 docker.io/biarms/mysql:5.7
```

Next, we will start another container running Locust that will generate some simple traffic to the PetClinic application. Locust is a simple load-testing tool that can be used to generate traffic to a web application.

```bash
docker run --network="host" -d -p 8090:8090 -v ~/workshop/petclinic:/mnt/locust docker.io/locustio/locust -f /mnt/locust/locustfile.py --headless -u 1 -r 1 -H http://127.0.0.1:8083
```

Next, compile, build and package PetClinic using `maven`:

```bash
./mvnw package -Dmaven.test.skip=true
```

> [!INFO]
> This will take a few minutes the first time you run and will download a lot of dependencies before it compiles the application. Future builds will be a lot quicker.

Once the build completes, you need to obtain the public IP address of the instance you are running on. You can do this by running the following command:

```bash
curl http://ifconfig.me
```

You will see an IP address returned, make a note of this as we will need it to validate that the application is running.
