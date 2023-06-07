---
title: Add Prometheus metrics
weight: 7
---
We need visibility into performance - let us add metrics with [Prometheus][prometheus].

Install the [Python Prometheus client][py-prom] as a dependency:

{{< tabs >}}
{{% tab title="Shell Command" %}}
echo "prometheus-client" >> requirements.txt
python3 -m venv .venv
source .venv/bin/activate
.venv/bin/pip install -r requirements.txt
{{% /tab %}}
{{< /tabs >}}

Import the modules by editing `app.py`. These imports go towards the top of the file:

```python
import prometheus_client
from prometheus_client.exposition import CONTENT_TYPE_LATEST
from prometheus_client import Counter
```

Define a metrics endpoint before `@app.route('/wordcount', methods=['POST'])`:

```python
@app.route('/metrics')
def metrics():
    return Response(prometheus_client.generate_latest(), mimetype=CONTENT_TYPE_LATEST)
```

And use this python snippet after `app = Flask(__name__)` to define a new counter metric:

```python
c_recv = Counter('characters_recv', 'Number of characters received')
```

Increase the counter metric after `data = request.files['text'].read().decode('utf-8')`:

```python
c_recv.inc(len(data))
```

Test that the application exposes metrics by hitting the endpoint while the app is running:

{{< tabs >}}
{{% tab title="Shell Command" %}}

``` bash
curl http://127.0.0.1:5000/metrics
```

{{% /tab %}}
{{< /tabs >}}

The milestone for this task is `02service-metrics`.

[prometheus]: https://prometheus.io/docs/introduction/overview/#architecture
[py-prom]: https://pypi.org/project/prometheus-client/
