---
title: 3. ログタイムラインチャート
weight: 3
---

Log Observerで特定のビューを持った後、そのビューをダッシュボードで使用できると、将来的に問題の検出や解決にかかる時間を短縮するのに非常に役立ちます。ワークショップの一環として、これらのチャートを使用する例示的なカスタムダッシュボードを作成します。

**ログタイムライン**チャートの作成を見ていきましょう。ログタイムラインチャートは、時間経過に伴うログメッセージを視覚化するために使用されます。ログメッセージの頻度を確認し、パターンを特定するための優れた方法です。また、環境全体でのログメッセージの分布を確認するための素晴らしい方法でもあります。これらのチャートはカスタムダッシュボードに保存できます。

{{% notice title="情報" style="green" title="演習" icon="running" %}}

まず、関心のある列のみに情報量を減らします：

- **ログテーブル**の上にあるテーブル設定{{% icon icon="cog" %}}アイコンをクリックして**Table Setting**を開き、`_raw` のチェックを外し、次のフィールドが選択されていることを確認します：`k8s.pod.name`、`message`、`version`。
  ![ログテーブル設定](../images/log-observer-table.png)
- 時間選択から固定時間を削除し、**過去 15 分**に設定します。
- すべてのトレースでこれを機能させるには、フィルターから `trace_id` を削除し、フィールド `sf_service=paymentservice` と `sf_environment=[WORKSHOPNAME]` を追加します。
- **Save**をクリックし、**Save to Dashboard**を選択します。
  ![保存する](../images/save-query.png)
- 表示されるチャート作成ダイアログボックスで、**Chart name**として `ログタイムライン` を使用します。
- {{% button style="blue" %}}Select Dashboard{{% /button %}}をクリックし、ダッシュボード選択ダイアログボックスで{{% button style="blue" %}}New Dashboard{{% /button %}}をクリックします。
- **New Dashboard**ダイアログボックスに、新しいダッシュボードの名前を入力します（説明を入力する必要はありません）。次の形式を使用します：`イニシャル - サービスヘルスダッシュボード`、そして{{% button style="blue" %}}Save{{% /button %}}をクリックします。
- リスト内で新しいダッシュボードが強調表示されていることを確認し（**1**）、{{% button style="blue" %}}OK{{% /button %}}（**2**）をクリックします。
  ![ダッシュボードの保存](../images/dashboard-save.png)
- **Chart Type**として**Log timeline**が選択されていることを確認します。
  ![ログタイムライン](../images/log-timeline.png?classes=left&width=25vw)
- {{% button %}}Save{{% /button %}}ボタンをクリックします（この時点では**Save and go to dashboard**をクリック**しないで**ください）。

{{% /notice %}}

次に、**ログビュー**チャートを作成します。
