---
title: トレースデータの探索
linkTitle: 4. トレースデータの探索
weight: 4
time: 5 minutes
---

アプリケーションからいくつかのタグをキャプチャできたので、この追加コンテキストを含むトレースデータを探索し、一部のケースでユーザーエクスペリエンスが低下している原因を特定できるか確認しましょう。

## Trace Analyzer の使用

**APM -> Trace Analyzer** に移動します。**Trace Analyzer** では、フィルターを追加して目的のトレースを検索できます。たとえば、credit score が `7` で始まるトレースをフィルタリングできます。

![Credit Check Starts with Seven](../images/credit_score_starts_with_seven.png)

これらのトレースの1つを読み込むと、credit score が確かに7で始まっていることがわかります。

customer number、credit score category、credit score result についても同様のフィルターを適用できます。

## エラーのあるトレースの探索

credit score フィルターを削除し、**Errors only** を `on` に切り替えると、エラーが発生したトレースのみが一覧表示されます。

![Traces with Errors Only](../images/traces_errors_only.png)

これらのトレースをいくつかクリックして、キャプチャしたタグを確認してみてください。何かパターンに気づきますか？

次に、**Errors only** を `off` に切り替え、トレースを duration でソートします。最も実行時間の長いトレースをいくつか確認し、最も実行時間の短いトレースと比較してみてください。何かパターンに気づきますか？

パフォーマンスの低下やエラーの原因を説明するパターンを見つけられたなら、素晴らしいです！ただし、この方法でのトラブルシューティングは困難であることに留意してください。多くのトレースを確認し、確認した内容を頭の中で追跡してパターンを特定する必要があるためです。

幸いなことに、**Splunk Observability Cloud** にはこれをより効率的に行う方法が用意されています。次のセクションで詳しく見ていきましょう。
