---
title: Create a Monolith Service
weight: 5
---
Checkout the milestone for this task. See the introduction for a brief howto.

{{< tabs >}}
{{% tab title="Shell Command" %}}
git reset --hard && git clean -fdx && git checkout 01service{{% /tab %}}
{{< /tabs >}}

Let's get python sorted first. On a provided AWS instance, `python3` is already available.

If you are on a Mac:

{{< tabs >}}
{{% tab title="Shell Command" %}}
brew install python@3
{{% /tab %}}
{{< /tabs >}}

On another system, install a recent version of python (i.e. 3.x) with your package manager.

Navigate to `o11y-bootcamp/bootcamp/service/src` and run the provided python service:

{{< tabs >}}
{{% tab title="Shell Command: python3" %}}

``` bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

{{% /tab %}}
{{% tab title="Example Output python3" %}}

``` text
* Serving Flask app 'app' (lazy loading)
* Environment: production
WARNING: This is a development server. Do not use it in a production deployment.
Use a production WSGI server instead.
* Debug mode: off
* Running on all addresses.
WARNING: This is a development server. Do not use it in a production deployment.
* Running on http://10.42.1.202:5000/ (Press CTRL+C to quit)
```

{{% /tab %}}
{{< /tabs >}}

Then test the service in a separate shell in the `~/o11y-bootcamp/bootcamp/service/src` directory with:

{{< tabs >}}
{{% tab title="Shell Command: curl" %}}

``` bash
curl -X POST http://127.0.0.1:5000/wordcount -F text=@hamlet.txt{{% /tab %}}
{{% tab title="Example Output: curl" %}}
[["in", 436], ["hamlet", 484], ["my", 514], ["a", 546], ["i", 546], ["you", 550], ["of", 671], ["to", 763], ["and", 969], ["the", 1143]]
```

%{{% /tab %}}
{{< /tabs >}}

The bootcamp contains other text files at `~/nlp/resources/corpora`. To use a random example:

{{< tabs >}}
{{% tab title="Shell Command" %}}

``` bash
SAMPLE=$(find ~/nlp/resources/corpora/gutenberg -name '*.txt' | shuf -n1)
curl -X POST http://127.0.0.1:5000/wordcount -F text=@$SAMPLE{{% /tab %}}
```

{{< /tabs >}}

To generate load:

{{< tabs >}}
{{% tab title="Shell Command" %}}

``` bash
FILES=$(find ~/nlp/resources/corpora/gutenberg -name '*.txt')
while true; do
    SAMPLE=$(shuf -n1 <<< "$FILES")
    curl -X POST http://127.0.0.1:5000/wordcount -F text=@${SAMPLE}
    sleep 1
done
```

{{% /tab %}}
{{< /tabs >}}
