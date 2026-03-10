---
title: 1. Build the App
weight: 1
---

The workshop includes a simple Spring Boot application with a few REST endpoints. Let's build it.

## Verify Java and Maven

Your instance has OpenJDK 17 and Maven pre-installed. Confirm:

{{< tabs >}}
{{% tab title="Command" %}}

```bash
java -version && mvn -version
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
openjdk version "17.0.x" ...
Apache Maven 3.x.x ...
```

{{% /tab %}}
{{< /tabs >}}

## Build the Application

Navigate to the workshop app directory and build the fat JAR:

{{< tabs >}}
{{% tab title="Command" %}}

```bash
cd ~/workshop/appd/app
mvn package -DskipTests
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
[INFO] BUILD SUCCESS
```

{{% /tab %}}
{{< /tabs >}}

{{% notice title="First build" style="info" icon="info-circle" %}}
The first `mvn package` downloads Spring Boot dependencies. This takes 30-60 seconds. Subsequent builds are much faster.
{{% /notice %}}

## Test the Application (without AppD)

Run the app briefly to confirm it starts:

```bash
java -jar target/ingest-workshop-1.0.0.jar &
```

Wait a few seconds, then test:

{{< tabs >}}
{{% tab title="Command" %}}

```bash
curl -s localhost:8080/health | jq .
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```json
{
  "status": "healthy"
}
```

{{% /tab %}}
{{< /tabs >}}

Stop the app before proceeding:

```bash
kill %1
```

The application works. Next, you'll download the AppDynamics Java Agent so you can attach it to this process.
