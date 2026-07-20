---
title: 3. Splunk APMで確認する
weight: 3
---

## Splunk APMの確認

{{% notice title="演習" style="green" icon="running" %}}

1. Splunk Observability Cloudで **APM** に移動します。
2. サービス名 `warmup-app` でフィルタリングします。
3. `/hello` エンドポイントのトレースが表示されます。
**注意: 最初のトレースが取り込まれるまで数分かかる場合があります**

{{% /notice %}}

## 何が起きたのか？

1. Flaskアプリは「素の状態」で、オブザーバビリティのコードは一切含まれていません。helloを返すことと、ハートビートメトリクスを送信することだけを行います。
2. OBIがカーネルのネットワークスタックにeBPFプローブをアタッチし、アプリのプロセスを流れるHTTPトラフィックを観測しました。
3. OBIがOpenTelemetry互換のトレースSpanを生成し、Splunkに直接送信しました。

**SDKなし、コード変更なし、再起動なしで、カーネルから実行中のプロセスに分散トレーシングを追加しました。**

これはPhase 1および2で使用するのと同じ技術ですが、ベアプロセスではなくDockerコンテナ内で動作します。

## Phase 0のクリーンアップ

次に進む前に、PythonアプリとOBIを停止します

``` bash
kill %1 2>/dev/null
sudo pkill -f ./obi 2>/dev/null
deactivate
```
