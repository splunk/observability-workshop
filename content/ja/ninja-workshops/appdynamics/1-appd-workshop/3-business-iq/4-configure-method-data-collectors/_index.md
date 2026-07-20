---
title: Method Data Collectorの設定
time: 2 minutes
weight: 4
description: この演習では、WebブラウザからAppDynamics Controllerにアクセスし、Agentless Analyticsを有効にします。
---
Method invocation data collectorは、メソッドの引数、変数、戻り値などのコードデータをキャプチャします。HTTP data collectorでは十分なビジネスデータが取得できない場合でも、コード実行からこれらの情報をキャプチャできます。

この演習では、以下のタスクを実行します。

* メソッドを検出する
* ディスカバリーセッションを開く
* メソッドパラメータを検出する
* コード内のオブジェクトにドリルダウンする
* Method invocation data collectorを作成する
* Method invocation data collectorのアナリティクスを検証する

## ディスカバリーセッションを開く

アプリケーション開発者がソースコードからメソッドやパラメータを特定できない場合があります。しかし、AppDynamicsから直接アプリケーションのメソッドやオブジェクトを検出するアプローチがあります。

1. 画面左上の **Applications** タブを選択します。
2. **Supercar-Trader-YOURINITIALS** アプリケーションを選択します。
3. **Configuration** タブを選択します。
4. **Instrumentation** リンクをクリックします。
5. **Transaction Detection** タブを選択します。
6. 右側の **Live Preview Button** をクリックします。

![OpenDiscoverySession](images/05-live-preview.png)

1. **Start Discovery Session** ボタンをクリックします。
2. ポップアップウィンドウで **Web-Portal Node** を選択します。調査しているメソッドが実行されているノードと同じノードである必要があります。
3. **Ok** をクリックします。

![OpenDiscoverySession](images/05-biq-trans-disco.png)

1. 右側のトグルで **Tools** を選択します。
2. ドロップダウンリストで **Classes/Methods** を選択します。
3. **Search** セクションで **Classes** with nameを選択します。
4. テキストボックスにクラス名 **supercars.dataloader.CarDataLoader** を入力します。クラス名を見つけるには、コールグラフを検索するか、理想的にはソースコードで見つけます。
5. **Apply** をクリックして、一致するクラスメソッドを検索します。
6. 結果が表示されたら、検索に一致するクラスを展開します。
7. 同じメソッド **saveCar** を探します。

![OpenDiscoverySession](images/05-biq-trans-disco-config.png)

**saveCar** メソッドが入力パラメータとして **CarForm** オブジェクトを受け取ることに注目してください。

## オブジェクトへのドリルダウン

メソッドが見つかったので、そのパラメータを調べて車の詳細プロパティを取得できる場所を確認します。

**saveCar** メソッドが複合オブジェクト **CarForm** を入力パラメータとして受け取ることがわかりました。このオブジェクトには、アプリケーションのWebページで入力されたフォームデータが保持されます。次に、そのオブジェクトを検査して、車の詳細を取得する方法を確認する必要があります。

1. テキストボックスに入力オブジェクトのクラス名 **supercars.form.CarForm** を入力します。
2. **Apply** をクリックしてクラスメソッドを検索します。
3. 結果が表示されたら、検索に一致する **supercars.form.CarForm** クラスを展開します。
4. 取得したい車の詳細を返すメソッドを探します。price、model、colorなどの **get** メソッドが見つかります。

![ObjectDrillDown](images/05-biq-object-drilldown.png)

## Method Invocation Data Collectorの作成

前の演習で得た情報を使って、実行時にコードから車の詳細を直接取得するmethod invocation data collectorを設定できます。

1. **Applications** タブを選択します。
2. **Supercar-Trader-YOURINITIALS** アプリケーションを選択します。
3. **Configuration** タブを選択します。
4. **Instrumentation** リンクをクリックします。
5. **Data Collectors** タブを選択します。
6. **Method Invocation Data Collectors** で **Add** をクリックします。

