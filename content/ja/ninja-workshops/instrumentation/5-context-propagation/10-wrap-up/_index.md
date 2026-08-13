---
title: まとめ
linkTitle: まとめ
weight: 10
time: 5 minutes

---

## サマリー

このワークショップでは、Splunk RUMから注文 → 決済 → フルフィルメントパイプラインを通る単一のチェックアウトをトレースし、Traceが途切れやすい3つの箇所で相関関係を復元しました。

1つ目は、エッジのNGINXゲートウェイです。明示的なproxy_set_headerルールがリクエストを転送していましたが、W3C Trace Contextは転送していませんでした。そこで、proxy_set_header traceparent $http_traceparent（およびtracestateとbaggage）を追加して、リバースプロキシを通じてヘッダーを渡すようにしました。

2つ目は、決済ゲートウェイです。計装済みのNode.jsプロキシがチェーンを切断していました。これは、送信HTTPコールがコンテキストを伝播していなかったためです。典型的なBFF/プロキシのバグであり、アプリケーションコードでpropagation.inject()を使用し、上流のfetchからsuppressTracing()を削除することで修正しました。

3つ目は、RabbitMQ間の通信です。ブローカー自体はTrace Contextを運びません。非同期ハンドオフが失敗したのは、プロデューサーがW3CヘッダーをAMQPメッセージプロパティに注入せず、コンシューマーがそれを抽出していなかったためです。そこで、パブリッシュ時のinjectとコンシューム時のextractを実装しました（これはOTelメッセージング計装が他のスタックで自動化しているのと同じ規約です）。

これらの修正により、ブラウザ/RUM Span、プロキシやアプリケーション層ゲートウェイを経由する同期HTTPホップ、および非同期フルフィルメント処理が1つのTraceに再接続され、Splunk APMでエンドツーエンドに追跡できるようになります。

{{% notice title="お疲れ様でした" style="info" %}}
おめでとうございます。プロキシとメッセージバスを横断するフルスタックオブザーバビリティを復元できました！
{{% /notice %}}

## クリーンアップ

ローカルのワークショップリソース（k3dクラスター、Splunk Collector、アプリケーションワークロード、ローカルイメージ）をすべて削除します。

プロジェクトルート [~/workshop/context-propagation] から以下を実行します。

```bash
make cleanup
```
