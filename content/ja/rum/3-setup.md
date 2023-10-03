---
title: 3. 自分のWebサイトでRUMを有効化する場合の例
linkTitle: 3. 自分のWebサイトでRUMを使う
weight: 3
isCJKLanguage: true
---

* ブラウザでOnline BoutiqueのウェブページのオリジナルのHEADセクション（またはここにある例を使用）をチェックします
* ワークショップ Online Boutique の Webアドレスを検索します
* Online Boutiqueに加えられた変更を確認します

---

## 1. RUMなしのOnline Boutiqueのオリジナルコードを確認する

APMセッションの一部でEC2インスタンスにOnline Boutiqueをインストールしていれば、ポート番号81でサイトにアクセスできます。

Online BoutiqueがインストールされたEC2インスタンスにアクセスできない場合は、講師からRUMがインストールされていないOnline BoutiqueのURLを教えてもらい、次のステップに進んでください。

## 2. RUM Access Tokenの入手

これから行うデプロイメントは、RUM ワークショップセクションの一部としても使用されます。Splunk UIからRUM Access Tokenを取得する必要があります。ワークショップのアクセストークンは、左下の **>>** をクリックし ![settings](../images/setting.png) メニューをクリックして、 **Settings → Access Tokens** を選択すると見つけることができます。

講師が使用するように指示したRUMワークショップトークン（例： **O11y-Workshop-RUM-TOKEN** ）を展開し、 **Show Token** をクリックしてトークンを公開します。 {{% button style="grey" %}}Copy{{% /button %}} ボタンをクリックし、クリップボードにコピーしてください。 **Default** のトークンは使用しないでください。トークンのAuthorization ScopeがRUMであることを確認してください。

![Access Token](../images/RUM-Access-Token.png)

{{% notice title="新規にトークンを作らないでください" color="warning" %}}
このワークショップのために、皆さんが行う演習に適した設定をしたRUM Tokenを作成しています。
{{% /notice %}}

EC2にSSHアクセスしているシェルスクリプトで環境変数 `RUM_TOKEN` を作成し、デプロイメントをパーソナライズします。

{{< tabs >}}
{{% tab title="Export Variables" %}}

```bash
export RUM_TOKEN=<replace_with_O11y-Workshop-RUM-TOKEN>
```

{{% /tab %}}
{{< /tabs >}}

## 2. Online Boutiqueのデプロイ

Online BoutiqueアプリケーションをK3sにデプロイするには、apm configスクリプトを実行し、デプロイを適用してください。

{{< tabs >}}
{{% tab title="Deploy Online Boutique" %}}

```bash
cd ~/workshop/apm
kubectl apply -f deployment.yaml
```

{{% /tab %}}
{{% tab title="Deployment Output"  %}}

``` text
deployment.apps/checkoutservice created
service/checkoutservice created
deployment.apps/redis-cart created
service/redis-cart created
deployment.apps/productcatalogservice created
service/productcatalogservice created
deployment.apps/loadgenerator created
service/loadgenerator created
deployment.apps/frontend created
service/frontend created
service/frontend-external created
deployment.apps/paymentservice created
service/paymentservice created
deployment.apps/emailservice created
service/emailservice created
deployment.apps/adservice created
service/adservice created
deployment.apps/cartservice created
service/cartservice created
deployment.apps/recommendationservice created
service/recommendationservice created
deployment.apps/shippingservice created
service/shippingservice created
deployment.apps/currencyservice created
service/currencyservice created
```

{{% /tab %}}
{{< /tabs >}}

{{% notice title="変数未セットに関するメッセージが表示された場合" color="warning" %}}
**kubectl delete -f deployment.yaml** コマンドを実行しAPM環境のデプロイ削除します。
次にガイド、メッセージに表示されていた変数をexportし上記のデプロイスクリプトを再実行します。
{{% /notice %}}

