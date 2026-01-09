---
title: ダッシュボードへのチャートの追加
linkTitle: 1.09. Adding more charts
weight: 1.09
---

## 1. 既存のダッシュボードへの保存

チャートを保存する前に、左上隅で **YOUR_NAME-Dashboard: YOUR_NAME-Dashboard (1)** が選択されていることを確認してください。これにより、チャートが正しいダッシュボードに保存されます。

次に、チャートに名前を付けます。**Latency History** **(2)** と入力し、必要に応じて **Chart Description (3)** に簡単な説明を追加してください（例のように）。
![Save Chart 1](../../images/morecharts-1.png)

---
準備ができたら、{{% button style=blue %}}Save And Close{{% /button %}} ボタン **(4)** をクリックします。ダッシュボードに戻り、2つのチャートが含まれるようになります。
![Save Chart 2](../../images/morecharts-2.png)

---

## 2. チャートのコピーと貼り付け

次に、先ほど作成したチャートを複製して、別のチャートをすばやく追加しましょう。

ダッシュボードで **Latency History** チャートを見つけ、チャートの右上隅にある three dots **`...`** **(1)** をクリックします。メニューから **Copy (2)** を選択します。

コピー後、ページ上部の **+** アイコン **(3)** の前に小さな白い **1** が表示されます。これは、1つのチャートが貼り付け可能であることを示しています。
![Copy chart](../../images/morecharts-3.png)

---
ページ上部の **+** アイコン **(1)** をクリックし、ドロップダウンメニューで **(2)** を選択します。
その行の末尾にも **1** が表示され、コピーしたチャートが追加可能であることを確認できます。
![Past charts](../../images/morecharts-4.png)

これにより、前のチャートのコピーがダッシュボードに配置されます。
![Three Dashboard](../../images/morecharts-5.png)

---

## 3. 貼り付けたチャートの編集

複製したチャートを編集するには、ダッシュボード内の **Latency History** チャートの1つで three dots **`...`** をクリックし、**Open** を選択します。または、チャートのタイトル **Latency History** を直接クリックしてエディタで開くこともできます。

これにより、再びエディタ環境に移動します。

まず、チャートの右上隅にある時間範囲を調整します。最近のデータをより広く表示するために **Past 1 Hour (1)** に設定します。

次に、チャートをカスタマイズしてユニークにしましょう。**Signal A (2)** の横にある目のアイコンをクリックして、再び表示させます。
次に、**Signal C (3)** の目のアイコンをクリックして非表示にします。

チャートタイトルを *Latency history* から **Latency vs Load (4)** に更新し、必要に応じてチャートの説明を追加または編集して、更新されたフォーカスを反映させます **(5)**。
![Set Visibility](../../images/morecharts-6.png)

---
{{% button style=blue %}}Add Metric Or Event{{% /button %}} ボタンをクリックして、新しいシグナルを作成します。表示される入力フィールドに `demo.trans.count` **(1)** と入力して選択し、**Signal D** として追加します。

これにより、新しいシグナル **Signal D** がチャートに追加されます。これは、処理中のアクティブなリクエストの数を表します。

**Paris データセンター** に焦点を当てるために、**demo_datacenter: Paris (2)** のフィルターを追加します。次に、Configure Plot ⚙️ **(3)** ボタンをクリックして、データの表示方法を調整します。**rollup** タイプを **Auto (Delta)** から **Rate/sec (4)** に変更して、1秒あたりの受信リクエストの割合を表示します。

最後に、シグナル名を `demo.trans.count` から `Latency vs Load` **(5)** に変更して、チャート内での役割をより明確に反映させます。

![rollup change](../../images/rollout-change.png)

最後に {{% button %}}Save And Close{{% /button %}} ボタンを押します。これにより、3つの異なるチャートを持つダッシュボードに戻ります！

![three charts](../../images/3-charts.png)

「説明」ノートを追加してチャートを配置しましょう！
