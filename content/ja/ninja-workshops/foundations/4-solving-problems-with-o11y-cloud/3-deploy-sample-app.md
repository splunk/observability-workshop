---
title: サンプルアプリケーションのデプロイと OpenTelemetry による計装
linkTitle: 3. サンプルアプリケーションのデプロイと OpenTelemetry による計装
weight: 3
time: 15 minutes
---

ここまでで、K8s クラスターに OpenTelemetry Collector をデプロイし、インフラストラクチャメトリクスの収集に成功しました。

次のステップは、サンプルアプリケーションをデプロイし、OpenTelemetry で計装してトレースをキャプチャすることです。

Python で書かれたマイクロサービスベースのアプリケーションを使用します。ワークショップをシンプルにするため、credit check サービスと credit processor サービスの2つのサービスに焦点を当てます。

## アプリケーションのデプロイ

時間を節約するため、両方のサービスの Docker イメージはすでにビルド済みで、Docker Hub で利用可能です。以下のコマンドで K8s クラスターに credit check サービスをデプロイできます。

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

次に、credit processor サービスをデプロイします。

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

最後に、トラフィックを生成するためのロードジェネレーターをデプロイします。

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

## アプリケーションの確認

このセクションでは、アプリケーションの概要を説明します。アプリケーションの完全なソースコードを確認したい場合は、[GitHub の Observability Workshop リポジトリ](https://github.com/splunk/observability-workshop/tree/main/workshop/tagging)を参照してください。

### OpenTelemetry による計装

credit check サービスと credit processor サービスのビルドに使用された Dockerfile を確認すると、すでに OpenTelemetry で計装されていることがわかります。例として、`/home/splunk/workshop/tagging/creditcheckservice-py-with-tags/Dockerfile` を見てみましょう。

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

`opentelemetry-bootstrap` が含まれており、アプリケーションで使用されるサポート対象パッケージの OpenTelemetry 計装をインストールしていることがわかります。また、アプリケーションの起動コマンドの一部として `opentelemetry-instrument` が使用されていることも確認できます。

`/home/splunk/workshop/tagging/creditcheckservice-py-with-tags/requirements.txt` ファイルを確認すると、パッケージリストに `splunk-opentelemetry[all]` が含まれていることがわかります。

最後に、このサービスのデプロイに使用した Kubernetes マニフェスト（`/home/splunk/workshop/tagging/creditcheckservice-py-with-tags/creditcheckservice-dockerhub.yaml`）を確認すると、OTLP データのエクスポート先を OpenTelemetry に伝えるための環境変数がコンテナに設定されていることがわかります。

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

これだけで、サービスに OpenTelemetry を計装できます。

### アプリケーションの確認

アプリケーションでいくつかのカスタムタグをキャプチャしており、これについてはすぐに確認します。その前に、タグの概念とその重要性について紹介しましょう。

### タグとは

タグは、トレース内のスパンに関する追加のメタデータを提供するキーと値のペアで、**Splunk APM** に送信するスパンのコンテキストを充実させることができます。

例えば、決済処理アプリケーションでは、以下を追跡できると便利です。

* 使用された決済タイプ（クレジットカード、ギフトカードなど）
* 決済をリクエストした顧客の ID

これにより、決済処理中にエラーやパフォーマンスの問題が発生した場合に、トラブルシューティングに必要なコンテキストを得ることができます。

一部のタグは OpenTelemetry Collector で追加できますが、このワークショップで扱うタグはより詳細なもので、OpenTelemetry SDK を使用してアプリケーション開発者が追加します。

### なぜタグはそれほど重要なのか

タグは、アプリケーションが真にオブザーバブルであるために不可欠です。タグはトレースにコンテキストを追加し、なぜ一部のユーザーは良い体験を得られ、他のユーザーはそうでないのかを理解するのに役立ちます。また、**Splunk Observability Cloud** の強力な機能はタグを活用して、根本原因にすばやくたどり着くことができます。

> 先に進む前に、用語についての注意事項です。このワークショップでは **tags** について説明しており、これは **Splunk Observability Cloud** で使用される用語ですが、OpenTelemetry では代わりに **attributes** という用語を使用します。そのため、このワークショップ全体でタグに言及している箇所は、attributes と同義として扱ってください。

### タグのキャプチャ方法

Python アプリケーションでタグをキャプチャするには、まず `/home/splunk/workshop/tagging/creditcheckservice-py-with-tags/main.py` ファイルの先頭に import 文を追加して trace モジュールをインポートします。

```` python
import requests
from flask import Flask, request
from waitress import serve
from opentelemetry import trace  # <--- ADDED BY WORKSHOP
...
````

次に、現在のスパンへの参照を取得して、属性（タグ）を追加できるようにします。

```` python
def credit_check():
    current_span = trace.get_current_span()  # <--- ADDED BY WORKSHOP
    customerNum = request.args.get('customernum')
    current_span.set_attribute("customer.num", customerNum)  # <--- ADDED BY WORKSHOP
...
````

とても簡単ですね。credit check サービスでは合計4つのタグをキャプチャしており、最終的な結果は以下のようになります。

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

Splunk Observability Cloud でトレースデータを確認する前に、以下のコマンドでエージェント Collector のログを tail して、debug exporter がキャプチャした内容を確認しましょう。

``` bash
kubectl logs -l component=otel-collector-agent -f
```

ヒント: ログの tail を停止するには `CTRL+C` を使用します。

エージェント Collector のログに、以下のようなトレースが書き込まれていることが確認できます。

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

トレースに、コード内でキャプチャしたタグ（属性）が含まれていることに注目してください。例えば `credit.score` や `credit.score.category` などです。次のセクションでは、Splunk Observability Cloud でトレースを分析してパフォーマンス問題の根本原因を特定する際に、これらのタグを使用します。
