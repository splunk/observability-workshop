---
title: サンプルアプリケーションのデプロイと OpenTelemetry によるインストルメンテーション
linkTitle: 3. サンプルアプリケーションのデプロイと OpenTelemetry によるインストルメンテーション
weight: 3
time: 15 minutes
---

ここまでで、K8s クラスターに OpenTelemetry collector をデプロイし、インフラストラクチャメトリクスの収集に成功しています。

次のステップは、サンプルアプリケーションをデプロイし、OpenTelemetry でインストルメントしてトレースをキャプチャすることです。

Python で書かれたマイクロサービスベースのアプリケーションを使用します。ワークショップをシンプルに保つため、credit check service と credit processor service の 2 つのサービスに焦点を当てます。

## アプリケーションのデプロイ

時間を節約するため、これらのサービスの Docker イメージはすでにビルドされており、Docker Hub から利用できます。次のコマンドで K8s クラスターに credit check service をデプロイできます。

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

次に、credit processor service をデプロイしましょう。

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

最後に、トラフィックを生成するロードジェネレーターをデプロイしましょう。

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

## アプリケーションの探索

このセクションではアプリケーションの概要を説明します。アプリケーションの完全なソースコードを確認したい場合は、[GitHub の Observability Workshop リポジトリ](https://github.com/splunk/observability-workshop/tree/main/workshop/tagging) を参照してください。

### OpenTelemetry によるインストルメンテーション

credit check service と credit processor service のビルドに使用されている Dockerfile を見ると、すでに OpenTelemetry でインストルメントされていることがわかります。たとえば、`/home/splunk/workshop/tagging/creditcheckservice-py-with-tags/Dockerfile` を見てみましょう。

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
RUN opentelemetry-bootstrap -a install

# Set the entrypoint command to run the application
CMD ["opentelemetry-instrument", "python3", "main.py"]
```

`opentelemetry-bootstrap` が含まれていることがわかります。これにより、アプリケーションが使用するサポート対象パッケージ向けの OpenTelemetry インストルメンテーションがインストールされます。また、アプリケーションを起動するコマンドの一部として `opentelemetry-instrument` が使用されていることもわかります。

そして `/home/splunk/workshop/tagging/creditcheckservice-py-with-tags/requirements.txt` ファイルを確認すると、パッケージリストに `splunk-opentelemetry[all]` が含まれていることがわかります。

最後に、このサービスをデプロイするために使用した Kubernetes マニフェスト (`/home/splunk/workshop/tagging/creditcheckservice-py-with-tags/creditcheckservice-dockerhub.yaml`) を確認すると、OTLP データのエクスポート先を OpenTelemetry に伝えるために、コンテナ内で環境変数が設定されていることがわかります。

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

OpenTelemetry でサービスをインストルメントするために必要なのは、これだけです！

### アプリケーションの探索

アプリケーションでいくつかのカスタムタグをキャプチャしており、まもなくそれらを探索します。その前に、タグの概念とその重要性について紹介します。

### タグとは何か？

タグは、トレース内のスパンに関する追加のメタデータを提供するキーと値のペアであり、**Splunk APM** に送信するスパンのコンテキストを充実させることができます。

たとえば、決済処理アプリケーションでは、次のような情報を追跡することが有用です。

* 使用された決済タイプ (クレジットカード、ギフトカードなど)
* 決済をリクエストした顧客の ID

このようにすれば、決済処理中にエラーやパフォーマンスの問題が発生した場合でも、トラブルシューティングに必要なコンテキストを得られます。

一部のタグは OpenTelemetry collector で追加できますが、このワークショップで扱うタグはより粒度が細かく、アプリケーション開発者が OpenTelemetry SDK を使用して追加します。

### なぜタグはそれほど重要なのか？

タグは、アプリケーションが真に観測可能であるために不可欠です。タグはトレースにコンテキストを追加し、なぜ一部のユーザーは優れた体験を得て、他のユーザーはそうでないのかを理解するのに役立ちます。そして **Splunk Observability Cloud** の強力な機能はタグを活用して、根本原因に素早くたどり着くことを支援します。

> 先に進む前に用語について一言。このワークショップでは **tags** について説明し、これは **Splunk Observability Cloud** で使用する用語ですが、OpenTelemetry では代わりに **attributes** という用語を使用します。そのため、このワークショップで tags という記述を見かけたら、attributes と同義として扱ってかまいません。

### タグはどのようにキャプチャされるのか？

Python アプリケーションでタグをキャプチャするには、まず `/home/splunk/workshop/tagging/creditcheckservice-py-with-tags/main.py` ファイルの先頭に import 文を追加して、trace モジュールをインポートします。

```` python
import requests
from flask import Flask, request
from waitress import serve
from opentelemetry import trace  # <--- ADDED BY WORKSHOP
...
````

次に、現在のスパンへの参照を取得して、属性 (タグ) を追加できるようにします。

```` python
def credit_check():
    current_span = trace.get_current_span()  # <--- ADDED BY WORKSHOP
    customerNum = request.args.get('customernum')
    current_span.set_attribute("customer.num", customerNum)  # <--- ADDED BY WORKSHOP
...
````

とても簡単でしたよね？ credit check service では合計 4 つのタグをキャプチャしており、最終的な結果は次のようになります。

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

## トレースデータの確認

Splunk Observability Cloud でトレースデータを確認する前に、次のコマンドで agent collector のログを tail して、debug exporter がキャプチャした内容を確認しましょう。

``` bash
kubectl logs -l component=otel-collector-agent -f
```

ヒント: ログの tail を停止するには `CTRL+C` を使用してください。

agent collector のログには、次のようなトレースが書き込まれているのが確認できるはずです。

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

トレースには、`credit.score` や `credit.score.category` のように、コードでキャプチャしたタグ (属性) が含まれていることに注意してください。これらは次のセクションで、Splunk Observability Cloud でトレースを分析してパフォーマンス問題の根本原因を特定するときに使用します。
