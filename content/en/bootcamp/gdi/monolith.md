---
title: Create a Monolith Service
weight: 5
---
Checkout the milestone for this task. See the introduction for a brief howto.

{{<tabpane>}}
{{<tab header="Shell Command" lang="bash" >}}
git reset --hard && git clean -fdx && git checkout 01service{{</tab>}}
{{</tabpane>}}

Let's get python sorted first. On a provided AWS instance, `python3` is already available.

If you are on a Mac:

{{<tabpane>}}
{{<tab header="Shell Command" lang="bash" >}}
brew install python@3
{{</tab>}}
{{</tabpane>}}

On another system, install a recent version of python (i.e. 3.x) with your package manager.

Navigate to `o11y-bootcamp/bootcamp/service/src` and run the provided python service:

{{<tabpane>}}
{{<tab header="Shell Command: python3" lang="bash" >}}
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py{{</tab>}}
{{<tab header="Example Output python3" lang="text" >}}
* Serving Flask app 'app' (lazy loading)
* Environment: production
WARNING: This is a development server. Do not use it in a production deployment.
Use a production WSGI server instead.
* Debug mode: off
* Running on all addresses.
WARNING: This is a development server. Do not use it in a production deployment.
* Running on http://10.42.1.202:5000/ (Press CTRL+C to quit)
{{</tab>}}
{{</tabpane>}}


Then test the service in a separate shell in the `~/o11y-bootcamp/bootcamp/service/src` directory with:

{{<tabpane>}}
{{<tab header="Shell Command: curl" lang="bash" >}}
curl -X POST http://127.0.0.1:5000/wordcount -F text=@hamlet.txt{{</tab>}}
{{<tab header="Example Output: curl" lang="json" >}}
[["in", 436], ["hamlet", 484], ["my", 514], ["a", 546], ["i", 546], ["you", 550], ["of", 671], ["to", 763], ["and", 969], ["the", 1143]]%{{</tab>}}
{{</tabpane>}}

The bootcamp contains other text files at `~/nlp/resources/corpora`. To use a random example:

{{<tabpane>}}
{{<tab header="Shell Command" lang="bash" >}}
SAMPLE=$(find ~/nlp/resources/corpora/gutenberg -name '*.txt' | shuf -n1)
curl -X POST http://127.0.0.1:5000/wordcount -F text=@$SAMPLE{{</tab>}}
{{</tabpane>}}

To generate load:

{{<tabpane>}}
{{<tab header="Shell Command" lang="bash" >}}
FILES=$(find ~/nlp/resources/corpora/gutenberg -name '*.txt')
while true; do
    SAMPLE=$(shuf -n1 <<< "$FILES")
    curl -X POST http://127.0.0.1:5000/wordcount -F text=@${SAMPLE}
    sleep 1
done
{{</tab>}}
{{</tabpane>}}
