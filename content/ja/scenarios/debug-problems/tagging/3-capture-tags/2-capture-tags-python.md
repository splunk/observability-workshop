---
title: 2. タグのキャプチャ - Python
weight: 2
time: 15 minutes
---

トレースにタグを追加して、一部の顧客がアプリケーションで悪い体験を受ける理由を特定しましょう。

## 有用なタグの特定

まず、`creditcheckservice` の `credit_check` 関数のコードを確認します（`/home/splunk/workshop/tagging/creditcheckservice-py/main.py` ファイルにあります）。

```` python
@app.route('/check')
def credit_check():
    customerNum = request.args.get('customernum')

    # Get Credit Score
    creditScoreReq = requests.get("http://creditprocessorservice:8899/getScore", params={"customernum": customerNum})
    creditScoreReq.raise_for_status()
    creditScore = int(creditScoreReq.text)

    creditScoreCategory = getCreditCategoryFromScore(creditScore)

    # Run Credit Check
    creditCheckReq = requests.get("http://creditprocessorservice:8899/runCreditCheck", params={"customernum": customerNum, "score": creditScore})
    creditCheckReq.raise_for_status()
    checkResult = str(creditCheckReq.text)

    return checkResult
````

この関数は入力として **顧客番号** を受け取ることがわかります。これをトレースの一部としてキャプチャすると役立ちます。他に何が役立つでしょうか？

`creditprocessorservice` から返されるこの顧客の **クレジットスコア** も興味深いかもしれません（ただし、PII データをキャプチャしないように注意が必要です）。また、 **クレジットスコアカテゴリ** と **クレジットチェック結果** をキャプチャするのも有用です。

このサービスから調査に役立つ4つのタグを特定しました。では、これらをどのようにキャプチャすればよいでしょうか？

## タグのキャプチャ

まず、`creditcheckservice-py/main.py` ファイルの先頭にimport文を追加して、traceモジュールをインポートします。

```` python
import requests
from flask import Flask, request
from waitress import serve
from opentelemetry import trace  # <--- ADDED BY WORKSHOP
...
````

次に、現在のSpanへの参照を取得して、属性（タグ）を追加できるようにします。

```` python
def credit_check():
    current_span = trace.get_current_span()  # <--- ADDED BY WORKSHOP
    customerNum = request.args.get('customernum')
    current_span.set_attribute("customer.num", customerNum)  # <--- ADDED BY WORKSHOP
...
````

簡単でしたね。さらにキャプチャを追加して、最終結果は以下のようになります。

```` python
def credit_check():
    current_span = trace.get_current_span()  # <--- ADDED BY WORKSHOP
    customerNum = request.args.get('customernum')
    current_span.set_attribute("customer.num", customerNum)  # <--- ADDED BY WORKSHOP

    # Get Credit Score
    creditScoreReq = requests.get("http://creditprocessorservice:8899/getScore", params={"customernum": customerNum})
    creditScoreReq.raise_for_status()
    creditScore = int(creditScoreReq.text)
    current_span.set_attribute("credit.score", creditScore)  # <--- ADDED BY WORKSHOP

    creditScoreCategory = getCreditCategoryFromScore(creditScore)
    current_span.set_attribute("credit.score.category", creditScoreCategory)  # <--- ADDED BY WORKSHOP

    # Run Credit Check
    creditCheckReq = requests.get("http://creditprocessorservice:8899/runCreditCheck", params={"customernum": customerNum, "score": creditScore})
    creditCheckReq.raise_for_status()
    checkResult = str(creditCheckReq.text)
    current_span.set_attribute("credit.check.result", checkResult)  # <--- ADDED BY WORKSHOP

    return checkResult
````

## サービスの再デプロイ

これらの変更が完了したら、以下のスクリプトを実行して `creditcheckservice` 用のDockerイメージを再ビルドし、Kubernetesクラスターに再デプロイします。

```` bash
./5-redeploy-creditcheckservice.sh
````

## タグが正常にキャプチャされたことの確認

数分後、 **Splunk Observability Cloud** に戻り、最新のトレースの1つを読み込んで、タグが正常にキャプチャされたことを確認します（ヒント: タイムスタンプでソートして最新のトレースを見つけます）。

**![Trace with Attributes](../../images/trace_with_attributes.png)**

お疲れ様でした。OpenTelemetryのスキルがレベルアップし、タグを使用してトレースにコンテキストを追加できるようになりました。

次に、これらのタグを **Splunk Observability Cloud** でどのように活用できるかを見ていきましょう！
