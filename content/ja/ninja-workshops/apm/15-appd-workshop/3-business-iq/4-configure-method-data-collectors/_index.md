---
title: メソッドデータコレクターの設定
time: 2 minutes
weight: 4
description: この演習では、Web ブラウザから AppDynamics Controller にアクセスし、そこから Agentless Analytics を有効化します。
---
メソッド呼び出しデータコレクターは、メソッドの引数、変数、戻り値などのコードデータをキャプチャします。HTTP データコレクターで十分なビジネスデータが取得できない場合でも、コード実行からこれらの情報をキャプチャできます。

この演習では、以下のタスクを実行します。

* メソッドを検出する。
* ディスカバリーセッションを開く。
* メソッドのパラメーターを検出する。
* コード内のオブジェクトをドリルダウンする。
* メソッド呼び出しデータコレクターを作成する。
* メソッド呼び出しデータコレクターのアナリティクスを検証する。

## ディスカバリーセッションを開く

ソースコードからメソッドやパラメーターを特定できるアプリケーション開発者がいない場合もあります。しかし、AppDynamics から直接アプリケーションのメソッドやオブジェクトを検出する方法があります。

1. 画面左上の **Applications** タブを選択します。
2. **Supercar-Trader-YOURINITIALS** アプリケーションを選択します。
3. **Configuration** タブを選択します。
4. **Instrumentation** リンクをクリックします。
5. **Transaction Detection** タブを選択します。
6. 右側の **Live Preview Button** をクリックします。

![OpenDiscoverySession](images/05-live-preview.png)

1. **Start Discovery Session** ボタンをクリックします。
2. ポップアップウィンドウで **Web-Portal Node** を選択します。これは、調査対象のメソッドが実行されているノードと同じである必要があります。
3. **Ok** をクリックします。

![OpenDiscoverySession](images/05-biq-trans-disco.png)

1. 右側のトグルで **Tools** を選択します。
2. ドロップダウンリストで **Classes/Methods** を選択します。
3. **Search** セクションで **Classes** with name を選択します。
4. テキストボックスにクラス名 **supercars.dataloader.CarDataLoader** を入力します。クラス名を見つけるには、コールグラフを検索するか、できればソースコードから探します。
5. **Apply** をクリックして、一致するクラスメソッドを検索します。
6. 結果が表示されたら、検索に一致するクラスを展開します。
7. **saveCar** メソッドを探します。

![OpenDiscoverySession](images/05-biq-trans-disco-config.png)

**saveCar** メソッドは入力パラメーターとして **CarForm** オブジェクトを受け取ることに注意してください。

## オブジェクトへのドリルダウン

メソッドが見つかりましたので、そのパラメーターを調べて、車の詳細プロパティをどこから取得できるかを確認します。

**saveCar** メソッドが入力パラメーターとして複合オブジェクト **CarForm** を受け取ることが分かりました。このオブジェクトには、アプリケーションの Web ページで入力されたフォームデータが格納されます。次に、そのオブジェクトを検査して、そこから車の詳細を取得する方法を確認する必要があります。

1. テキストボックスに入力オブジェクトのクラス名 **supercars.form.CarForm** を入力します。
2. **Apply** をクリックしてクラスメソッドを検索します。
3. 結果が表示されたら、検索に一致する **supercars.form.CarForm** クラスを展開します。
4. 必要な車の詳細を返すメソッドを探します。価格、モデル、色などの **get** メソッドが見つかります。

![ObjectDrillDown](images/05-biq-object-drilldown.png)

## メソッド呼び出しデータコレクターの作成

これまでの演習で得た情報をもとに、メソッド呼び出しデータコレクターを設定して、ランタイムで実行中のコードから直接車の詳細を取得できます。

1. **Applications** タブを選択します。
2. **Supercar-Trader-YOURINITIALS** アプリケーションを選択します。
3. **Configuration** タブを選択します。
4. **Instrumentation** リンクをクリックします。
5. **Data Collectors** タブを選択します。
6. **Method Invocation Data Collectors** で **Add** をクリックします。

