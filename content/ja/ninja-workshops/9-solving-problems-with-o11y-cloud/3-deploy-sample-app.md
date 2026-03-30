---
title: サンプルアプリケーションのデプロイと OpenTelemetry による計装
linkTitle: 3. サンプルアプリケーションのデプロイと OpenTelemetry による計装
weight: 3
time: 15 minutes
---

この時点で、K8sクラスターにOpenTelemetry Collectorをデプロイし、
インフラストラクチャメトリクスの収集に成功しています。

次のステップは、サンプルアプリケーションをデプロイし、
OpenTelemetryで計装してトレースをキャプチャすることです。

Pythonで書かれたマイクロサービスベースのアプリケーションを使用します。ワークショップをシンプルに保つため、
credit check serviceとcredit processor serviceの2つのサービスに焦点を当てます。

## アプリケーションのデプロイ

時間を節約するため、両方のサービスのDockerイメージを既に構築してDocker Hubで公開しています。
以下のコマンドで、K8sクラスターにcredit check serviceをデプロイできます：

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl apply -f /home/splunk/workshop/tagging/creditcheckservice-py-with-tags/creditcheckservice-dockerhub.yaml
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
deployment.apps/creditcheckservice created
service/creditcheckservice created
```

{{% /tab %}}
{{< /tabs >}}

次に、credit processor serviceをデプロイしましょう：

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl apply -f /home/splunk/workshop/tagging/creditprocessorservice/creditprocessorservice-dockerhub.yaml
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
deployment.apps/creditprocessorservice created
service/creditprocessorservice created
```

{{% /tab %}}
{{< /tabs >}}

最後に、トラフィックを生成するロードジェネレーターをデプロイしましょう：

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl apply -f /home/splunk/workshop/tagging/loadgenerator/loadgenerator-dockerhub.yaml
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
deployment.apps/loadgenerator created
```

{{% /tab %}}
{{< /tabs >}}

## アプリケーションの詳細を確認する

このセクションでは、アプリケーションの概要を説明します。アプリケーションの完全な
ソースコードを確認したい場合は、[GitHub の Observability Workshop リポジトリ](https://github.com/splunk/observability-workshop/tree/main/workshop/tagging)を参照してください。

### OpenTelemetry による計装

credit check serviceとcredit processor serviceのビルドに使用されるDockerfileを見ると、
OpenTelemetryで既に計装されていることがわかります。例として、
`/home/splunk/workshop/tagging/creditcheckservice-py-with-tags/Dockerfile` を見てみましょう：

``` dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements over
COPY requirements.txt .

RUN apt-get update && apt-get install --yes gcc python3-dev

ENV PIP_ROOT_USER_ACTION=ignore

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy main app
COPY main.py .

# Bootstrap OTel
RUN splunk-py-trace-bootstrap

# Set the entrypoint command to run the application
CMD ["splunk-py-trace", "python3", "main.py"]
```

`splunk-py-trace-bootstrap` が含まれていることがわかります。これは、アプリケーションで使用される
サポートされているパッケージにOpenTelemetryの計装をインストールします。また、`splunk-py-trace` が
アプリケーションを起動するコマンドの一部として使用されていることもわかります。

`/home/splunk/workshop/tagging/creditcheckservice-py-with-tags/requirements.txt` ファイルを確認すると、
パッケージのリストに `splunk-opentelemetry[all]` が含まれていることがわかります。

最後に、このサービスのデプロイに使用したKubernetesマニフェスト（`/home/splunk/workshop/tagging/creditcheckservice-py-with-tags/creditcheckservice-dockerhub.yaml`）を確認すると、
コンテナに環境変数が設定されており、OTLPデータのエクスポート先を
OpenTelemetryに伝えていることがわかります：

``` yaml
  env:
    - name: PORT
      value: "8888"
    - name: NODE_IP
      valueFrom:
        fieldRef:
          fieldPath: status.hostIP
    - name: OTEL_EXPORTER_OTLP_ENDPOINT
      value: "http://$(NODE_IP):4317"
    - name: OTEL_SERVICE_NAME
      value: "creditcheckservice"
    - name: OTEL_PROPAGATORS
      value: "tracecontext,baggage"