ウェブブラウザーを起動し、Online Boutiqueにアクセスします。 (以前使用したもの、または新しくワークショップ講師が提供したもの）。RUMなしのOnline Boutiqueが起動していることが確認できます。

![Online Boutique](../images/online-boutique.png)

下記のお使いのブラウザの説明に従ってください。

### 1.1 Chrome, FireFox & Microsoft Edge ユーザー - ページのソースを確認

Chrome、Firefox、Microsoft Edgeでは、Online Boutiqueのサイト上で右クリックすると、 **「ページのソースを表示」** のオプションが表示されます。

![Chrome-see-source](../images/Chrome-1.png)

これを選択すると、HTMLページのソースコードが別のタブで表示されます。

![Chrome-see-html](../images/Chrome-html.png)

成功すれば、 [2 - 変更前のHEADセクションの確認](./#2---変更前のheadセクションの確認) へ進みます。

### 1.2 Safari ユーザー - ページのソースを確認

Safariでは機能を有効化する必要がある場合があります。OS Xメニューバーの *Safari* の配下にある **「設定」** をクリックします。

![Safari-1](../images/Safari-1.png)

ダイアログがポップアップしますので、 **「詳細」** ペイン内の **「メニューバーに"開発"メニューを表示」** にチェックをいれ、ダイアログボックスを閉じます。

![Safari-2](../images/Safari-2.png)

Online Boutiqueを右クリックすると、「ページのソースを表示する」オプションが表示されるようになります。

![Safari-3](../images/Safari-3.png)

Online Boutiqueでそのオプションを選択すると、以下のようなHTMLソースコードが表示されます。

![Safari-html](../images/Safari-html.png)

成功すれば、 [2 - 変更前のHEADセクションの確認](./#2---変更前のheadセクションの確認) へ進みます。

### 1.3 Internet Explorer ユーザー - ページのソースを確認

Internet Explorer 11 をお使いの場合、この演習では Web/RUM 用のSplunk Open Telemetry JavaScriptの特定のバージョンが必要になるため、問題が発生する可能性があります。
ただし、Online Boutiqueサイトを右クリックすると、**「ソースを表示」** のオプションが表示され、必要な変更を確認することができます。

![IE-1](../images/IE-1.png)

Online Boutiqueでそのオプションを選択すると、以下のようなHTMLソースコードが表示されます。

![IE-2](../images/IE-2.png)

## 2 - 変更前のHEADセクションの確認

RUMのための変更は、WebページのHEADセクションで実施します。以下は、あなたのローカルのBaseバージョンにあるべきオリジナルの行です。

![Online Boutique](../images/ViewBase-HEAD-html.png)

Splunk または Open Telemetry Beacon (RUM Metrics と Traces を送信するために使用される関数) への参照はありません。

## 3. RUM有効Online Boutiqueのウェブ（URL）を探す

RUMで使用するOnline Boutiqueは、RUM有効インスタンスのIPアドレスの81番ポートで見ることができます。URLはワークショップの講師から提供されます。

このRUMのセッションでは、講師が用意したRUM有効Online Boutiqueにアクセスできます。新しいウェブブラウザを開き、 `http://{==RUM-HOST-EC2-IP==}:81/` にアクセスすると、RUM有効Online Boutiqueが動作しているのが見えます。ここでも、前のセクションで説明したように、HTMLページのソースを表示します。

## 4. RUMを有効にするために行った変更をHEADセクションで確認

RUMに必要な変更は、WebページのHEADセクションに配置されます。以下は、RUMを有効にするために必要な変更を加えたhostsの更新されたHEADセクションです。

![Online Boutique](../images/ViewRUM-HEAD-html.png)

最初の3行（赤色でマーク）は、RUMトレースを有効にするためにWebページのHEADセクションに追加されています。最後の3行（青色でマーク）はオプションで、カスタムRUMイベントを有効にするために使用します。

```html
<script src="https://cdn.signalfx.com/o11y-gdi-rum/latest/splunk-otel-web.js" type="text/javascript"></script>
<script>window.SplunkRum && window.SplunkRum.init({beaconUrl: "https://rum-ingest.eu0.signalfx.com/v1/rum",
        rumAuth: "1wCqZVUWIP5XSdNjPoQRFg", app: "ksnq-rum-app", environment: "ksnq-rum-env"});</script>
    <script>
    const Provider = SplunkRum.provider; 
    var tracer=Provider.getTracer('appModuleLoader');
</script>
```

* 最初の行は、Splunk Open Telemetry Javascript ファイルをダウンロードする場所を指定しています。*<https://cdn.signalfx.com/o11y-gdi-rum/latest/splunk-otel-web.js>*  (必要であれば、ローカルに読み込むこともできます)
* 2行目は、Beacon URLでトレースの送信先を定義しています。 `{beaconUrl: "https://rum-ingest.eu0.signalfx.com/v1/rum"`
* また、Access Tokenを追加しています。 `rumAuth: "1wCqZVUWIP5XSdNjPoQRFg"` (もちろんこれは例です。全てのアプリケーションに対して、複数のRUM Access Tokenを作成することができます。) *
* また、SPLUNK RUM UIで使用するために、アプリケーション名や環境などの識別タグをRUMトレースに追加するために使用されます。 `app: "ksnq-rum-app", environment: "ksnq-rum-env"}`

{{% notice title="Info" color="info" %}}
この例ではアプリ名は **ksnq-rum-app** ですが、これはワークショップでは異なるでしょう。RUMセッションで使用するアプリ名と環境は講師に確認し、メモしておいてください。
{{% /notice %}}

上記の2行だけであなたのWebサイトでRUMを有効にすることができます。

(青色の)オプションのセクションでは、 `var tracer=Provider.getTracer('appModuleLoader');` を使用して、すべてのページ変更に対してカスタムイベントを追加し、ウェブサイトのコンバージョンと使用状況をよりよく追跡できるようにします。
