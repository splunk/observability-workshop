---
title: Dockerize the Service
weight: 13
---
Dockerize the service. Use this `Dockerfile` as a skeleton:

```docker
ARG APP_IMAGE=python:3
FROM $APP_IMAGE as base

FROM base as builder
WORKDIR /app
RUN python -m venv .venv && .venv/bin/pip install --no-cache-dir -U pip setuptools
COPY requirements.txt .
RUN .venv/bin/pip install -r requirements.txt --no-cache-dir -r requirements.txt

FROM base
WORKDIR /app
COPY --from=builder /app /app
COPY app.py .

ENV PATH="/app/.venv/bin:$PATH"
```

Add the [appropriate CMD][docker-cmd] at the end to launch the app.

Stop other instances of the app if you had any running.

Then build and run the image:

{{< tabs >}}
{{% tab title="Shell Command" %}}
docker build . -t wordcount
docker run -p 5000:5000 wordcount:latest
{{% /tab %}}
{{< /tabs >}}

Test the service in another shell:

{{< tabs >}}
{{% tab title="Shell Command" %}}

``` bash
curl -X POST http://127.0.0.1:5000/wordcount -F text=@hamlet.txt
```

{{% /tab %}}
{{< /tabs >}}

The milestone for this task is `05docker`.

[docker-cmd]: https://docs.docker.com/engine/reference/builder/#cmd
