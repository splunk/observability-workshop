---
title: 7. Tag Spotlightの使用
linkTitle: 7. Tag Spotlightの使用
weight: 7
isCJKLanguage: true
---

* より深く分析のために様々なエンドポイントのメトリクスビューを調査したりTag spotlightに送信されたTagを使用します。

---

## 1. CartエンドポイントのURLを探す

RUMの概要ページから、**Cart** エンドポイントのURLを選択し、このエンドポイントで利用可能な情報をさらに深く掘り下げてみてください。

![RUM-Cart2](../images/RUM-select-cart.png)

青色のURLをクリックすると、 **Tag Spotlight** の概要に遷移します。

![RUM-Tag](../images/RUM-TAG-Overview.png)

ここでは、RUM トレースの一部として Splunk RUM に送信されたすべてのタグが表示されます。表示されるタグは、あなたが選択した概要に関連するものです。これらはトレースが送信されたときに自動的に作成された一般的なタグと、ウェブサイトの設定の一部でトレースに追加した追加タグです。

{{% notice title="追加タグ" color="info" %}}
既に2つの追加タグを送信しています。それは皆さんのウェブサイトに追加された *Beacon url* に定義されている *app: "[nodename]-store", environment: "[nodename]-workshop"* です（詳しくは後で確認します）。同様の方法で、タグを追加することができます。
{{% /notice %}}

この例では、以下のように **Document Load Latency** ビューを選択しています。

![RUM-Header](../images/RUM-Selection.png)

特定のメトリクスにフォーカスした以下のタグビューのいずれかを選択することができます。

![RUM-views](../images/RUM-Tag-views.png)

---

## 2. Tag Spotlight内の情報を探索

Tag Spotlightは、チャートビューで異常値を確認したり、タグで問題を特定するのに役立つように設計されています。

**Document Load Latency** ビューで、**Browser** 、 **Browser Version** 、 **OS Name** タグビューを見ると、様々なブラウザーの種類とバージョン、そして基盤となるOSを確認することができます。
これにより、特定のブラウザやOSのバージョンに関連する問題が強調表示されるため、特定が容易になります。

![RUM-Tag2](../images/RUMBrowserTags.png)

上記の例では、Firefoxのレスポンスが最も遅く、様々なバージョンのブラウザ（Chrome）のレスポンスが異なること、Android端末のレスポンスが遅いことが分かります。

さらに、ISPや場所などに関連する問題を特定するために使用できる地域タグがあります。ここでは、Online Boutiqueにアクセスするために使用している場所を見つけることができます。以下のように、Online Boutiqueにアクセスしている都市や国をクリックしてドリルダウンしてください（City内のAmsterdam）。

![RUM-click](../images/RUM-Region.png)

以下のように選択した都市に関連するトレースのみが選択されます。

![RUM-Adam](../images/RUM-Adam.png)

様々なタグを選択することでフィルターを構築することができ、現在の選択項目も確認できます。

![RUM-Adam](../images/RUM-Filter.png)

フィルタを解除してすべてのトレースを表示するには、ページ右上の **Clear All** をクリックしてください。

概要ページが空であるか、 ![RUM-Adam](../images/RUM-NoTime.png) と表示されている場合、選択したタイムスロットでトレースが受信されていないことを示します。
左上のタイムウィンドウを広げる必要があります。例えば、*Last 12 hours* で調べることができます。

下の図のように表示したい時間帯を選択し、小さな虫眼鏡のアイコンをクリックして時間フィルタをセットにすることができます。

![RUM-time](../images/RUM-TimeSelect.png)
