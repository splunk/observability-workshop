---
title: SignalFlowの使用
linkTitle: 1.08. Signalflow
weight: 1.08
---

## 1. SignalFlowの紹介

ここでは、Splunk Observability Cloudを支える強力な分析言語である **SignalFlow** について詳しく見ていきます。SignalFlowを使用すると、モニタリングロジックをコードとして定義でき、メトリクスの操作やアラートの自動化を柔軟かつリアルタイムに行えます。

**Splunk Infrastructure Monitoring** の中核には **SignalFlow分析エンジン** があり、ストリーミングメトリクスデータをリアルタイムで処理します。SignalFlowはPythonに似た構文で記述され、 **メトリクス時系列（MTS）** を入力として受け取り、変換や計算を実行し、新しいMTSを出力するコンピュテーションを構築できます。

SignalFlowの一般的なユースケースには以下が含まれます。

* 現在の値と過去のトレンドの比較（週次比較など）
* 分散パーセンタイルチャートを使用したポピュレーションレベルのインサイトの作成
* 変化率やしきい値のモニタリング（サービスレベル目標（SLO）の違反検出など）
* 相関するディメンションの特定（ディスク空き容量不足アラートの増加に関連するサービスの特定など）

**Chart Builder** インターフェースでメトリクスを選択し、分析関数を視覚的に適用することで、SignalFlowベースのコンピュテーションを直接作成できます。より高度なユースケースでは、 **SignalFlow API** を使用してSignalFlowプログラムを直接記述・実行することも可能です。

SignalFlowには、時系列データに対して動作する豊富な組み込み関数が含まれており、複雑なシステム全体にわたる動的なリアルタイムモニタリングに最適です。

{{% notice title="情報" style="info" %}}
SignalFlowの詳細については、[Analyze incoming data using SignalFlow](https://docs.splunk.com/Observability/infrastructure/analytics/signalflow.html)を参照してください。
{{% /notice %}}

## 2. SignalFlowの表示

Chart Builderで **View SignalFlow** をクリックして、チャートを動かしている基盤コードを開きます。

![SignalFlow](../../images/view-signalflow.png)

**View SignalFlow** をクリックすると、チャートの背後にあるロジックと変換を定義する **SignalFlowプログラム（1）** が表示されます。このビューでは、ビジュアルエディターでは実現できない範囲まで、視覚化を支えるコードに直接アクセスして微調整や拡張が可能です。

以下は、先ほど作成したチャートのSignalFlowコードの例です。このスニペットは、2つのパーセンタイルシグナル（現在と1週間前）を定義し、timeshiftを適用し、それらの差分を計算する方法を示しています。コードを確認することで、各ステップが最終的なチャートにどのように寄与しているかを明確に理解できます。

{{< tabs >}}
{{% tab title="SignalFlow" %}}

```python
A = data('demo.trans.latency', filter=filter('demo_datacenter', 'Paris')).percentile(pct=95).publish(label='A', enable=False)
B = data('demo.trans.latency', filter=filter('demo_datacenter', 'Paris')).percentile(pct=95).timeshift('1w').publish(label='B', enable=False)
C = (A-B).publish(label='C')
```

{{% /tab %}}
{{< /tabs >}}

**View Builder（2）** をクリックして、Chart **Builder** UIに戻ります。

![View Builder](../../images/show-signalflow.png)

この新しいチャートをDashboardに保存しましょう。
