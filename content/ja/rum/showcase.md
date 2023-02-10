---
title: Online BoutiqueでのRUMの利用
weight: 3
menu:
  docs:
    weight: 3
isCJKLanguage: true
---
* Online Boutiqueのアドレスを探します
* Online Boutiqueのウェブショップで買い物しトラフィックを生成させます

---

## 1. RUMが有効化されたOnline BoutiqueのURL

前のセクションで説明したように、RUMホスト上で動作するOnline Boutiqueを使用します。
RUMのみのワークショップに参加される方は、使用するシステムは既に準備されていますので、RUMインスタンスのURLを受け取った後、セクション4 [Online Boutiqueを使ってシステムに負荷を与える](./#4-online-boutiqueを使ってシステムに負荷を与える) まで進むことができます。


## 2. RUM Access Token の入手

APMワークショップでサービスをインストールしました。これから、RUM機能もデプロイメントに追加していきます。

まず、RUM Authorization スコープを持つ RUM_ACCESS_TOKEN を取得する必要があります。ワークショップのRUM Access Tokenは、 **settings** ![settings](../images/setting.png) メニューボタンをクリックし、 **Access Tokens** を選択することで見つけることができます。

講師が使用するように指示したRUMワークショップトークン（例： **O11y-Workshop-RUM-TOKEN** ）を展開し、 **Show Token** をクリックしてトークンを表示します。 {{% labelbutton color="ui-button-grey" %}}Copy{{% /labelbutton %}} ボタンをクリックし、クリップボードにコピーしてください。 **Default** トークンは使用しないでください。トークンのAuthorization ScopeがRUMであることを確認してください。

![Access Token](../images/RUM-Access-Token.png)

{{% notice title="自分のトークンを作らないでください" color="warning" %}}
このワークショップのために、皆さんが行う演習に適した設定をしたRUM Tokenを作成ししています。
{{% /notice %}}

進行中のシェルスクリプトで環境変数 `RUM_TOKEN` を作成し、デプロイメントをパーソナライズします。

{{< tabs >}}
{{< tab name="Export Variables" lang="sh" >}}
export RUM_TOKEN=<replace_with_O11y-Workshop-RUM-TOKEN>
{{< /tab >}}
{{< /tabs >}}

## 3. RUMを組み込んだOnline Boutiqueのデプロイ

EC2インスタンスのkubernetes（K3s）にOnline Boutiqueのアプリケーションをデプロイするには、元のデプロイメントを削除し、RUM用のapm configスクリプトを実行し、RUMのデプロイメントを適用します。

{{< tabs >}}
{{< tab name="Deploy Online Boutique with RUM" lang="sh" >}}
cd ~/workshop/apm
kubectl delete -f deployment.yaml
./apm-config.sh -r
kubectl apply -f deployment.yaml
{{< /tab >}}
{{< tab name="Partial Deployment Output" lang= "text" >}}
......
Adding RUM_TOKEN to deployment
deployment.apps/recommendationservice created
service/recommendationservice created
deployment.apps/productcatalogservice created
service/productcatalogservice created
deployment.apps/cartservice created
service/cartservice created
deployment.apps/adservice created
service/adservice created
deployment.apps/paymentservice created
service/paymentservice created
deployment.apps/loadgenerator created
service/loadgenerator created
deployment.apps/shippingservice created
service/shippingservice created
deployment.apps/currencyservice created
service/currencyservice created
deployment.apps/redis-cart created
service/redis-cart created
deployment.apps/checkoutservice created
service/checkoutservice created
deployment.apps/frontend created
service/frontend created
service/frontend-external created
deployment.apps/emailservice created
service/emailservice created
deployment.apps/rum-loadgen-deployment created
{{< /tab >}}
{{< /tabs >}}

{{% notice title="変数未セットに関するメッセージが表示された場合" color="warning" %}}
**kubectl delete -f deployment.yaml** コマンドを実行しAPM環境のデプロイ削除します。
次にガイド、メッセージに表示されていた変数をexportし上記のデプロイスクリプトを再実行します。
{{% /notice %}}

## 4. Online Boutiqueを使ってシステムに負荷を与える
皆さんと一緒にOnline Boutiqueに接続し買い物をシミュレートする合成ユーザーもいます。これにより、複数の場所からのトラフィックが発生し、よりリアルなデータが得られます。

ワークショップ講師からURLを受け取っているはずです。
新しいWebブラウザを立ち上げ `http://{==RUM-HOST-EC2-IP==}:81/` にアクセスするとRUMが有効化されたOnline Boutiqueが表示されます。

![Online Boutique](../images/online-boutique.png)

## 5. トラフィックを発生させる

この演習の目的は、RUMが有効化されたOnline Boutiqueを閲覧し、さまざまな商品と数量の組み合わせで購入することです。
さらに別のブラウザやスマートフォンからアクセスすることもできます。

これにより複数のセッションが作成され、調査することができます。じっくりと吟味して、いろいろな商品を購入しカートに入れてください。

![Cart Online Boutique](../images/cart.png)

Home Barista Kitよくないですか？...  ショッピングを楽しんでください！

![Clock](../images/Clock.gif)
