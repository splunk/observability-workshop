---
title: HTTP データコレクターの設定
time: 2 minutes
weight: 3
description: この演習では、HTTP データコレクターを有効化して使用します。

---
データコレクターを使用すると、ビジネストランザクションおよびトランザクション分析データをアプリケーションデータで補強できます。アプリケーションデータは、ビジネストランザクションのパフォーマンス問題にコンテキストを追加できます。たとえば、パフォーマンス問題の影響を受けているビジネストランザクションについて、特定のユーザー、注文、製品といった特定のパラメータの値や戻り値を表示できます。

HTTP データコレクターは、ビジネストランザクションでやり取りされる HTTP メッセージの URL、パラメータ値、ヘッダー、Cookie をキャプチャします。

この演習では、以下のタスクを実行します。

* すべての HTTP データコレクターを有効化します。
* 関連する HTTP データコレクターを観察して選定します。
* HTTP パラメータを使用して Analytics でビジネスデータをキャプチャします。
* HTTP パラメータに対する Analytics を検証します。

## すべての HTTP データコレクターを有効化する

最初は、すべての HTTP データコレクターをキャプチャすることで、Analytics に取り込んでダッシュボードで活用できる有用なパラメータを把握できます。

{{% notice title="ヒント" style="orange"  icon="lightbulb" %}}
この手順は本番環境ではなく、UAT 環境で実施することを強く推奨します。
{{% /notice %}}

1. 画面左上の **Applications** タブを選択します。
2. **Supercar-Trader-YOURINITIALS** アプリケーションを選択します。
3. 左側の **Configuration** タブを選択します。
4. **Instrumentation** リンクをクリックします。
5. **Data Collectors** タブを選択します。
6. **HTTP Request Data Collectors** にある **Add** ボタンをクリックします。

![HTTPDataCollectors 1](images/05-biq-datacollectors.png)

これから、すべての HTTP パラメータをキャプチャするように HTTP データコレクターを設定します。Transaction Analytics で必要となる正確なパラメータを特定するまでオーバーヘッドを避けるため、Transaction Snapshots でのみ有効化します。

1. **Name** には **All HTTP Param** を指定します。
2. **Enable Data Collector for** で **Transaction Snapshots** のチェックボックスをオンにします。
3. Transaction Analytics は **有効化しないでください**。
4. HTTP Parameters セクションの **\+ Add** をクリックします。
5. 新しいパラメータの Display Name に **All** を指定します。
6. 次に、HTTP Parameter name にアスタリスク **\*** を指定します。
7. **Save** をクリックします。

![HTTPDataCollectors 2](images/05-biq-http-collector.png)

1. "Ok" をクリックしてデータコレクターを確定します。
2. **/Supercar-Trader/sell.do** トランザクションを有効化します。
3. **Save** をクリックします。

![HTTPDataCollectors 2](images/05-biq-bt-enble.png)

## 関連する HTTP データコレクターの観察と選定

1. アプリケーション、特に **SellCar** トランザクションに負荷をかけます。Full Call Graph 付きのスナップショットを開き、**Data Collectors Tab** を選択します。

これですべての HTTP パラメータが表示されます。Car Price、Color、Year など、いくつかの重要なメトリクスが確認できます。

1. **HTTP Parameters** リストに再度追加して Transaction Analytics で有効化するため、正確なパラメータ名を控えておきます。
2. 追加が完了したら、**All HTTP Param** HTTP データコレクターを削除します。

![HTTPDataCollectors 2](images/05-biq-snapshot-collector.png)

## HTTP パラメータを使用して Analytics でビジネスデータをキャプチャする

これから HTTP データコレクターを再度設定しますが、今回は有用な HTTP パラメータのみをキャプチャし、Transaction Analytics で有効化します。新しい HTTP データコレクターを追加します。Application -> Configuration -> Instrumentation -> Data Collector タブ -> **HTTP Request Data Collectors** セクションの **Add** をクリックします。

1. Name には **CarDetails** を指定します。
2. **Transaction Snapshots** を有効化します。
3. **Transaction Analytics** を有効化します。
4. HTTP Parameters セクションの **\+ Add** をクリックします。
5. 新しいパラメータの Display Name に **CarPrice\_http** を指定します。
6. 次に、HTTP Parameter name に **carPrice** を指定します。
7. 以下に示すように、残りの Car パラメータについても繰り返します。
8. **Save** をクリックします。
9. **Ok** をクリックしてデータコレクターの実装を確認します。

![SaveHttpDataCollectors](images/05-biq-httpcollector-cardetails.png)
![Car Params](images/05-biq-car-params.png)

1. **/Supercar-Trader/sell.do** トランザクションを有効化します。
2. **Save** をクリックします。

![HTTPDataCollectors 2](images/05-biq-cardetails-bt.png)

1. **All HTTP Param** コレクターをクリックし、**Delete** ボタンをクリックして削除します。

## HTTP パラメータに対する Analytics の検証

これから、HTTP データコレクターによってビジネスデータが AppDynamics Analytics でキャプチャされたかを検証します。

1. 画面左上の **Analytics** タブを選択します。
2. **Searches** タブを選択します。
3. **+ Add** ボタンをクリックして、新しい **Drag and Drop Search** を作成します。

![Drag and Drop Search](images/05-biq-search.png)

1. **+ Add Criteria** をクリックします。
2. **Application** を選択し、ご自身のアプリケーション名 **Supercar-Trader-YOURINITIALS** を検索します。
3. **Fields** パネルで、**Business Parameters** が Custom HTTP Request Data のフィールドとして表示されることを確認します。
4. **CarPrice_http** のチェックボックスをオンにし、フィールドにデータが入っていることを検証します。

![ValidateHttpDataCollectors](images/05-biq-search-validation.png)
