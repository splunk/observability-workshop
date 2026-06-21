---
title: Kubernetes 監査イベントメトリクスの可視化
linkTitle: 4.2 Kubernetes 監査イベントメトリクスの可視化
weight: 3
---

メトリクスにディメンションが追加されたので、イベントの `verb` ディメンションを使用して、さまざまな Kubernetes アクションの状態を示すチャートを作成します。

{{% notice title="演習: Kubernetes 監査イベントメトリクスの可視化" style="green" icon="running" %}}

**1.** 前のセクションで作成したチャートを閉じた場合は、右上の **+** アイコン → **Chart** をクリックして新しいチャートを作成します。

![Create New Chart](../../images/create_new_chart.png?width=40vw)

**2.** 新しく作成したチャートの **Plot Editor** で、メトリクス名フィールドに `k8s_audit*` と入力します。ここではワイルドカードを使用して、取り込まれているすべてのメトリクスを確認できるようにします。

![Review Metric](../../images/review_metric.png?width=40vw)

**3.** メトリクスが1つから複数に変化したことに注目してください。これは、パイプラインを更新してディメンションを含めた時点での変化です。このメトリクスが利用可能になったので、アクションにエラーが関連付けられているかどうかを確認できるようにチャートを調整しましょう。

![Metric Timeseries](../../images/metric_timeseries.png?width=40vw)

まず、**response_status** フィールドで利用可能な HTTP レスポンスコードを使用して、成功しなかった Kubernetes イベントのみにフィルタリングします。レスポンスコードが **409**（コンフリクトを示す。例えば、既に存在するリソースを作成しようとした場合）または **503**（リクエストに対して API が応答しなかったことを示す）のイベントのみを対象とします。

**4.** チャートの Plot Editor で **Add filter** をクリックし、フィールドに **response_status** を使用し、値として **409.0** と **503.0** を選択します。

次に、**resource**、**action**、**response status** でグループ化されたイベントの合計数を計算する関数をチャートに追加します。これにより、どのアクションと関連リソースにエラーがあったかを正確に確認できます。これで、成功しなかった Kubernetes イベントのみを表示しています。

**5.** **Add analytics** → **Sum** → **Sum:Aggregation** をクリックし、**Group by** フィールドに **resource**、**action**、**response_status** を追加します。

![Add Metric Filters](../../images/add_metric_filters.png?width=40vw)

**6.** 上部のボタンにあるチャートタイプを使用して、チャートを **heatmap** に変更します。**Plot editor** の隣にある **Chart options** をクリックします。**Group by** セクションで **response_status**、次に **action** を選択します。**Color threshold** を **Auto** から **Fixed** に変更します。青い **+ button** をクリックして別のしきい値を追加します。**下矢印を Yellow**、**中間を orange** に変更します。**上矢印は red のまま**にします。**中間しきい値に 5**、**上限しきい値に 20** を入力します。

![Configure Thresholds](../../images/configure_thresholds.png?width=40vw)

**7.** チャートの右上にある青い **Save as...** ![Preview Button](../../images/save_as_btn.png?height=20px&classes=inline) ボタンをクリックします。チャートの名前を入力します（例: Kubernetes Audit Logs - Conflicts and Failures）。

![Chart Name](../../images/chart_name.png)

**8.** **Choose a dashboard** で **New dashboard** を選択します。

![New Dashboard](../../images/new_dashboard.png)

**9.** 後で簡単に見つけられるように、イニシャルを含むダッシュボード名を入力します。**Save** をクリックします。

![New Dashboard Name](../../images/dashboard_name.png)

**10.** 作成した新しいダッシュボードが選択されていることを確認し、**Ok** をクリックします。

![Save New Dashboard](../../images/save_new_dashboard.png)

これで、作成したチャートが含まれる新しい Kubernetes Audit Events ダッシュボードに移動します。環境内の他のメトリクスから新しいチャートを追加できます。例えば、Kubernetes クラスター上で実行されているアプリケーションのエラーやレスポンスタイム、Pod フェーズ、Pod メモリ使用率などの他の Kubernetes メトリクスを追加して、クラスターイベントからアプリケーションの状態まで、Kubernetes 環境の相関ビューを構築できます。

![Audit Dashboard](../../images/audit_dashboard.png?width=40vw)

チャートのビジュアライゼーションボックスの右上にある三点リーダー `...` を使用して、このチャートのコピーを作成します。

![Copy chart button](../../images/copy_chart_button.png?width=40vw)

UI の右上にある `+` アイコンを使用して、作業中の同じダッシュボードに貼り付けます。

![Paste chart into dashboard](../../images/paste_chart_into_dashboard.png?width=40vw)

貼り付けたチャートをクリックし、ビジュアライゼーションを **Column** チャートに変更します。

![Change to column chart visualization](../../images/change_to_column_chart_visualization.png?width=40vw)

