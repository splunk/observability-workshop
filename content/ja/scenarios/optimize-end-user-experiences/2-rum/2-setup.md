---
title: ブラウザアプリでの RUM 計装
linkTitle:  2. RUM 計装
weight: 2
---

* ブラウザで Online Boutique ウェブページの HEAD セクションを確認します
* RUM を計装するコードを見つけます

---

## 1. Online Boutique にアクセスする

ワークショップの講師が、RUM がインストールされた Online Boutique の URL を提供します。次のステップを完了するために使用してください。

## 2. HTML ソースの確認

RUM に必要な変更は、ホストの Web ページの `<head>` セクションに配置されます。右クリックしてページソースを表示するか、コードを検査してください。以下は RUM が設定された `<head>` セクションの例です

![Online Boutique](../images/rum-inst.png)

このコードは、ユーザーワークフローのコンテキストでパフォーマンスをより深く理解するために、RUM Tracing、[Session Replay](https://docs.splunk.com/observability/en/rum/rum-session-replay.html)、および [Custom Events](https://docs.splunk.com/observability/en/rum/RUM-custom-events.html) を有効にします

* 最初の部分は、Splunk Open Telemetry Javascript ファイルのダウンロード元を指定します`https://cdn.signalfx.com/o11y-gdi-rum/latest/splunk-otel-web.js`（必要に応じてローカルにホストすることも可能です）。
* 次のセクションでは、beacon url でトレースの送信先を定義します`{beaconUrl: "https://rum-ingest.eu0.signalfx.com/v1/rum"`
* RUM Access Token`rumAuth: "<redacted>"`
* SPLUNK RUM UI で識別するための `app` と `environment` の識別タグ。例`app: "online-boutique-us-store", environment: "online-boutique-us"}`（これらの値はワークショップによって異なります）

上記の 21 行目と 23〜30 行目が、ウェブサイトで RUM を有効にするために必要なすべてです！

22 行目と 31〜34 行目は、Session Replay を計装する場合のオプションです。

36〜39 行目の `var tracer=Provider.getTracer('appModuleLoader');` は、ページ遷移ごとに Custom Event を追加し、ウェブサイトのコンバージョンと使用状況をより適切に追跡できるようにします。このワークショップでは計装されている場合とされていない場合があります。

{{% notice title="演習" style="green" icon="running" %}}
ショッピングの時間です！ワークショップのストア URL をお好きなだけ多くのブラウザやデバイスで開き、商品を閲覧し、カートに追加し、チェックアウトしてください。終わったらショッピング用のブラウザを閉じてかまいません。これは軽量なデモショップサイトですので、カートの内容が選んだ商品と一致しなくても心配しないでください！
{{% /notice %}}
