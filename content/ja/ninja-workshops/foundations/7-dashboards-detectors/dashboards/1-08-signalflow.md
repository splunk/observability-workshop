---
title: Using SignalFlow
linkTitle: 1.08. Signalflow
weight: 1.08
---

## 1. SignalFlow の紹介

ここでは、Splunk Observability Cloud を支える強力な分析言語である **SignalFlow** について詳しく見ていきます。SignalFlow を使うと、監視ロジックをコードとして定義でき、メトリクスを柔軟かつリアルタイムに扱い、アラート発行を自動化できます。

**Splunk Infrastructure Monitoring** の中核には、ストリーミングメトリクスデータをリアルタイムに処理する **SignalFlow analytics engine** があります。SignalFlow は Python に似た構文で記述し、**metric time series (MTS)** を入力として受け取り、変換や計算を行い、新しい MTS を出力する計算処理を構築できます。

SignalFlow の代表的なユースケースには以下のようなものがあります。

* 現在値と過去のトレンドの比較 (例: 週次比較)
* 分散パーセンタイルチャートを使った母集団レベルの洞察の作成
* 変化率やしきい値の監視 (例: Service Level Objective (SLO) 違反の検知)
* 相関するディメンションの特定 (例: ディスク容量不足アラートの増加と関連するサービスの特定)

SignalFlow ベースの計算処理は、メトリクスを選択し分析関数をビジュアル的に適用することで、**Chart Builder** インターフェイス上で直接作成できます。より高度なユースケースでは、**SignalFlow API** を使って SignalFlow プログラムを直接記述・実行することもできます。

SignalFlow には時系列データに対して動作する豊富な組み込み関数が用意されており、複雑なシステム全体にわたる動的かつリアルタイムな監視に最適です。

{{% notice title="Info" style="info" %}}
SignalFlow の詳細については [Analyze incoming data using SignalFlow](https://docs.splunk.com/Observability/infrastructure/analytics/signalflow.html) を参照してください。
{{% /notice %}}

## 2. SignalFlow の表示

Chart Builder で **View SignalFlow** をクリックすると、チャートを動かしている内部コードを開けます。

![SignalFlow](../../images/view-signalflow.png)

**View SignalFlow** をクリックすると、チャートのロジックと変換処理を定義している **SignalFlow program (1)** が表示されます。このビューでは、可視化を支えているコードに直接アクセスできるため、ビジュアルエディタでは実現できない範囲の微調整や拡張が可能になります。

以下は、先ほど作成したチャートの SignalFlow コードの例です。このスニペットでは、2 つのパーセンタイルシグナル (現在と 1 週間前) を定義し、タイムシフトを適用し、それらの差分を計算する方法を示しています。コードを確認することで、各ステップが最終的なチャートにどう寄与しているかを理解しやすくなります。

{{< tabs >}}
{{% tab title="SignalFlow" %}}

```python
A = data('demo.trans.latency', filter=filter('demo_datacenter', 'Paris')).percentile(pct=95).publish(label='A', enable=False)
B = data('demo.trans.latency', filter=filter('demo_datacenter', 'Paris')).percentile(pct=95).timeshift('1w').publish(label='B', enable=False)
C = (A-B).publish(label='C')
```

{{% /tab %}}
{{< /tabs >}}

**View Builder (2)** をクリックすると、Chart **Builder** UI に戻れます。

![View Builder](../../images/show-signalflow.png)

それでは、この新しいチャートをダッシュボードに保存しましょう。
