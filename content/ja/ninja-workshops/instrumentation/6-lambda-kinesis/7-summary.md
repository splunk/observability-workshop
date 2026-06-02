---
title: まとめ
linkTitle: 7. まとめ
weight: 7
---

Lambda Tracing Workshop の完了、おめでとうございます！自動計装を手動の手順で補完することで、`producer-lambda` 関数のコンテキストを Kinesis ストリームのレコード経由で `consumer-lambda` 関数に送信する方法を確認しました。これにより、期待どおりの分散トレースを構築し、Splunk APM 上で両関数間の関係を文脈づけることができました。

![Lambda application, fully instrumented](../images/13-Architecture_Instrumented.png)

これで、2 つの異なる関数を連携させて、手動でトレースを構築できるようになりました。この手法は、自動計装やサードパーティ製システムがコンテキスト伝播を標準でサポートしていない場合や、より関連性の高いトレース分析のためにトレースへカスタム属性を追加したい場合に役立ちます。
