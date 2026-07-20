---
title: HTTP Data Collectorの設定
time: 2 minutes
weight: 3
description: この演習では、HTTP Data Collectorを有効化して使用します。

---
Data Collectorを使用すると、ビジネストランザクションやTransaction Analyticsのデータをアプリケーションデータで補完できます。アプリケーションデータは、ビジネストランザクションのパフォーマンス問題にコンテキストを追加します。例えば、パフォーマンスの問題が発生しているビジネストランザクションの特定のパラメータの値や戻り値（特定のユーザー、注文、製品など）を表示します。

HTTP Data Collectorは、ビジネストランザクションでやり取りされるHTTPメッセージのURL、パラメータ値、ヘッダー、Cookieをキャプチャします。

この演習では、以下のタスクを実行します。

* すべてのHTTP Data Collectorを有効化する
* 関連するHTTP Data Collectorを確認して選択する
* HTTP Paramsを使用してAnalyticsにビジネスデータをキャプチャする
* HTTPパラメータのAnalyticsを検証する

## すべてのHTTP Data Collectorを有効化する

最初に、すべてのHTTP Data Collectorをキャプチャして、Analyticsに取り込んでダッシュボードで使用できる有用なパラメータを確認します。

{{% notice title="ヒント" style="orange"  icon="lightbulb" %}}
このステップは本番環境ではなく、UAT環境で実行することを強く推奨します。
{{% /notice %}}

1. 画面左上の **Applications** タブを選択します。
2. **Supercar-Trader-YOURINITIALS** アプリケーションを選択します。
3. 左側の **Configuration** タブを選択します。
4. **Instrumentation** リンクをクリックします。
5. **Data Collectors** タブを選択します。
6. **HTTP Request Data Collectors** の **Add** ボタンをクリックします。

![HTTPDataCollectors 1](images/05-biq-datacollectors.png)

次に、すべてのHTTPパラメータをキャプチャするHTTP Data Collectorを設定します。Transaction Analyticsに必要な正確なパラメータを特定するまで、オーバーヘッドを避けるためにTransaction Snapshotsのみで有効にします。

1. **Name** に **All HTTP Param** を指定します。
2. **Enable Data Collector for** の下で、 **Transaction Snapshots** のチェックボックスをオンにします。
3. Transaction Analyticsは **有効にしないでください** 。
4. HTTP Parametersセクションの **\+ Add** をクリックします。
5. 新しいParameterのDisplay Nameに **All** を指定します。
6. HTTP Parameter nameにアスタリスク **\*** を指定します。
7. **Save** をクリックします。

![HTTPDataCollectors 2](images/05-biq-http-collector.png)

1. "Ok"をクリックしてData Collectorを確認します。
2. **/Supercar-Trader/sell.do** トランザクションを有効にします。
3. **Save** をクリックします。

![HTTPDataCollectors 2](images/05-biq-bt-enble.png)

## 関連するHTTP Data Collectorを確認して選択する

1. アプリケーションに負荷をかけます。特に **SellCar** トランザクションを実行します。Full Call Graphを含むスナップショットの1つを開き、 **Data Collectors Tab** を選択します。

すべてのHTTPパラメータが表示されます。Car Price、Color、Yearなど、いくつかの重要なメトリクスが確認できます。

1. 正確なパラメータ名を記録し、 **HTTP Parameters** リストに再度追加してTransaction Analyticsで有効にします。
2. 追加が完了したら、 **All HTTP Param** HTTP Data Collectorを削除します。

![HTTPDataCollectors 2](images/05-biq-snapshot-collector.png)

## HTTP ParamsでAnalyticsにビジネスデータをキャプチャする

再度HTTP Data Collectorを設定しますが、今回は有用なHTTPパラメータのみをキャプチャしてTransaction Analyticsで有効にします。新しいHTTP Data Collectorを追加します: Application -> Configuration -> Instrumentation -> Data Collectorタブ -> **HTTP Request Data Collectors** セクションの **Add** をクリック

1. Nameに **CarDetails** を指定します。
2. **Transaction Snapshots** を有効にします。
3. **Transaction Analytics** を有効にします。
4. HTTP Parametersセクションの **\+ Add** をクリックします。
5. 新しいParameterのDisplay Nameに **CarPrice\_http** を指定します。
6. HTTP Parameter nameに **carPrice** を指定します。
7. 以下に示すように、残りのCarパラメータについても同様に繰り返します。
8. **Save** をクリックします。
9. **Ok** をクリックしてData Collectorの実装を確認します。

![SaveHttpDataCollectors](images/05-biq-httpcollector-cardetails.png)
![Car Params](images/05-biq-car-params.png)

1. **/Supercar-Trader/sell.do** トランザクションを有効にします。
2. **Save** をクリックします。

![HTTPDataCollectors 2](images/05-biq-cardetails-bt.png)

1. **All HTTP Param** Collectorをクリックして選択し、 **Delete** ボタンをクリックして削除します。

## HTTPパラメータのAnalyticsを検証する

AppDynamics AnalyticsでHTTP Data Collectorによってビジネスデータがキャプチャされたかどうかを検証します。

1. 画面左上の **Analytics** タブを選択します。
2. **Searches** タブを選択します。
3. **+ Add** ボタンをクリックし、新しい **Drag and Drop Search** を作成します。

![Drag and Drop Search](images/05-biq-search.png)

1. **+ Add Criteria** をクリックします。
2. **Application** を選択し、アプリケーション名 **Supercar-Trader-YOURINITIALS** を検索します。
3. **Fields** パネルで、Custom HTTP Request Dataのフィールドとして **Business Parameters** が表示されていることを確認します。
4. **CarPrice_http** のチェックボックスをオンにし、フィールドにデータがあることを確認します。

![ValidateHttpDataCollectors](images/05-biq-search-validation.png)
