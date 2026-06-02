---
title: Kubernetes 監査イベントメトリクスを可視化する
linkTitle: 4.2 Kubernetes 監査イベントメトリクスを可視化する
weight: 3
---

メトリクスにディメンションが追加されたので、イベントの `verb` ディメンションを使って、さまざまな Kubernetes アクションの状態を示すチャートを作成します。

{{% notice title="演習: Kubernetes 監査イベントメトリクスを可視化する" style="green" icon="running" %}}

**1.** 前のセクションで作成したチャートを閉じてしまった場合は、画面右上の **+** アイコン → **Chart** をクリックして新しいチャートを作成します。

![Create New Chart](../../images/create_new_chart.png?width=40vw)

**2.** 新しく作成したチャートの **Plot Editor** で、メトリクス名フィールドに `k8s_audit*` と入力します。ワイルドカードを使うことで、取り込まれているすべてのメトリクスを確認できます。

![Review Metric](../../images/review_metric.png?width=40vw)

**3.** 1 つだったメトリクスが複数に変わっていることに注目してください。これは、ディメンションを含めるようにパイプラインを更新したタイミングで発生したものです。このメトリクスが利用可能になったので、いずれかのアクションにエラーが関連付けられていないかを表示するようにチャートを調整しましょう。

![Metric Timeseries](../../images/metric_timeseries.png?width=40vw)

まず、**response_status** フィールドで利用可能な HTTP レスポンスコードを使って、Kubernetes イベントを成功しなかったものだけにフィルタリングします。レスポンスコードが **409**（競合を示します。例えばすでに存在するリソースを作成しようとした場合など）または **503**（リクエストに対して API が応答しなかったことを示します）であるイベントのみを対象にします。

**4.** チャートのプロットエディターで **Add filter** をクリックし、フィールドに **response_status** を指定して、値として **409.0** と **503.0** を選択します。

次に、**resource**、**action**、**response status** ごとにグループ化されたイベントの合計数を計算する関数をチャートに追加します。これにより、どのアクションと関連リソースでエラーが発生したかを正確に確認できます。これで、成功しなかった Kubernetes イベントのみを参照している状態になります。

**5.** **Add analytics** → **Sum** → **Sum:Aggregation** をクリックし、**Group by** フィールドに **resource**、**action**、**response_status** を追加します。

![Add Metric Filters](../../images/add_metric_filters.png?width=40vw)

**6.** 上部のボタンにあるチャートタイプを使って、チャートを **heatmap** に変更します。**Plot editor** の隣の **Chart options** をクリックします。**Group by** セクションで **response_status** を選択し、次に **action** を選択します。**Color threshold** を **Auto** から **Fixed** に変更します。青い **+ ボタン** をクリックして別のしきい値を追加します。**下向き矢印を Yellow** に、**真ん中を orange** に変更します。**上向き矢印は red のまま** にします。**真ん中のしきい値に 5**、**上のしきい値に 20** を入力します。

![Configure Thresholds](../../images/configure_thresholds.png?width=40vw)

**7.** チャートの右上で青い **Save as...** ![Preview Button](../../images/save_as_btn.png?height=20px&classes=inline) ボタンをクリックします。チャートに名前を入力します（例: Kubernetes Audit Logs - Conflicts and Failures）。

![Chart Name](../../images/chart_name.png)

**8.** **Choose a dashboard** で **New dashboard** を選択します。

![New Dashboard](../../images/new_dashboard.png)

**9.** あとで簡単に見つけられるよう、自分のイニシャルを含むダッシュボード名を入力します。**Save** をクリックします。

![New Dashboard Name](../../images/dashboard_name.png)

**10.** 作成したばかりの新しいダッシュボードが選択されていることを確認し、**Ok** をクリックします。

![Save New Dashboard](../../images/save_new_dashboard.png)

これで、作成したチャートとともに新しい Kubernetes Audit Events ダッシュボードに移動するはずです。Kubernetes クラスター上で動作するアプリケーションのアプリケーションエラーやレスポンスタイムなど、環境内の他のメトリクスからチャートを追加したり、Pod のフェーズや Pod のメモリ使用率などの他の Kubernetes メトリクスを追加したりすることで、クラスターイベントからアプリケーションの健全性に至るまで、Kubernetes 環境を相関的に把握できるビューが得られます。

![Audit Dashboard](../../images/audit_dashboard.png?width=40vw)

チャートのビジュアライゼーションボックスの右上にある三点リーダー `...` を使って、このチャートのコピーを作成します。

![Copy chart button](../../images/copy_chart_button.png?width=40vw)

UI 右上の `+` アイコンを使って、これまで作業していたのと同じダッシュボードに貼り付けます。

![Paste chart into dashboard](../../images/paste_chart_into_dashboard.png?width=40vw)

貼り付けたチャートをクリックし、ビジュアライゼーションを **Column** チャートに変更します。

