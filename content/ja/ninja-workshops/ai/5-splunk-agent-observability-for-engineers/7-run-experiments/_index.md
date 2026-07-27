---
title: リリース前にExperimentを実行する
linkTitle: 7. Experimentの実行
weight: 7
time: 20 minutes
---

ここまで、本番環境でエージェントを観察してきました。**Experiments** はそのアプローチを逆転させます。固定のデータセットに対してリリース*前*にエージェントを評価し、ユーザーが気づく前にリグレッションを検出できます。

{{% notice title="ペルソナ" style="orange" icon="user" %}}

Careful Health Providerの **AIエンジニア** として、プロンプトを変更し、異なるモデルを試そうとしています。いくつかのサンプル回答からの直感ではなく、品質が向上したという客観的な証拠が必要です。Experimentは、信頼できる再現可能でスコア付きのベンチマークを提供します。

{{% /notice %}}

> [!splunk] 体系的な評価がなければ、すべてのデプロイは運任せとなり、ユーザーが苦情を報告するまでリグレッションは見えないままです。**Experimentは直感をエビデンスに置き換えます**。一貫性があり、再現可能で、比較可能です。リリースゲートとして使用したり、バリアント（プロンプト、モデル、設定）を比較して最適な組み合わせを選択したりできます。

{{% notice title="作業場所" style="info" %}}

この章では `~/workshop/healthcare-assistant/3-app-with-experiments` で作業します。計装済みアプリをベースに、`experiments/` パッケージと `dataset.csv` を追加しています。Experimentランナーはチャットアプリと **同じ `HealthcareAgent`** を使用するため、これまで確認してきたSpanはExperiment実行時にも表示されます。フォルダは完成した状態で提供されるため、この章のリファレンスとしても機能します。

{{% /notice %}}

サブセクションに進み、データセットの作成、Experimentの実行、結果の確認を行います。
