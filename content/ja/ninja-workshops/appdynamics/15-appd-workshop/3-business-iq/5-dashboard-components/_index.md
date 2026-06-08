---
title: ダッシュボードコンポーネント
time: 2 minutes
weight: 5
description: この演習では、魅力的なダッシュボードを構築するために使用できるダッシュボードコンポーネントの一部を操作します。
---
ダッシュボードを構築する機能は、AppDynamics の機能と価値の重要なコンポーネントです。この演習では、魅力的なダッシュボードを構築するために使用できるダッシュボードコンポーネントの一部を操作します。

## 新しいダッシュボードの作成

1. **Dashboard & Reports** タブを選択します。
2. **Create Dashboard** をクリックします。
3. **SuperCar-Dashboard-YOURINITIALS** などのダッシュボード名を入力します。
4. **Canvas Type** として **Absolute Layout** を選択します。
5. **OK** をクリックします。

![NewDashboard](images/05-biq-create-dashboard.png)

新しく作成された空のダッシュボードを開きます。ここからさまざまなウィジェットタイプを追加していきます。

## ダッシュボードコンポーネント カスタムウィジェットビルダー

カスタムウィジェットビルダーは、数値ビュー、時系列、円グラフなど、さまざまなデータ表現を生成できる非常に柔軟なツールです。AppDynamics AD Query Language に基づいています。

ウィジェットを作成するには、次の手順に従います

1. ダッシュボードの左上隅にある **Edit Mode** を切り替えます。
2. **Add Widget** をクリックします。
3. 左側の **Analytics** タブを選択します。
4. **Custom Widget Builder** をクリックします。

![NewCustomWidgetBuilder](images/05-biq-widget-builder.png)

Custom Widget Builder では多くのチャートタイプを作成できます。情報をドラッグ＆ドロップするだけで、または Advanced ペインで AD Query を作成することもできます。

![NewCustomWidgetBuilder](images/05-biq-add-widget.png)

ここでは、Numeric、Bar、Pie チャートについて説明します。

### 数値チャート

**演習:** エラーによって影響を受けた金額を定量化することで、IT パフォーマンスがビジネス収益に与える影響を示すことができます。

1. **Numeric** チャートタイプを選択します。
2. Application フィールドにフィルターを追加し、アプリケーション名 **Supercar-Trader-YOURINITIALS** を選択します。
3. **/Supercar-Trader/sell.do** ビジネストランザクションにフィルターを追加します。
4. User Experience フィールドにフィルターを追加し、**Error** のみを選択してエラーの影響を表示します。
5. 左パネルで **CarPrice_MIDC** フィールドを見つけ、Y-Axis にドラッグ＆ドロップします。SUM がモデルごとの合計価格を取得するための集計として使用されていることに注目してください。
6. 視認性を高めるためにフォントの色を赤に変更します。
7. **Save** をクリックします。

![NumericChartWidget](images/05-biq-lost-revenue.png)

User Experience フィルターを NORMAL、SLOW、VERY SLOW のみに変更することで、**$ Amount Transacted Successfully** 基準についても同様のことができます。

また、Analytics モジュールでカスタムメトリクスを作成し、**$ Amount Impacted** がベースライン以上であることを示すヘルスルールを定義することで、このメトリクスのベースラインを設定することもできます。通貨のラベルを追加することもできます。

![NumericChartSamples](images/06-numeric-chart-widget-samples-09.png)

### 棒グラフ

**演習:** 影響を受けた上位の車モデルを視覚化する棒グラフを作成します。このグラフは、すべての **SellCar** トランザクションの車モデルを User Experience ごとに分類して表示します。

1. **+ Add Widget**、**Analytics**、**Custom Widger Builder** をクリックして新しいウィジェットを作成します。
2. **Column** チャートタイプを選択します。
3. 次のフィルターを追加します：Application = **Supercar-Trader-YOURINITIALS** および Business Transaction = **/Supercar-Trader/sell.do**。
4. X-Axis に **CarModel\_MIDC** と **User Experience** を追加します。
5. **Save** をクリックします。

