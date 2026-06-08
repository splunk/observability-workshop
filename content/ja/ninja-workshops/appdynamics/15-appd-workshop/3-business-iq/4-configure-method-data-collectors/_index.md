---
title: Method Data Collector の設定
time: 2 minutes
weight: 4
description: この演習では、Web ブラウザから AppDynamics Controller にアクセスし、Agentless Analytics を有効にします。
---
Method invocation data collector は、メソッドの引数、変数、戻り値などのコードデータをキャプチャします。HTTP data collector で十分なビジネスデータが取得できない場合でも、コード実行からこれらの情報をキャプチャすることができます。

この演習では、以下のタスクを実行します

* メソッドの検出
* ディスカバリーセッションの開始
* メソッドパラメータの検出
* コード内のオブジェクトへのドリルダウン
* Method invocation data collector の作成
* Method invocation data collector のアナリティクス検証

## ディスカバリーセッションの開始

ソースコードからメソッドやパラメータを特定できるアプリケーション開発者がいない場合があります。しかし、AppDynamics から直接アプリケーションのメソッドやオブジェクトを検出するアプローチがあります。

1. 画面左上の **Applications** タブを選択します。
2. **Supercar-Trader-YOURINITIALS** アプリケーションを選択します。
3. **Configuration** タブを選択します。
4. **Instrumentation** リンクをクリックします。
5. **Transaction Detection** タブを選択します。
6. 右側の **Live Preview Button** をクリックします。

![OpenDiscoverySession](images/05-live-preview.png)

7. **Start Discovery Session** ボタンをクリックします。
8. ポップアップウィンドウで **Web-Portal Node** を選択します。調査しているメソッドが実行されているノードと同じものを選択してください。
9. **Ok** をクリックします。

![OpenDiscoverySession](images/05-biq-trans-disco.png)

10. 右側のトグルで **Tools** を選択します。
11. ドロップダウンリストで **Classes/Methods** を選択します。
12. **Search** セクションで **Classes** with name を選択します。
13. テキストボックスにクラス名 **supercars.dataloader.CarDataLoader** を入力します。クラス名を見つけるには、コールグラフを検索するか、理想的にはソースコードで確認します。
14. **Apply** をクリックして、一致するクラスメソッドを検索します。
15. 結果が表示されたら、検索に一致するクラスを展開します。
16. **saveCar** メソッドを探します。

![OpenDiscoverySession](images/05-biq-trans-disco-config.png)

**saveCar** メソッドは入力パラメータとして **CarForm** オブジェクトを受け取ることに注意してください。

## オブジェクトへのドリルダウン

メソッドが見つかったので、そのパラメータを調べて車の詳細プロパティをどこから取得できるかを確認します。

**saveCar** メソッドは、入力パラメータとして複合オブジェクト **CarForm** を受け取ることがわかりました。このオブジェクトは、アプリケーションの Web ページで入力されたフォームデータを保持します。次に、このオブジェクトを調べて、そこから車の詳細情報を取得する方法を見つける必要があります。

1. テキストボックスに入力オブジェクトのクラス名 **supercars.form.CarForm** を入力します。
2. **Apply** をクリックしてクラスメソッドを検索します。
3. 結果が表示されたら、検索に一致する **supercars.form.CarForm** クラスを展開します。
4. 必要な車の詳細情報を返すメソッドを探します。price、model、color などの **get** メソッドが見つかります。

![ObjectDrillDown](images/05-biq-object-drilldown.png)

## Method Invocation Data Collector の作成

前の演習での発見を基に、実行時に動作中のコードから直接車の詳細情報を取得する method invocation data collector を設定できます。

1. **Applications** タブを選択します。
2. **Supercar-Trader-YOURINITIALS** アプリケーションを選択します。
3. **Configuration** タブを選択します。
4. **Instrumentation** リンクをクリックします。
5. **Data Collectors** タブを選択します。
6. **Method Invocation Data Collectors** で **Add** をクリックします。

![MIDCDataCollector](images/05-biq-method-collector.png)

