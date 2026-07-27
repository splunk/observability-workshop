---
title: 3. Splunk APM で確認する
weight: 3
---

## Splunk APM を確認する

{{% notice title="演習" style="green" icon="running" %}}

1. Splunk Observability Cloud で **APM** に移動します。
2. サービス名 `warmup-app` でフィルタリングします。
3. `/hello` エンドポイントのトレースが表示されるはずです。
**注意: 最初のトレースが取り込まれるまで数分かかる場合があります**

{{% /notice %}}

## 何が起きたのか？

1. Flask アプリは「素のまま」で、オブザーバビリティのコードは一切含まれていません。hello を返すことと heartbeat メトリクスを送信することしかできません。
2. OBI はカーネルのネットワークスタックに eBPF プローブをアタッチし、アプリのプロセスを流れる HTTP トラフィックを観測しました。
3. OBI は OpenTelemetry 互換のトレーススパンを生成し、Splunk に直接送信しました。

**SDK なし、コード変更なし、再起動なしで、カーネルから実行中のプロセスに分散トレーシングを追加しました。**

これは Phase 1 と Phase 2 で使用するのと同じ技術ですが、ベアプロセスではなく Docker コンテナ内で使用します。

## Phase 0 のクリーンアップ

次に進む前に、Python アプリと OBI を停止します:

``` bash
kill %1 2>/dev/null
sudo pkill -f ./obi 2>/dev/null
deactivate
```