```

これだけで、サービスをOpenTelemetryで計装できます！

### アプリケーションの詳細を確認する

アプリケーションでいくつかのカスタムタグをキャプチャしていますが、これについては後ほど詳しく見ていきます。その前に、
タグの概念とそれが重要な理由について説明します。

### タグとは？

タグは、トレース内のスパンに関する追加のメタデータを提供するキーと値のペアで、**Splunk APM** に送信するスパンのコンテキストを充実させることができます。

例えば、決済処理アプリケーションでは以下を追跡できると便利です：

* 使用された決済方法（クレジットカード、ギフトカードなど）
* 決済をリクエストした顧客のID

これにより、決済処理中にエラーやパフォーマンスの問題が発生した場合、トラブルシューティングに必要なコンテキストを得ることができます。

一部のタグはOpenTelemetry Collectorで追加できますが、このワークショップで扱うタグはより詳細なもので、アプリケーション開発者がOpenTelemetry SDKを使用して追加します。

### なぜタグはそれほど重要なのか？

タグは、アプリケーションを真にオブザーバブルにするために不可欠です。トレースにコンテキストを追加することで、
なぜ一部のユーザーは素晴らしい体験を得て、他のユーザーはそうでないのかを理解する助けになります。また、
**Splunk Observability Cloud** の強力な機能は、タグを活用して根本原因に素早くたどり着くことを支援します。

> 先に進む前に用語について説明します。このワークショップでは **tags**（タグ）について説明しますが、
> これは **Splunk Observability Cloud** で使用する用語です。OpenTelemetry では
> 代わりに **attributes**（属性）という用語を使用します。そのため、このワークショップ全体で
> タグが言及されている場合、それは属性と同義として扱ってください。

### タグはどのようにキャプチャされるのか？

Pythonアプリケーションでタグをキャプチャするには、まず `/home/splunk/workshop/tagging/creditcheckservice-py-with-tags/main.py` ファイルの先頭に
import文を追加してtraceモジュールをインポートします：

```` python
import requests
from flask import Flask, request
from waitress import serve
from opentelemetry import trace  # <--- ADDED BY WORKSHOP
...
````

次に、現在のスパンへの参照を取得して、属性（別名タグ）を追加できるようにします：

```` python
def credit_check():
    current_span = trace.get_current_span()  # <--- ADDED BY WORKSHOP
    customerNum = request.args.get('customernum')
    current_span.set_attribute("customer.num", customerNum)  # <--- ADDED BY WORKSHOP
...
````

とても簡単ですよね？credit check serviceで合計4つのタグをキャプチャしており、最終的な結果は以下のようになります：

```` python
def credit_check():
    current_span = trace.get_current_span()  # <--- ADDED BY WORKSHOP
    customerNum = request.args.get('customernum')
    current_span.set_attribute("customer.num", customerNum)  # <--- ADDED BY WORKSHOP

    # Get Credit Score
    creditScoreReq = requests.get("http://creditprocessorservice:8899/getScore?customernum=" + customerNum)
    creditScoreReq.raise_for_status()
    creditScore = int(creditScoreReq.text)
    current_span.set_attribute("credit.score", creditScore)  # <--- ADDED BY WORKSHOP

    creditScoreCategory = getCreditCategoryFromScore(creditScore)
    current_span.set_attribute("credit.score.category", creditScoreCategory)  # <--- ADDED BY WORKSHOP

    # Run Credit Check
    creditCheckReq = requests.get("http://creditprocessorservice:8899/runCreditCheck?customernum=" + str(customerNum) + "&score=" + str(creditScore))
    creditCheckReq.raise_for_status()
    checkResult = str(creditCheckReq.text)
    current_span.set_attribute("credit.check.result", checkResult)  # <--- ADDED BY WORKSHOP

    return checkResult
````

## トレースデータを確認する

Splunk Observability Cloudでトレースデータを確認する前に、
以下のコマンドでエージェントCollectorのログをtailして、debug exporterがキャプチャした内容を確認しましょう：

``` bash
kubectl logs -l component=otel-collector-agent -f
```

ヒント：`CTRL+C` を使用してログのtailを停止します。

エージェントCollectorのログに以下のようなトレースが書き込まれているはずです：

````
InstrumentationScope opentelemetry.instrumentation.flask 0.44b0
Span #0
    Trace ID       : 9f9fc109903f25ba57bea9b075aa4833
    Parent ID      : 
    ID             : 6d71519f454f6059
    Name           : /check
    Kind           : Server
    Start time     : 2024-12-23 19:55:25.815891965 +0000 UTC
    End time       : 2024-12-23 19:55:27.824664949 +0000 UTC
    Status code    : Unset
    Status message : 
Attributes:
     -> http.method: Str(GET)
     -> http.server_name: Str(waitress.invalid)
     -> http.scheme: Str(http)
     -> net.host.port: Int(8888)
     -> http.host: Str(creditcheckservice:8888)
     -> http.target: Str(/check?customernum=30134241)
     -> net.peer.ip: Str(10.42.0.19)
     -> http.user_agent: Str(python-requests/2.31.0)
     -> net.peer.port: Str(47248)
     -> http.flavor: Str(1.1)
     -> http.route: Str(/check)
     -> customer.num: Str(30134241)
     -> credit.score: Int(443)
     -> credit.score.category: Str(poor)
     -> credit.check.result: Str(OK)
     -> http.status_code: Int(200)
````

トレースに、コードでキャプチャした `credit.score` や `credit.score.category` などの
タグ（属性とも呼ばれる）が含まれていることに注目してください。次のセクションで、
Splunk Observability Cloudでトレースを分析してパフォーマンス問題の根本原因を見つける際に、これらを使用します。
