---
title: HTTP Data Collector の設定
time: 2 minutes
weight: 3
description: この演習では、HTTP Data Collector を有効化して使用します。
---

Data Collector を使用すると、ビジネストランザクションおよびトランザクション分析データにアプリケーションデータを補足できます。アプリケーションデータは、ビジネストランザクションのパフォーマンス問題にコンテキストを追加できます。たとえば、パフォーマンス問題の影響を受けるビジネストランザクションの特定のパラメータ値や戻り値（特定のユーザー、注文、製品など）を表示します。

HTTP Data Collector は、ビジネストランザクションでやり取りされる HTTP メッセージの URL、パラメータ値、ヘッダー、Cookie をキャプチャします。

この演習では、以下のタスクを実行します

* すべての HTTP Data Collector を有効化する。
* 関連する HTTP Data Collector を確認して選択する。
* HTTP パラメータを使用して Analytics にビジネスデータをキャプチャする。
* HTTP パラメータの Analytics を検証する。

## すべての HTTP Data Collector を有効化する

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

次に、すべての HTTP パラメータをキャプチャする HTTP Data Collector を設定します。Transaction Analytics に必要な正確なパラメータを特定するまで、オーバーヘッドを避けるために Transaction Snapshots でのみ有効化します。

1. **Name** に **All HTTP Param** を指定します。
2. **Enable Data Collector for** の下にある **Transaction Snapshots** のチェックボックスをオンにします。
3. Transaction Analytics は**有効にしないでください**。
4. HTTP Parameters セクションの **\+ Add** をクリックします。
5. 新しいパラメータの Display Name に **All** を指定します。
6. HTTP Parameter name にアスタリスク **\*** を指定します。
7. **Save** をクリックします。

![HTTPDataCollectors 2](images/05-biq-http-collector.png)

8. "Ok" をクリックして Data Collector を確認します。
9. **/Supercar-Trader/sell.do** トランザクションを有効化します。
10. **Save** をクリックします。

![HTTPDataCollectors 2](images/05-biq-bt-enble.png)

## 関連する HTTP Data Collector を確認して選択する

1. アプリケーションに負荷をかけます。特に **SellCar** トランザクションに対して負荷をかけます。Full Call Graph を含むスナップショットの1つを開き、**Data Collectors Tab** を選択します。

すべての HTTP パラメータが表示されます。Car Price、Color、Year など、多くの重要なメトリクスが確認できます。

2. 正確なパラメータ名をメモして、**HTTP Parameters** リストに再度追加し、Transaction Analytics で有効化します。
3. 追加が完了したら、**All HTTP Param** HTTP Data Collector を削除します。

![HTTPDataCollectors 2](images/05-biq-snapshot-collector.png)

## HTTP パラメータを使用して Analytics にビジネスデータをキャプチャする

次に、HTTP Data Collector を再度設定しますが、今回は有用な HTTP パラメータのみをキャプチャし、Transaction Analytics で有効化します。新しい HTTP Data Collector を追加します：Application -> Configuration -> Instrumentation -> Data Collector tab -> **HTTP Request Data Collectors** セクションの下にある **Add** をクリックします。

1. Name に **CarDetails** を指定します。
2. **Transaction Snapshots** を有効化します。
3. **Transaction Analytics** を有効化します。
4. HTTP Parameters セクションの **\+ Add** をクリックします。
5. 新しいパラメータの Display Name に **CarPrice\_http** を指定します。
6. HTTP Parameter name に **carPrice** を指定します。
7. 以下に示すように、残りの Car パラメータについても同様に繰り返します。
8. **Save** をクリックします。
9. **Ok** をクリックして Data Collector の実装を確認します。

![SaveHttpDataCollectors](images/05-biq-httpcollector-cardetails.png)
![Car Params](images/05-biq-car-params.png)

10. **/Supercar-Trader/sell.do** トランザクションを有効化します。
11. **Save** をクリックします。

![HTTPDataCollectors 2](images/05-biq-cardetails-bt.png)

12. **All HTTP Param** Collector をクリックして選択し、**Delete** ボタンをクリックして削除します。

## HTTP パラメータの Analytics を検証する

次に、AppDynamics Analytics で HTTP Data Collector によってビジネスデータがキャプチャされたかどうかを検証します。

1. 画面左上の **Analytics** タブを選択します。
2. **Searches** タブを選択します。
3. **+ Add** ボタンをクリックし、新しい **Drag and Drop Search** を作成します。

![Drag and Drop Search](images/05-biq-search.png)

4. **+ Add Criteria** をクリックします。
5. **Application** を選択し、アプリケーション名 **Supercar-Trader-YOURINITIALS** を検索します。
6. **Fields** パネルの下で、Custom HTTP Request Data のフィールドとして **Business Parameters** が表示されていることを確認します。
7. **CarPrice_http** のチェックボックスをオンにして、フィールドにデータがあることを確認します。

![ValidateHttpDataCollectors](images/05-biq-search-validation.png)