![Change to column chart visualization](../../images/change_to_column_chart_visualization.png?width=40vw)

SUM を `resource`、`namespace` のみに変更します（フィルターによって、すでに問題のあるコードのみに絞り込まれています）。

![Group chart by resource and namespace](../../images/group_chart_by_resource_and_namespace.png?width=40vw)

Chart options でタイトルを `Kubernetes Audit Logs - Conflicts by Namespace` に変更します。

![Change chart title](../../images/change_chart_title.png?width=40vw)

**Save** をクリックして閉じます。

![Save and close chart](../../images/save_and_close_chart.png)

{{% /notice %}}

{{% notice title="演習: Kubernetes 監査ログに基づくディテクターを作成する" style="green" icon="running" %}}

Conflicts by Namespace チャートで小さなベルアイコンをクリックし、New detector from chart を選択します。

![Bell icon to create detector](../../images/bell_icon_create_detector.png?width=40vw)

名前を選択して **Create alert rule** をクリックします。

![Enter name for alert rule](../../images/enter_name_alert_rule.png?width=40vw)

Alert condition で **Static Threshold** をクリックし、**Alert Settings** へ進みます。

![Select static threshold condition](../../images/select_static_threshold_condition.png?width=40vw)

**Threshold** に `20` を入力します。

![Enter threshold value](../../images/enter_threshold_value.png?width=40vw)

このアラートでは受信者を選択しないので、**Activate** に進み、**Activate Alert Rule** を選択して **Save** します。

![Activate alert rule and save](../../images/activate_alert_rule_and_save.png?width=40vw)

最後に右上の **Save** をもう一度クリックして、ディテクターを保存します。

![Final save for detector](../../images/final_save_detector.png?width=40vw)

ダッシュボードに戻ると、チャートに点灯したベルアイコンで示されたチャートに関連付けられたディテクターが表示されます。

![Detector bell icon on chart](../../images/detector_bell_icon_on_chart.png?width=40vw)

{{% /notice %}}

{{% notice title="演習: Splunk Cloud - Dashboard Studio で時系列データを可視化する" style="green" icon="running" %}}

時系列メトリクスを Splunk Observability Cloud のデータストアに取り込んだので、Splunk Cloud でこれらの時系列メトリクスを簡単に可視化できます。

Splunk Cloud インスタンスで **Dashboards** に移動し、**Create New Dashboard** を選択します。

![Create new dashboard in Splunk Cloud](../../images/create_new_dashboard_splunk_cloud.png)

ダッシュボードのタイトル、権限、**Dashboard Studio** を選択し、Layout Mode も任意のものを選びます。
**Create** をクリックします。

![Dashboard title and layout options](../../images/dashboard_title_layout_options.png)

Dashboard Studio でチャートアイコンをクリックし、**Column** を選択します。

![Select column chart in Dashboard Studio](../../images/select_column_chart_dashboard_studio.png)

**Select data source** で **Create splunk observability cloud metric search** を選択します。

![Choose observability cloud metric search as data source](../../images/choose_observability_cloud_metric_search.png)

新しいデータソースに名前を付け、**Search for metric or metadata** の下にある **Content Import** リンクをクリックします。

チャートの URL をコピーして **Content URL** フィールドに貼り付けます。

![Paste chart URL and import](../../images/paste_chart_url_and_import.png?width=40vw)

**Import** をクリックします。

![Chart imported to dashboard](../../images/chart_imported_to_dashboard.png)

![Chart visible in dashboard](../../images/chart_visible_in_dashboard.png)

ダッシュボードに合わせてチャートのサイズを調整します。

![Resize chart in dashboard](../../images/resize_chart_in_dashboard.png?width=40vw)

チャートの **Configuration** の右側で **Interactions** を展開し、**Add Interaction** をクリックします。

![Expand interactions and add interaction](../../images/expand_interactions_add_interaction.png)

Splunk Observability のダッシュボードから URL をコピーします。

![Apply interaction settings](../../images/apply_interaction_settings.png?width=40vw)

**On click** で **Link to custom URL** を選択し、Splunk Observability Cloud のダッシュボードの URL を追加することで、ソースデータへ簡単に戻れるようにします。
ナビゲーションをわかりやすくするために **Open in new tab** も選択します。

![Interaction added](../../images/interaction_added.png)

右上の **Save** をクリックしてダッシュボードを保存します。

![Save dashboard in Splunk Cloud](../../images/save_dashboard_splunk_cloud.png)

チャート内のカラムまたは名前をハイライトしてクリックします。

![Click column or name in chart](../../images/click_column_or_name_in_chart.png)

Splunk Observability に戻ろうとしている旨が表示されます。**Continue** をクリックします。

![Continue navigation to Splunk Observability](../../images/continue_navigation_splunk_observability.png)

これで、Splunk Cloud から対応する Splunk Observability ダッシュボードに戻りました。

{{% /notice %}}
