---
title: 3. Splunk APM での確認
weight: 3
---

## Splunk APM の確認

{{% notice title="演習" style="green" icon="running" %}}

1. Splunk Observability Cloud で **APM** に移動します。
2. サービス名 `warmup-app` でフィルタリングします。
3. `/hello` エンドポイントのトレースが表示されているはずです。
**注意: 最初のトレースが取り込まれるまで数分かかる場合があります**

{{% /notice %}}

## 何が起こったのか?

1. Flask アプリは「裸」の状態で、オブザーバビリティのコードはまったく含まれていません。hello を返すこととハートビートメトリクスを送信することしかできません。
2. OBI はカーネルのネットワーキングスタックに eBPF プローブをアタッチし、アプリのプロセスを通過する HTTP トラフィックを観察しました。
3. OBI は OpenTelemetry 互換のトレーススパンを生成し、Splunk に直接送信しました。

**カーネルから実行中のプロセスに分散トレーシングを追加したことになります。SDK もコード変更も再起動も不要です。**

これは Phase 1 と 2 で使用するのと同じテクノロジーですが、ベアプロセスではなく Docker コンテナ内で動作します。

## Phase 0 のクリーンアップ

次に進む前に、Python アプリと OBI を停止します。

``` bash
kill %1 2>/dev/null
sudo pkill -f ./obi 2>/dev/null
deactivate
```
