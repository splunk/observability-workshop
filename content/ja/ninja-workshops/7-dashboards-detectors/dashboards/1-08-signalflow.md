---
title: SignalFlow の使用
linkTitle: 1.08. Signalflow
weight: 1.08
---

## 1. SignalFlow の紹介

それでは、Splunk Observability Cloudを支える強力な分析言語である **SignalFlow** を詳しく見てみましょう。SignalFlowを使用すると、監視ロジックをコードとして定義でき、メトリクスを扱いアラートを自動化するための柔軟でリアルタイムな方法を提供します。

**Splunk Infrastructure Monitoring** の中核には、ストリーミングメトリクスデータをリアルタイムで処理する **SignalFlow 分析エンジン** があります。SignalFlowはPythonに似た構文で記述され、**メトリクス時系列（MTS）** を取り込み、変換や計算を実行し、新しいMTSを出力する計算を構築できます。

SignalFlowの一般的なユースケースには以下が含まれます：

* 週次比較など、現在の値と過去のトレンドの比較
* 分散パーセンタイルチャートを使用した母集団レベルの洞察の作成
* Service Level Objective（SLO）違反の検出など、変化率やしきい値の監視
* ディスク容量不足アラートの増加に関連するサービスの特定など、相関ディメンションの識別

**Chart Builder** インターフェースでメトリクスを選択し、分析関数を視覚的に適用することで、SignalFlowベースの計算を直接作成できます。より高度なユースケースでは、**SignalFlow API** を使用してSignalFlowプログラムを直接記述および実行することもできます。

SignalFlowには、時系列データを操作する堅牢な組み込み関数セットが含まれており、複雑なシステム全体でのダイナミックでリアルタイムな監視に最適です。

{{% notice title="Info" style="info" %}}
SignalFlowの詳細については、[Analyze incoming data using SignalFlow](https://docs.splunk.com/Observability/infrastructure/analytics/signalflow.html) を参照してください。
{{% /notice %}}

## 2. SignalFlow の表示

Chart Builderで **View SignalFlow** をクリックして、チャートを駆動する基盤となるコードを開きます。

![SignalFlow](../../images/view-signalflow.png)

**View SignalFlow** をクリックすると、チャートの背後にあるロジックと変換を定義する **SignalFlow プログラム (1)** が表示されます。このビューにより、可視化を駆動するコードに直接アクセスでき、ビジュアルエディタでは不可能な微調整や拡張が可能になります。

以下は、先ほど作成したチャートのSignalFlowコードの例です。このスニペットは、2つのパーセンタイルシグナル（現在と1週間前）を定義し、タイムシフトを適用し、それらの差を計算した方法を示しています。コードを確認することで、各ステップが最終的なチャートにどのように貢献しているかが明確になります。

{{< tabs >}}
{{% tab title="SignalFlow" %}}

```python
A = data('demo.trans.latency', filter=filter('demo_datacenter', 'Paris')).percentile(pct=95).publish(label='A', enable=False)
B = data('demo.trans.latency', filter=filter('demo_datacenter', 'Paris')).percentile(pct=95).timeshift('1w').publish(label='B', enable=False)
C = (A-B).publish(label='C')
```

{{% /tab %}}
{{< /tabs >}}

**View Builder (2)** をクリックして、Chart **Builder** UIに戻ります。

![View Builder](../../images/show-signalflow.png)

この新しいチャートをダッシュボードに保存しましょう！
