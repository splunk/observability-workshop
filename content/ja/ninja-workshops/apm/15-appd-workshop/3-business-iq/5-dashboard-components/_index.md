---
title: ダッシュボードコンポーネント
time: 2 minutes
weight: 5
description: この演習では、魅力的なダッシュボードを構築するために使用できるダッシュボードコンポーネントのいくつかを扱います。
---
ダッシュボードを構築する機能は、AppDynamicsの機能と価値を支える重要なコンポーネントです。この演習では、魅力的なダッシュボードを構築するために使用できるダッシュボードコンポーネントのいくつかを扱います。

## 新しいダッシュボードを作成する

1. **Dashboard & Reports** タブを選択します。
2. **Create Dashboard** をクリックします。
3. **SuperCar-Dashboard-YOURINITIALS** のようなダッシュボード名を入力します。
4. **Canvas Type** として **Absolute Layout** を選択します。
5. **OK** をクリックします。

![NewDashboard](images/05-biq-create-dashboard.png)

新しく作成された空のダッシュボードを開きます。これからさまざまなウィジェットタイプを追加していきます。

## ダッシュボードコンポーネントのカスタムウィジェットビルダー

カスタムウィジェットビルダーは、数値ビュー、時系列、円グラフなど、データのさまざまな表現を生成できる柔軟性の高いツールです。AppDynamics AD Query Languageに基づいています。

ウィジェットを作成するには、以下の手順に従います。

1. ダッシュボード左上の **Edit Mode** を切り替えます。
2. **Add Widget** をクリックします。
3. 左側の **Analytics** タブを選択します。
4. **Custom Widget Builder** をクリックします。

![NewCustomWidgetBuilder](images/05-biq-widget-builder.png)

Custom Widget Builderでは多数のチャートタイプを作成できます。情報を単純にドラッグ＆ドロップすることも、Advancedペインで AD Query を作成することもできます。

![NewCustomWidgetBuilder](images/05-biq-add-widget.png)

ここでは、Numeric、Bar、Pie Chartsを取り上げます。

### Numeric charts

**演習:** エラーによる影響を金額で定量化することで、ITパフォーマンスがビジネス収益に与える影響を示すことができます。

1. **Numeric** チャートタイプを選択します。
2. Application フィールドにフィルターを追加し、アプリケーション名 **Supercar-Trader-YOURINITIALS** を選択します。
3. **/Supercar-Trader/sell.do** ビジネストランザクションにフィルターを追加します。
4. User Experience フィールドにフィルターを追加し、エラーの影響を表示するために **Error** のみを選択します。
5. 左パネルで **CarPrice_MIDC** フィールドを見つけ、Y軸にドラッグ＆ドロップします。SUMがモデルごとの合計価格を取得するための集計として使用されていることに注目してください。
6. 視認性を高めるため、フォントの色を赤に変更します。
7. **Save** をクリックします。

![NumericChartWidget](images/05-biq-lost-revenue.png)

User Experience フィルターをNORMAL、SLOW、VERY SLOWのみを含むように変更すれば、**$ Amount Transacted Successfully** 基準に対しても同じことができることに注意してください。

また、Analyticsモジュールでカスタムメトリクスを作成し、**$ Amount Impacted** がベースライン以上であるかを示すヘルスルールを定義することで、このメトリクスをベースライン化することもできます。通貨のラベルを追加することもできます。

![NumericChartSamples](images/06-numeric-chart-widget-samples-09.png)

### Bar charts

**演習:** ここからは、影響を受けた上位の車種モデル(Top Impacted Car Models)を可視化する棒グラフを作成します。このチャートでは、すべての **SellCar** トランザクションの車種モデルを、User Experienceで分類して表示します。

1. **+ Add Widget**、**Analytics**、**Custom Widger Builder** をクリックして新しいウィジェットを作成します。
2. **Column** チャートタイプを選択します。
3. 以下のフィルターを追加します: Application = **Supercar-Trader-YOURINITIALS** および Business Transaction = **/Supercar-Trader/sell.do**。
4. **CarModel\_MIDC** と **User Experience** をX軸に追加します。
5. **Save** をクリックします。

![BarChartWidget](images/05-biq-bar-chart.png)

