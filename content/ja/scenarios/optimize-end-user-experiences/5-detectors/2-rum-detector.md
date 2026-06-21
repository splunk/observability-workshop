---
title: RUM Detectors
linkTitle: 2. RUM Detectors
weight: 2
hidden: false
---

サポートセンターからのチケットを待たずに、本番環境の問題を把握したいとしましょう。ここで [RUM でディテクターを作成する](https://docs.splunk.com/observability/en/rum/rum-alerts.html) ことが役立ちます。

1. アプリの RUM 概要に移動します。LCP チャートまでスクロールし、チャートメニューアイコンをクリックして、Create Detector をクリックします。
![RUM LCP chart with action menu flyout](../_img/rum-lcp.png)

1. ディテクターの名前に **チーム名** と **イニシャル** を含めるように変更し、ディテクターのスコープを App に変更して、単一の URL やページに限定されないようにします。時間枠内に少なくとも1つのアラートイベントが表示されるまで、しきい値と感度を調整します。
![RUM alert details](../_img/rum-detector.png)

1. アラートの重大度を変更し、必要に応じて受信者を追加して、{{% button style="blue" %}}Activate{{% /button %}} をクリックして Detector を保存します。

{{% notice title="Exercise" style="green" icon="running" %}}
ワークショップのインストラクターがウェブサイトに変更を加えます。問題をどのように発見し、どのように調査しますか？
{{% /notice %}}

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}
数分待ってから、ブラウザでオンラインストアのホームページを確認してください。シークレットブラウザウィンドウでの体験はどうですか？ページを更新するとどのように変わりますか？
{{% /notice %}}
