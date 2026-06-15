---
title: HTTP Data Collector の設定
time: 2 minutes
weight: 3
description: この演習では、HTTP Data Collector を有効にして使用します。
---

Data Collector を使用すると、ビジネストランザクションやトランザクション分析データにアプリケーションデータを補足できます。アプリケーションデータは、ビジネストランザクションのパフォーマンス問題にコンテキストを追加できます。例えば、パフォーマンスの問題が発生しているビジネストランザクションの特定のパラメータ値や戻り値（特定のユーザー、注文、製品など）を表示します。

HTTP Data Collector は、ビジネストランザクションでやり取りされる HTTP メッセージの URL、パラメータ値、ヘッダー、Cookie をキャプチャします。

この演習では、以下のタスクを実行します

* すべての HTTP Data Collector を有効にする。
* 関連する HTTP Data Collector を確認して選択する。
* HTTP パラメータを使用して Analytics にビジネスデータをキャプチャする。
* HTTP パラメータの Analytics を検証する。

## すべての HTTP Data Collector を有効にする

最初に、すべての HTTP Data Collector をキャプチャして、Analytics にキャプチャしてダッシュボードで使用できる有用なパラメータを確認します。

{{% notice title="Tip" style="orange"  icon="lightbulb" %}}
この手順は本番環境ではなく、UAT 環境で実行することを強く推奨します。
{{% /notice %}}

1. 画面左上の **Applications** タブを選択します。
2. **Supercar-Trader-YOURINITIALS** アプリケーションを選択します。
3. 左側の **Configuration** タブを選択します。
4. **Instrumentation** リンクをクリックします。
5. **Data Collectors** タブを選択します。
6. **HTTP Request Data Collectors** の **Add** ボタンをクリックします。

![HTTPDataCollectors 1](images/05-biq-datacollectors.png)

次に、すべての HTTP パラメータをキャプチャする HTTP Data Collector を設定します。Transaction Analytics に必要な正確なパラメータを特定するまで、オーバーヘッドを避けるために Transaction Snapshots でのみ有効にします。

1. **Name** に **All HTTP Param** と指定します。
2. **Enable Data Collector for** の下で、**Transaction Snapshots** のチェックボックスをオンにします。
3. Transaction Analytics は有効に**しないでください**。
4. HTTP Parameters セクションの **\+ Add** をクリックします。
5. 新しいパラメータの Display Name に **All** と指定します。
6. HTTP Parameter name にアスタリスク **\*** を指定します。
7. **Save** をクリックします。

![HTTPDataCollectors 2](images/05-biq-http-collector.png)

1. "Ok" をクリックして Data Collector を確認します。
2. **/Supercar-Trader/sell.do** トランザクションを有効にします。
3. **Save** をクリックします。

![HTTPDataCollectors 2](images/05-biq-bt-enble.png)

## 関連する HTTP Data Collector を確認して選択する

1. アプリケーション、特に **SellCar** トランザクションに負荷をかけます。Full Call Graph を含むスナップショットの1つを開き、**Data Collectors Tab** を選択します。

すべての HTTP パラメータが表示されます。Car Price、Color、Year など、多くの重要なメトリクスが確認できます。

1. 正確なパラメータ名をメモし、**HTTP Parameters** リストに再度追加して Transaction Analytics で有効にします。
2. 追加したら、**All HTTP Param** HTTP Data Collector を削除します。

![HTTPDataCollectors 2](images/05-biq-snapshot-collector.png)

## HTTP パラメータを使用して Analytics にビジネスデータをキャプチャする

ここでは HTTP Data Collector を再度設定しますが、今回は有用な HTTP パラメータのみをキャプチャし、Transaction Analytics で有効にします。新しい HTTP Data Collector を追加します：Application -> Configuration -> Instrumentation -> Data Collector tab -> **HTTP Request Data Collectors** セクションの **Add** をクリックします。

1. Name に **CarDetails** と指定します。
2. **Transaction Snapshots** を有効にします。
3. **Transaction Analytics** を有効にします。
4. HTTP Parameters セクションの **\+ Add** をクリックします。
5. 新しいパラメータの Display Name に **CarPrice\_http** と指定します。
6. HTTP Parameter name に **carPrice** と指定します。
7. 以下に示すように、残りの Car パラメータについても同様に繰り返します。
8. **Save** をクリックします。
9. **Ok** をクリックして Data Collector の実装を確認します。

![SaveHttpDataCollectors](images/05-biq-httpcollector-cardetails.png)
![Car Params](images/05-biq-car-params.png)

1. **/Supercar-Trader/sell.do** トランザクションを有効にします。
2. **Save** をクリックします。

![HTTPDataCollectors 2](images/05-biq-cardetails-bt.png)

1. **All HTTP Param** Collector をクリックして選択し、**Delete** ボタンをクリックして削除します。

## HTTP パラメータの Analytics を検証する

ここでは、HTTP Data Collector によって AppDynamics Analytics にビジネスデータがキャプチャされたかどうかを検証します。

1. 画面左上の **Analytics** タブを選択します。
2. **Searches** タブを選択します。
3. **+ Add** ボタンをクリックし、新しい **Drag and Drop Search** を作成します。

![Drag and Drop Search](images/05-biq-search.png)

1. **+ Add Criteria** をクリックします。
2. **Application** を選択し、アプリケーション名 **Supercar-Trader-YOURINITIALS** を検索します。
3. **Fields** パネルで、Custom HTTP Request Data に **Business Parameters** がフィールドとして表示されていることを確認します。
4. **CarPrice_http** のチェックボックスをオンにし、フィールドにデータがあることを確認します。

![ValidateHttpDataCollectors](images/05-biq-search-validation.png)