このチャートタイプはニーズに応じて調整できます。たとえば、X軸を Customer Type、Company、Organizationなどでグループ化できます。次の例を参照してください。

![BarChartSamples](images/06-bar-chart-widget-samples-05.png)

### Pie charts

ここからは、`sellCar` トランザクションで報告されたすべての車種モデルとモデルごとの価格合計を表示する円グラフを作成します。これにより、アプリケーション内で最も需要の高いモデルが表示されます。

1. 新しいウィジェットを作成します。
2. **Pie** チャートタイプを選択します。
3. 以下のフィルターを追加します: Application = **Supercar-Trader-YOURINITIALS** および Business Transaction = **/Supercar-Trader/sell.do**。
4. **CarModel\_MIDC** をX軸に追加します。
5. **CarPrice\_MIDC** をY軸に追加します。**SUM** がモデルごとの合計価格を取得するための集計として使用されていることに注目してください。
6. タイトル **Sold by Car Model** を追加します。
7. **Save** をクリックします。

![PieChartWidget](images/05-biq-pie-chart.png)

円グラフウィジェットの追加の使用例については、次の例を参照してください。

![PieChartSamples](images/06-pie-chart-widget-samples-07.png)

## ダッシュボードコンポーネント: コンバージョンファネル

コンバージョンファネルは、複数のステップからなるプロセスを通過するユーザーやイベントの流れを可視化するのに役立ちます。これにより、より高いコンバージョンを実現するためにどのステップを最適化できるかをよりよく理解できます。また、コンバージョンファネルを使用して各ステップのITパフォーマンスを調査し、ユーザーエクスペリエンスにどのような影響を与えるかを理解し、ユーザーの離脱原因を特定することもできます。

ファネルは、各ステップへの総訪問数ではなく、特定の順序でこのパスを実行したユーザーに従ってフィルタリングされる点に注意してください。

ファネル作成の最初のステップは、ファネルを通過する各ユーザーのナビゲーションを表すことができるトランザクションの一意の識別子を選択することです。通常、Session ID はファネルの各ステップを通じて持続するため、最適な選択肢となります。

Session ID はトランザクションから取得できます。ファネルトランザクションのカウンタとして使用するために、**SessionId** データコレクターが必要です。

JavaアプリケーションでAppDynamicsは、デフォルトのHTTPデータコレクターでSession IDを扱う機能を備えています。これが有効になっていることを確認し、すべてのビジネストランザクションに適用して、すべてのトランザクションのSession IDを取得します。

1. **Applications** タブを選択します。
2. **Supercar-Trader-YOURINITIALS** アプリケーションを選択します。
3. 左側の **Configuration** タブを選択します。
4. **Instrumentation** をクリックします。
5. **Data Collectors** タブを選択します。
6. **Default HTTP Request Request Data Collectors** を編集します。
7. **Transaction Analytics** を選択します。
8. **SessionID** が選択されていることを確認します。
9. **Save** をクリックします。

![EnableSessionId](images/05-biq-session-id.png)

次に、**/Supercar-Trader/home.do** ページから複数回ナビゲートして負荷をかけます。その後、アプリケーションの **/Supercar-Trader/sell.do** ページに直接ナビゲートします。

ダッシュボードに戻ってファネルウィジェットを作成します。

1. **Edit** スライダーを切り替えます。
2. **Add Widget** をクリックします。
3. **Analytics** タブを選択します。
4. **Funnel Analysis** をクリックします。
5. ドロップダウンリストから **Transactions** を選択します。
6. **Count Distinct of** で、ドロップダウンリストから **uniqueSessionId** を選択します。
7. **Add Step** をクリックします。**Home Page** という名前を付けます。
8. **Add Criteria** をクリックします。次の条件を追加します: **Application**: Supercar-Trader-YOURINITIALS および **Business Transactions**: **/Supercar-Trader/home.do**。
9. **Add Step** をクリックします。**SellCar Page** という名前を付けます。
10. **Add Criteria** をクリックします。次の条件を追加します: **Application:** Supercar-Trader-YOURINITIALS および **Business Transactions:** /Supercar-Trader/sell.do。
11. 右パネルの **Show Health** チェックボックスを選択して、フローマップでトランザクションの健全性を可視化します。
12. **Save** をクリックします。

![FunnelWidget](images/05-biq-funnel-chart.png)
