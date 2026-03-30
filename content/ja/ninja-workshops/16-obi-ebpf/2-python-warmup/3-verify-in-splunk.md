---
title: 3. Splunk APM で確認する
weight: 3
---

## Splunk APM を確認する

{{% notice title="演習" style="green" icon="running" %}}

1. Splunk Observability Cloudの **APM** に移動します。
2. サービス名 `warmup-app` でフィルタリングします。
3. `/hello` エンドポイントのトレースが表示されます。
**注意: 最初のトレースが取り込まれるまで数分かかる場合があります**

{{% /notice %}}

## 何が起きたのか？

1. Flaskアプリは「素の状態」です。オブザーバビリティのコードは一切含まれていません。helloを返すことと、ハートビートメトリクスを送信する機能しかありません。
2. OBIはカーネルのネットワークスタックにeBPFプローブをアタッチし、アプリのプロセスを流れるHTTPトラフィックを監視しました。
3. OBIはOpenTelemetry互換のトレーススパンを生成し、Splunkに直接送信しました。

**カーネルから実行中のプロセスに分散トレーシングを追加しました。SDK も、コード変更も、再起動も不要です。**

これはPhase 1とPhase 2で使用するのと同じ技術ですが、ベアプロセスではなくDockerコンテナ内で動作します。

## Phase 0 のクリーンアップ

次に進む前に、PythonアプリとOBIを停止します:

``` bash
kill %1 2>/dev/null
sudo pkill -f ./obi 2>/dev/null
deactivate
```
