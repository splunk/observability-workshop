---
title: Tag Spotlight
linkTitle: Tag Spotlight
weight: 4
isCJKLanguage: true
---

## タグスポットライト

画面の右側にある **Tag Spotlight** をスクロールダウンし、ドロップダウンから **Top Across All Indexed Tags** を選択します。選択したら、下のスクリーンショットにあるように ![full_screen button](../../images/full_screen.png) をクリックします。

![Tag Spotlight](../../images/tag-spotlight.png)

タグスポットライトのページが表示されます。このページでは、アプリケーションの上位のタグと、それに対応するエラー率や秒間リクエスト数を確認できます。

**version** スパンタグでは、バージョン `350.10` のエラー率が100%であることがわかります。また、**tenant.level** スパンタグでは、3つのテナント（Gold、Silver、Bronze）すべてにエラーがあることがわかります。

![Tag Spotlight Dashboard](../../images/tag-spotlight-dashboard.png)

タグスポットライトのページはインタラクティブに、目的のタグをクリックするだけでフィルタとしてタグを追加することができます。**tenant.level** の下の **gold** をクリックして、フィルターとして追加します。これを行うと、ページには **tenant.level** が **gold** のデータのみが表示されます。

![Gold Tenant](../../images/gold-tenant.png)

タグスポットライトは、データを分析して傾向を見極めるのに非常に便利です。Gold Tenantでは、リクエストの総数のうち55件がエラーであることがわかります。（この数字はワークショップの実施時刻により異なります）

これをバージョンタグと関連付けると、バージョン `350.10` が55件、バージョン `350.9` が17件のリクエストに対応していることがわかります。つまり、バージョン `350.10` を経由したリクエストは、すべてエラー状態になったということになります。

**paymentservice** のバージョン `350.10` からのすべてのリクエストがエラーになるというこの理論をさらに検証するために、タグセレクタを使用して、フィルタを別のテナントに変更することができます。フィルターを **gold** テナントから **silver** テナントに変更します。

![Silver Tag Filter](../../images/silver-tag-filter.png)

ここで、**silver** テナントのエラーのあるリクエスト数を見て、バージョン番号と相関させることで、同様の分析を行うことができます。**silver** テナントのエラー数は、バージョン `350.10` のリクエスト数と一致していることに注目してください。

![Silver Tenant](../../images/silver-tenant.png)

タグスポットライトでは、秒間リクエスト数やエラー率だけでなく、サービスごとのレイテンシーも見ることができます。これを行うには、レイテンシーボタンを選択し、silver テナントタグを削除することで、すべての paymentservice のレイテンシーを確認することができます。

![Latency](../../images/latency.png)

右端の **Clear All** の下にある X ボタンを押して、サービスマップに戻りましょう。

右上にある「Services by Error Rate」グラフのピンク色の線上をクリックします。選択すると、サンプルトレースのリストが表示されます。`Initiating Operation of`が **frontend: POST /cart/checkout** であるサンプルトレースの1つをクリックしてください。