![BarChartWidget](images/05-biq-bar-chart.png)

このチャートタイプは必要に応じて調整できます。たとえば、X-AXIS を Customer Type、Company、Organization などでグループ化できます。次の例を参照してください。

![BarChartSamples](images/06-bar-chart-widget-samples-05.png)

### 円グラフ

`sellCar` トランザクションで報告されたすべての車モデルとモデルごとの価格の合計を表示する円グラフを作成します。これにより、アプリケーションで最も需要の高いモデルが表示されます。

1. 新しいウィジェットを作成します。
2. **Pie** チャートタイプを選択します。
3. 次のフィルターを追加します：Application = **Supercar-Trader-YOURINITIALS** および Business Transaction = **/Supercar-Trader/sell.do**。
4. X-Axis に **CarModel\_MIDC** を追加します。
5. Y-Axis に **CarPrice\_MIDC** を追加します。**SUM** がモデルごとの合計価格を取得するための集計として使用されていることに注目してください。
6. タイトル **Sold by Car Model** を追加します。
7. **Save** をクリックします。

![PieChartWidget](images/05-biq-pie-chart.png)

円グラフウィジェットのその他の使用例については、次の例を参照してください。

![PieChartSamples](images/06-pie-chart-widget-samples-07.png)

## ダッシュボードコンポーネント：コンバージョンファネル

コンバージョンファネルは、複数のステップからなるプロセスを通じたユーザーやイベントのフローを視覚化するのに役立ちます。これにより、より成功したコンバージョンのためにどのステップを最適化できるかをよりよく理解できます。また、コンバージョンファネルを使用して各ステップの IT パフォーマンスを調べ、それらがユーザーエクスペリエンスにどのように影響するかを理解し、ユーザー離脱の原因を特定することもできます。

ファネルは、ステップごとの総訪問数ではなく、その特定の順序でこのパスを実行したユーザーに基づいてフィルタリングされることに注意してください。

ファネル作成の最初のステップは、ファネルを通じた各ユーザーのナビゲーションを表すことができるトランザクションの一意の識別子を選択することです。通常、Session ID はファネルの各ステップを通じて永続するため、最適な選択です。

Session ID はトランザクションからキャプチャできます。ファネルトランザクションのカウンターとして使用するには、**SessionId** データコレクターが必要です。

Java アプリケーションの場合、AppDynamics にはデフォルトの HTTP データコレクターで Session ID をキャプチャする機能があります。これが有効になっていることを確認し、すべてのビジネストランザクションに適用して、各トランザクションの Session ID をキャプチャします。

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

**/Supercar-Trader/home.do** ページから複数回ナビゲートして負荷をかけます。次に、アプリケーションの **/Supercar-Trader/sell.do** ページに直接移動します。

ダッシュボードに戻り、ファネルウィジェットを作成します。

1. **Edit** スライダーを切り替えます。
2. **Add Widget** をクリックします。
3. **Analytics** タブを選択します。
4. **Funnel Analysis** をクリックします。
5. ドロップダウンリストから **Transactions** を選択します。
6. **Count Distinct of** で、ドロップダウンリストから **uniqueSessionId** を選択します。
7. **Add Step** をクリックします。**Home Page** と名前を付けます。
8. **Add Criteria** をクリックします。次の条件を追加します**Application**: Supercar-Trader-YOURINITIALS & **Business Transactions**: **/Supercar-Trader/home.do**。
9. **Add Step** をクリックします。**SellCar Page** と名前を付けます。
10. **Add Criteria** をクリックします。次の条件を追加します**Application:** Supercar-Trader-YOURINITIALS & **Business Transactions:** /Supercar-Trader/sell.do。
11. 右パネルの **Show Health** チェックボックスを選択して、フローマップにトランザクションの健全性を視覚化します。
12. **Save** をクリックします。

![FunnelWidget](images/05-biq-funnel-chart.png)
