---
title: 4. Synthetics Detector
weight: 4
---
テストを24時間365日実行できるため、ソーシャルメディアや稼働監視サイトから知らされる前に、テストが失敗したり、合意したSLAよりも長く実行されていることを早期に警告してもらうための理想的なツールです。

![Social media](../images/social-media-post.png)

それを防ぐために、テストが1.1分以上かかっているかどうかを検出しましょう。

{{% notice title="Exercise" style="green" icon="running" %}}

* 左側のメニューから Synthetics ホームページに戻ります
* 再度ワークショップのテストを選択し、ページ上部の {{% button %}}**Create Detector**{{% /button %}} ボタンをクリックします

  ![synth detector](../images/synth-detector.png)
* **New Synthetics Detector** **(1)** のテキストを編集し、`INITIALS - [WORKSHOPNAME]` に置き換えます
* アラート条件を変更して、メトリクスを Run Duration（Uptime ではなく）に、条件を Static Threshold に設定します
* **Trigger threshold** **(2)** を `65,000` から `68,000` 程度に設定し、Enter キーを押してチャートを更新します。上記のように、閾値ラインを超えるスパイクが複数あることを確認してください（実際のレイテンシに合わせて閾値を少し調整する必要があるかもしれません）
* 残りの設定はデフォルトのままにします
* スパイクの下に赤と白の三角形の列が表示されていることに注目してください **(3)**。赤い三角形は、ディテクターがテストが指定した閾値を超えたことを検出したことを示し、白い三角形は結果が閾値を下回ったことを示します。赤い三角形ごとにアラートがトリガーされます
* ドロップダウンを変更して Alerts の重大度 **(4)** を別のレベルに変更したり、アラートの方法を変更したりできます。Recipient は追加**しないでください**。アラートの嵐に見舞われる可能性があります！
* {{% button style="blue" %}}Activate{{% /button %}} をクリックしてディテクターをデプロイします
* 新しく作成したディテクターを確認するには、{{% button %}}Edit Test{{% /button %}} ボタンをクリックします
* ページの下部にアクティブなディテクターのリストがあります

  ![list of detectors](../images/detector-list.png)

* 自分のディテクターが見つからず、*New Synthetic Detector* というものがある場合は、自分の名前で正しく保存されていない可能性があります。*New Synthetic Detector* リンクをクリックして、名前の変更をやり直してください
* {{% button %}}Close{{% /button %}} ボタンをクリックして編集モードを終了します
{{% /notice %}}