![MIDCDataCollector](images/05-biq-method-collector.png)

車の詳細をキャプチャするためのmethod invocation data collectorを作成します。

1. **Name** に **SellCarMI-YOURINITIALS** を指定します。
2. **Transaction Snapshots** を有効にします。
3. **Transaction Analytics** を有効にします。
4. **with a Class Name that** を選択します。
5. **Class Name** に **supercars.dataloader.CarDataLoader** を追加します。
6. **Method Name** に **saveCar** を追加します。

![NewMIDCDataCollector](images/05-biq-midc-config.png)

確認した通り、SaveCarメソッドのIndex 0の入力パラメータはクラス **CarForm** のオブジェクトであり、そのオブジェクト内には **getPrice()** などの車の詳細プロパティを返すGetterメソッドがあります。

MIDCでその値を取得する方法を以下に説明します。

1. MIDCパネルの下部にある **Add** をクリックして、収集する新しいデータを指定します。
2. Display Nameに **CarPrice_MIDC** を指定します。
3. Collect Data Fromで **Method Parameter of Index 0**（**CarForm Object**）を選択します。
4. **Operation on Method Parameter** で **Use Getter Chain** を選択します。CarForm内のメソッドを呼び出して車の詳細を返します。
5. **CarForm** クラス内のpriceを返すGetterメソッド **getPrice()** を指定します。
6. **Save** をクリックします。

![CreateMIDCDataCollector1](images/05-biq-midc-datacoll.png)

1. color、modelなど、データを収集したいすべてのプロパティについて上記の手順を繰り返します。

![CreateMIDCDataCollector2](images/05-biq-midc-details.png)

1. **Save MIDC** をクリックし、 **"/Supercar-Trader/sell.do"** ビジネストランザクションに適用します。

MIDCの実装にはJVMの再起動が必要です。

1. EC2インスタンスにSSHで接続します。
2. Tomcatサーバーをシャットダウンします。

``` bash
cd /usr/local/apache/apache-tomcat-9/bin
./shutdown.sh
```

まだ実行中のアプリケーションJVMが残っている場合は、以下のコマンドで残りのJVMを終了します。

{{< tabs >}}
{{% tab title="コマンド" %}}

``` bash
sudo pkill -f Supercar-Trader
```

{{% /tab %}}
{{< /tabs >}}

1. Tomcatサーバーを再起動します。

``` bash
./startup.sh
```

1. Tomcatサーバーが実行中であることを確認します。数分かかる場合があります。

{{< tabs >}}
{{% tab title="コマンド" %}}

``` bash
curl localhost:8080
```

{{% /tab %}}
{{% tab title="出力例" %}}

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

## MDパラメータのアナリティクス検証

Webサイトにアクセスし、Sell Carページでフォームを数回送信して手動で負荷をかけます。

HTTP data collectorによってビジネスデータがAppDynamics Analyticsでキャプチャされたかどうかを確認します。

1. **Analytics** タブを選択します。
2. **Searches** タブを選択し、新しい **Drag and Drop Search** を追加します。
3. **+ Add** ボタンをクリックして、新しい **Drag and Drop Search** を作成します。
4. **+ Add Criteria** をクリックします。
5. **Application** を選択し、アプリケーション名 **Supercar-Trader-YOURINITIALS** を検索します。
6. **Custom Method Data** のフィールドとして **Business Parameters** が表示されることを確認します。
7. **CarPrice Field** にデータがあることを確認します。

![ValidateMIDCDataCollector](images/05-biq-search-results.png)

## まとめ

実行時にノードからSell Carトランザクションのビジネスデータをキャプチャできました。このデータは、AppDynamicsのAnalyticsおよびDashboard機能で使用して、ビジネスにより多くのコンテキストを提供し、ビジネスに対するITの影響を測定できます。
