---
title: APM Service Map
linkTitle: 1. APM Service Map
weight: 1
---

![apm map](../../images/zero-config-first-services-map.png)

上記のマップは、すべてのサービス間のインタラクションを示しています。PetClinic Microservice アプリケーションが起動して完全に同期されるまで数分かかるため、マップはまだ中間状態である可能性があります。**-2m** と入力して時間フィルターをカスタム時間 **2 minutes** に短縮すると見やすくなります。画面右上の **Refresh** ボタン **(1)** をクリックしてください。赤い円で示される起動時の初期エラーは、最終的に消えていきます。

次に、request, error, and duration (RED) メトリクスダッシュボードを確認することで、計装された各サービスで利用可能なメトリクスを調べてみましょう。

この演習では、サービスのオペレーションで高いレイテンシやエラーが発生している場合に使用する一般的なシナリオを使用します。

Dependency map で **customers-service** をクリックし、**Services** ドロップダウンボックス **(1)** で `customers-service` が選択されていることを確認します。次に、Service 名の隣にある Operations ドロップダウン **(2)** から `GET /owners` を選択します。

これにより、以下に示すように `GET /owners` でフィルタリングされたワークフローが表示されます。

![select a trace](../../images/select-workflow.png)