![MIDCDataCollector](images/05-biq-method-collector.png)

車の詳細をキャプチャするためのメソッド呼び出しデータコレクターを作成します。

1. **Name** には **SellCarMI-YOURINITIALS** を指定します。
2. **Transaction Snapshots** を有効化します。
3. **Transaction Analytics** を有効化します。
4. **with a Class Name that** を選択します。
5. **Class Name** として **supercars.dataloader.CarDataLoader** を追加します。
6. **Method Name** として **saveCar** を追加します。

![NewMIDCDataCollector](images/05-biq-midc-config.png)

確認したように、SaveCar メソッドのインデックス 0 の入力パラメーターは **CarForm** クラスのオブジェクトであり、そのオブジェクト内に **getPrice()** などの車の詳細プロパティを返す Getter メソッドがあります。

そのため、MIDC でその値を取得する方法を説明するために、以下の手順を実行します。

1. MIDC パネルの下部にある **Add** をクリックして、収集したい新しいデータを指定します。
2. Display Name には **CarPrice_MIDC** を指定します。
3. Collect Data From では、**Method Parameter of Index 0** を選択します。これは **CarForm Object** です。
4. **Operation on Method Parameter** には、**Use Getter Chain** を選択します。CarForm 内のメソッドを呼び出して車の詳細を取得します。
5. 次に、**CarForm** クラス内で価格を返す Getter メソッドである **getPrice()** を指定します。
6. **Save** をクリックします。

![CreateMIDCDataCollector1](images/05-biq-midc-datacoll.png)

1. 上記の手順を、色、モデル、その他データを収集したいすべてのプロパティに対して繰り返します。

![CreateMIDCDataCollector2](images/05-biq-midc-details.png)

1. **Save MIDC** をクリックして、**”/Supercar-Trader/sell.do”** ビジネストランザクションに適用します。

MIDC を反映させるには、JVM を再起動する必要があります。

1. EC2 インスタンスに SSH 接続します。
2. Tomcat サーバーをシャットダウンします。

``` bash
cd /usr/local/apache/apache-tomcat-9/bin
./shutdown.sh
```

アプリケーションの JVM がまだ実行中の場合は、以下のコマンドで残りの JVM を強制終了します。

{{< tabs >}}
{{% tab title="Command" %}}

``` bash
sudo pkill -f Supercar-Trader
```

{{% /tab %}}
{{< /tabs >}}

1. Tomcat サーバーを再起動します。

``` bash
./startup.sh
```

1. Tomcat サーバーが起動していることを確認します。これには数分かかる場合があります。

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

## MD パラメーターのアナリティクスを検証する

Web サイトにアクセスし、Sell Car ページでフォームを数回送信して、手動で負荷をかけます。

次に、AppDynamics Analytics で HTTP データコレクターによってビジネスデータがキャプチャされたかどうかを確認します。

1. **Analytics** タブを選択します。
2. **Searches** タブを選択し、新しい **Drag and Drop Search** を追加します。
3. **+ Add** ボタンをクリックして、新しい **Drag and Drop Search** を作成します。
4. **+ Add Criteria** をクリックします。
5. **Application** を選択し、アプリケーション名 **Supercar-Trader-YOURINITIALS** を検索します。
6. **Custom Method Data** に **Business Parameters** がフィールドとして表示されることを確認します。
7. **CarPrice Field** にデータが入っていることを確認します。

![ValidateMIDCDataCollector](images/05-biq-search-results.png)

## まとめ

これで、ランタイム中のノードから Sell Car トランザクションのビジネスデータをキャプチャできました。このデータは、AppDynamics 内のアナリティクスやダッシュボード機能で利用でき、ビジネスへのコンテキスト提供や、IT がビジネスに与える影響の測定に役立ちます。