SUM を `resource`、`namespace` のみに変更します（フィルターにより問題のあるコードのみに絞り込まれています）。

![Group chart by resource and namespace](../../images/group_chart_by_resource_and_namespace.png?width=40vw)

Chart options でタイトルを `Kubernetes Audit Logs - Conflicts by Namespace` に変更します。

![Change chart title](../../images/change_chart_title.png?width=40vw)

**Save** をクリックして閉じます。

![Save and close chart](../../images/save_and_close_chart.png)

{{% /notice %}}

{{% notice title="演習: Kubernetes 監査ログに基づくディテクターの作成" style="green" icon="running" %}}

Conflicts by Namespace チャートで小さなベルアイコンをクリックし、New detector from chart を選択します。

![Bell icon to create detector](../../images/bell_icon_create_detector.png?width=40vw)

名前を入力し、**Create alert rule** をクリックします。

![Enter name for alert rule](../../images/enter_name_alert_rule.png?width=40vw)

Alert condition で **Static Threshold** をクリックし、Proceed to **Alert Settings** をクリックします。

![Select static threshold condition](../../images/select_static_threshold_condition.png?width=40vw)

**Threshold** に `20` を入力します。

![Enter threshold value](../../images/enter_threshold_value.png?width=40vw)

このアラートの受信者は選択しないので、**Activate** をクリックし、**Activate Alert Rule** と **Save** を選択します。

![Activate alert rule and save](../../images/activate_alert_rule_and_save.png?width=40vw)

右上の **Save** を最後にもう一度クリックして、ディテクターを保存します。

![Final save for detector](../../images/final_save_detector.png?width=40vw)

ダッシュボードに戻ると、チャートに関連付けられたディテクターが、チャート上の点灯したベルアイコンで示されていることが確認できます。

![Detector bell icon on chart](../../images/detector_bell_icon_on_chart.png?width=40vw)

{{% /notice %}}

{{% notice title="演習: Splunk Cloud - Dashboard Studio で時系列データを可視化する" style="green" icon="running" %}}

時系列メトリクスが Splunk Observability Cloud のデータストアに取り込まれたので、これらの時系列メトリクスを Splunk Cloud で簡単に可視化できます。

Splunk Cloud インスタンスで **Dashboards** に移動し、**Create New Dashboard** を選択します。

![Create new dashboard in Splunk Cloud](../../images/create_new_dashboard_splunk_cloud.png)

Dashboard のタイトル、権限、**Dashboard Studio** を選択し、任意の Layout Mode を選びます。
**Create** をクリックします。

![Dashboard title and layout options](../../images/dashboard_title_layout_options.png)

Dashboard Studio でチャートアイコンをクリックし、**Column** を選択します。

![Select column chart in Dashboard Studio](../../images/select_column_chart_dashboard_studio.png)

**Select data source** で **Create splunk observability cloud metric search** を選択します。

![Choose observability cloud metric search as data source](../../images/choose_observability_cloud_metric_search.png)

新しいデータソースの名前を入力し、**Search for metric or metadata** の下にある **Content Import** リンクをクリックします。

チャートの URL をコピーして **Content URL** フィールドに貼り付けます。

![Paste chart URL and import](../../images/paste_chart_url_and_import.png?width=40vw)

**Import** をクリックします。

![Chart imported to dashboard](../../images/chart_imported_to_dashboard.png)

![Chart visible in dashboard](../../images/chart_visible_in_dashboard.png)

チャートのサイズをダッシュボードに合わせて調整します。

![Resize chart in dashboard](../../images/resize_chart_in_dashboard.png?width=40vw)

チャートの **Configuration** の右側にある **Interactions** を展開し、**Add Interaction** をクリックします。

![Expand interactions and add interaction](../../images/expand_interactions_add_interaction.png)

Splunk Observability のダッシュボードから URL をコピーします。

![Apply interaction settings](../../images/apply_interaction_settings.png?width=40vw)

**On click** で **Link to custom URL** を選択し、ソースデータに簡単に戻れるように Splunk Observability Cloud のダッシュボードの URL を追加します。
また、ナビゲーションを便利にするために **Open in new tab** を選択します。

![Interaction added](../../images/interaction_added.png)

右上の **Save** をクリックしてダッシュボードを保存します。

![Save dashboard in Splunk Cloud](../../images/save_dashboard_splunk_cloud.png)

チャート内のカラムまたは名前をハイライトしてクリックします。

![Click column or name in chart](../../images/click_column_or_name_in_chart.png)

Splunk Observability に戻ることが通知されます。**Continue** をクリックします。

![Continue navigation to Splunk Observability](../../images/continue_navigation_splunk_observability.png)

これで、Splunk Cloud から対応する Splunk Observability ダッシュボードに戻ることができました。

{{% /notice %}}
