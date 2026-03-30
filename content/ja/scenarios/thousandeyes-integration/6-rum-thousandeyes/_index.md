---
title: ThousandEyes と Splunk RUM
linkTitle: 6. RUM
weight: 6
time: 10 minutes
description: ThousandEyes のネットワークメトリクスと Splunk RUM を関連付けて、エンドユーザー体験とネットワークの問題を一緒に調査できるようにします。
---
ThousandEyesとSplunk RUMを統合して、ネットワークの問題がエンドユーザーの問題と関連しているかどうかを把握します。

## 前提条件

1. Splunk Observability CloudとThousandEyes両方の管理者権限
1. Splunk RUMにデータを送信しているアプリケーションが少なくとも1つ
1. Splunk RUMのアプリと**同じドメイン**で、ThousandEyesで以下のタイプのテストが少なくとも1つ実行されていること：
    - [agent-to-server](https://docs.thousandeyes.com/product-documentation/tests/network-tests#agent-to-server-tests)
    - [HTTP server](https://docs.thousandeyes.com/product-documentation/tests/http-server-tests)
    - [page load](https://docs.thousandeyes.com/product-documentation/tests/web-layer-tests#page-load-test)
    - [transaction](https://docs.thousandeyes.com/product-documentation/tests/web-layer-tests#transaction-test)

## 統合手順

1. ThousandEyesでOAuth Bearerトークンを作成します：
    - 右上隅のユーザー名を選択し、`Profile` を選択します。
    - User API Tokensの下で `Create` を選択してOAuth Bearer Tokenを生成します。
    - Observability Cloudのデータ統合ウィザードで使用するため、トークンをコピーまたはメモしておきます。
1. Splunk Observability Cloudで、Data Management > Available Integrations > ThousandEyes Integration with RUMを開きます。
    - [前回の Splunk 統合](/observability-workshop/en/scenarios/thousandeyes-integration/3-splunk-integration/index.html#step-1-create-a-splunk-observability-cloud-access-token)で使用したものと同じ `Ingest` トークンを使用するか、RUM統合のデータ使用量をより適切に追跡するために専用の `Ingest` トークンを作成して選択します。
    - ThousandEyesからのOAuth Bearerトークンを入力します。
    - テストのマッチングを確認し、必要に応じて選択を変更し、推定データ取り込み量を確認してから `Done` を選択します。

## 統合の確認

ThousandEyesテストが実行されているRUMアプリケーションに移動し、Mapを表示します。
ThousandEyesテストも実行されているロケーションにカーソルを合わせると、ThousandEyesメトリクスのプレビューが表示されます：
![Splunk RUM の地図表示、ThousandEyes からのネットワークレイテンシが表示されている](../images/rum-thousandeyes-map-preview.png)

ThousandEyesでアクティブなアラートがある場合、RUMの該当するロケーションのバブル上にThousandEyesアイコンが表示されます：
![Splunk RUM の地図表示](../images/rum-thousandeyes-map.png)

該当するリージョンをクリックすると、RUMの他のメトリクスと一緒にネットワークメトリクスが表示されます。`View ThousandEyes Tests` を開いてThousandEyesの関連テストに移動できます：
![RUM メトリクスと ThousandEyes メトリクス、Tests ダイアログが開いた状態](../images/rum-thousandeyes-tests-dialog.png)

## カスタムダッシュボードで RUM と ThousandEyes のメトリクスを表示する

これで、関連するThousandEyesテストからのシグナルと他のObservability CloudのKPIを関連付けることができます！

1. Dashboards > "RUM" で検索 > `RUM applications` グループ内のすぐに使えるRUMダッシュボードの1つをクリックします。
1. 興味のあるRUM KPIのチャートをコピーするか、右上のダッシュボードのアクションメニューを開いて `Save As` で自分のダッシュボードグループにコピーを作成します。
1. 新しいダッシュボードで、シグナル `network.latency` を使用して新しいチャートを作成します。
    - extrapolation policyを `Last value` に変更します。
    - 測定単位をTime > `Millisecond` に変更します。
    - Chart Optionsで、`Show on-chart legend` を選択し、値を `thousandeyes.source.agent.name` にします。これにより、ThousandEyesのエージェントロケーション別にチャートが分割されます。
1. 新しいチャートに名前を付けて保存し、それをコピーして `network.jitter` と `network.loss` の類似チャートを作成します。コピーしたチャートのシグナルでメトリクスを変更し、必要に応じて測定単位と可視化オプションを調整します。

カスタムダッシュボードとチャートの作成に関する詳細なガイダンスは、[Dashboard Workshop](/en/ninja-workshops/7-dashboards-detectors/) を参照してください。

{{% notice title="ヒント" style="primary"  icon="lightbulb" %}}
ThousandEyesのテストメトリクスと並べて表示すると便利なObservability Cloudの他のメトリクスについて考えてみてください。

例えば、SyntheticsでAPIテストを実行している場合は、ロケーション別のAPIテスト成功率のヒートマップを追加することを検討してください。

  {{% /notice %}}
