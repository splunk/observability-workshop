---
title: 2.1 Service Map
linkTitle: 2.1 Service Map
weight: 2
---

## Service Map

サービスマップで **paymentservice** をクリックし、**paymentservice** の下にある `breakdown` ドロップダウンフィルターから **version** を選択します。これにより、カスタムスパンタグ **version** でサービスマップがフィルタリングされます。

以下のスクリーンショットのように、サービスマップが更新され、**paymentservice** の異なるバージョンが表示されます。

Splunk Observability は、paymentservice でエラーが発生していること（リクエストレートとエラーレートを確認できます）だけでなく、このサービスが根本原因であることも示しています。

これは、サービスで分散トレーシングが有効になると、AI ディレクテッドトリアージ機能により自動的に行われます。このように表示されるために、閾値の設定などは一切必要ありません。

これは、お客様がより迅速に問題を検出し、エラーの発生箇所を特定できるようにすることで、MTTD と MTTR の削減に貢献する一例です。

![Payment Service](../../images/paymentservice.png)
