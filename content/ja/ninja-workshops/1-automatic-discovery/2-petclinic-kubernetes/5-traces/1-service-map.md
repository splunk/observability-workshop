---
title: APM Service Map
linkTitle: 1. APM Service Map
weight: 1
---

![apm map](../../images/zero-config-first-services-map.png)

上記のマップは、すべてのサービス間のすべての相互作用を示しています。PetClinic Microserviceアプリケーションが起動して完全に同期するまで数分かかるため、マップはまだ中間状態にある可能性があります。時間フィルタを**-2m**と入力してカスタム時間の**2分**に減らすと役立ちます。画面右上の**Refresh**ボタン**(1)**をクリックできます。赤い円で示される初期起動関連のエラーは最終的に消えます。

次に、各サービスで利用可能なメトリクスを調べるために、リクエスト、エラー、期間（RED）メトリクスダッシュボードを見てみましょう。

この演習では、サービスオペレーションが高いレイテンシやエラーを示している場合に使用する一般的なシナリオを使用します。

依存関係マップで**customers-service**をクリックし、**Services**ドロップダウンボックス**(1)**で`customers-service`が選択されていることを確認します。次に、サービス名に隣接するOperationsドロップダウン**(2)**から`GET /owners`を選択します。

これにより、以下に示すように`GET /owners`でフィルタリングされたワークフローが表示されます：

![select a trace](../../images/select-workflow.png)