車の詳細情報をキャプチャする method invocation data collector を作成します。

7. **Name** に **SellCarMI-YOURINITIALS** を指定します。
8. **Transaction Snapshots** を有効にします。
9. **Transaction Analytics** を有効にします。
10. **with a Class Name that** を選択します。
11. **Class Name** として **supercars.dataloader.CarDataLoader** を追加します。
12. **Method Name** として **saveCar** を追加します。

![NewMIDCDataCollector](images/05-biq-midc-config.png)

観察したとおり、SaveCar メソッドの Index 0 の入力パラメータはクラス **CarForm** のオブジェクトであり、そのオブジェクト内には **getPrice()** などの車の詳細プロパティを返す Getter メソッドがあります。

MIDC でその値をどのように取得するかを説明するため、以下の手順を実行します

13. MIDC パネルの下部にある **Add** をクリックして、収集する新しいデータを指定します。
14. Display Name に **CarPrice_MIDC** を指定します。
15. Collect Data From で **Method Parameter of Index 0**（**CarForm Object**）を選択します。
16. **Operation on Method Parameter** で **Use Getter Chain** を選択します。CarForm 内のメソッドを呼び出して車の詳細情報を返します。
17. **CarForm** クラス内の価格を返す Getter メソッド **getPrice()** を指定します。
18. **Save** をクリックします。

![CreateMIDCDataCollector1](images/05-biq-midc-datacoll.png)

19. color、model、その他収集したいプロパティについて、上記の手順を繰り返します。

![CreateMIDCDataCollector2](images/05-biq-midc-details.png)

20. **Save MIDC** をクリックし、**"/Supercar-Trader/sell.do"** ビジネストランザクションに適用します。

MIDC の実装には JVM の再起動が必要です

1. EC2 インスタンスに SSH で接続します。
2. Tomcat サーバーをシャットダウンします。

``` bash
cd /usr/local/apache/apache-tomcat-9/bin
./shutdown.sh
```

アプリケーション JVM がまだ実行中の場合は、以下のコマンドで残りの JVM を停止します。

{{< tabs >}}
{{% tab title="Command" %}}

``` bash
sudo pkill -f Supercar-Trader
```

{{% /tab %}}
{{< /tabs >}}

3. Tomcat サーバーを再起動します。

``` bash
./startup.sh
```

4. Tomcat サーバーが実行中であることを確認します。これには数分かかる場合があります。

{{< tabs >}}
{{% tab title="Command" %}}

``` bash
curl localhost:8080
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <title>Apache Tomcat/9.0.50</title>
        <link href="favicon.ico" rel="icon" type="image/x-icon" />
        <link href="tomcat.css" rel="stylesheet" type="text/css" />
    </head>

    <body>
        <div id="wrapper"
....
```

{{% /tab %}}
{{< /tabs >}}

## MD パラメータのアナリティクス検証

Web サイトにアクセスし、Sell Car ページでフォームを数回送信して手動で負荷をかけます。

ビジネスデータが AppDynamics Analytics の HTTP data collector によってキャプチャされたかどうかを確認します。

1. **Analytics** タブを選択します。
2. **Searches** タブを選択し、新しい **Drag and Drop Search** を追加します。
3. **+ Add** ボタンをクリックして新しい **Drag and Drop Search** を作成します。
4. **+ Add Criteria** をクリックします。
5. **Application** を選択し、アプリケーション名 **Supercar-Trader-YOURINITIALS** を検索します。
6. **Custom Method Data** にフィールドとして **Business Parameters** が表示されていることを確認します。
7. **CarPrice Field** にデータがあることを確認します。

![ValidateMIDCDataCollector](images/05-biq-search-results.png)

## まとめ

これで、実行時にノードから Sell Car トランザクションのビジネスデータをキャプチャできるようになりました。このデータは、AppDynamics のアナリティクスおよびダッシュボード機能で使用して、ビジネスにより多くのコンテキストを提供し、ビジネスに対する IT の影響を測定することができます。
