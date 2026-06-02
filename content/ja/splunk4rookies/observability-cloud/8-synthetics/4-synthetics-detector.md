---
title: 4. Synthetics Detector
weight: 4
---
これらのテストは 24 時間 365 日実行できるため、SNS や Uptime のサイトから知らされるのではなく、テストが失敗したり、合意した SLA を超えて実行時間が長くなり始めた際に、いち早く警告を受けるための理想的なツールとなります。

![Social media](../images/social-media-post.png)

 そのような事態を防ぐため、テストの実行時間が 1.1 分を超えていないかを検知してみましょう。

 {{% exercise title="Synthetics Detector を作成する" %}}

* 左側のメニューから Synthetics のホームページに戻ります
* 再度ワークショップのテストを選択し、ページ上部の {{% button %}}**Create Detector**{{% /button %}} ボタンをクリックします。

  ![synth detector](../images/synth-detector.png)
* テキスト **New Synthetics Detector** **(1)** を編集し、`INITIALS - [WORKSHOPNAME]` に置き換えます。
* メトリックが Run Duration（Uptime ではなく）になり、条件が Static Threshold になるようにアラート条件を変更します。
* **Trigger threshold** **(2)** を `65,000` から `68,000` 程度に設定し、Enter キーを押してチャートを更新します。上記のように、しきい値の線を超えるスパイクが複数あることを確認してください（実際のレイテンシに合わせて、しきい値の値を多少調整する必要があるかもしれません）。
* それ以外はデフォルトのままにしておきます。
* スパイクの下に赤と白の三角形の列が表示されるようになっていることに注意してください **(3)**。赤い三角形は、Detector がテストが指定されたしきい値を超えていることを検出したことを示し、白い三角形は結果がしきい値を下回って戻ったことを示しています。各赤い三角形がアラートをトリガーします。
* ドロップダウンを別のレベルに変更することで、アラートの重要度 **(4)** および通知方法を変更できます。アラートの嵐に巻き込まれる可能性があるため、Recipient は **追加しない** ようにしてください！
* {{% button style="blue" %}}Activate{{% /button %}} をクリックして Detector をデプロイします。
* 新しく作成した Detector を確認するには、{{% button %}}Edit Test{{% /button %}} ボタンをクリックします
* ページの下部に、アクティブな Detector のリストが表示されます。

  ![list of detectors](../images/detector-list.png)

* 自分のものが見つからず、*New Synthetic Detector* というものが見える場合は、自分の名前で正しく保存できていない可能性があります。*New Synthetic Detector* のリンクをクリックし、リネームをやり直してください。
* {{% button %}}Close{{% /button %}} ボタンをクリックして編集モードを終了します。
{{% /exercise %}}
