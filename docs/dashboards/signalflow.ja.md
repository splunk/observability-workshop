# SignalFlow

## 1. はじめに

ここでは、Observability Cloud の分析言語であり、Monitoring as Codeを実現するために利用する SignalFlow について見てみましょう。

Splunk Infrastructure Monitoring の中心となるのは、Python ライクな、計算を実行する SignalFlow 分析エンジンです。SignalFlow のプログラムは、ストリーミング入力を受け取り、リアルタイムで出力します。SignalFlow には、時系列メトリック（MTS）を入力として受け取り、計算を実行し、結果の MTS を出力する分析関数が組み込まれています。

- 過去の基準との比較する（例：前週との比較）
- 分布したパーセンタイルチャートを使った母集団の概要を表示する
- 変化率（またはサービスレベル目標など、比率で表されるその他の指標）が重要な閾値を超えたかどうか検出する
- 相関関係にあるディメンジョンの発見する（例：どのサービスの挙動がディスク容量不足の警告と最も相関関係にあるかの判断する）

Infrastructure Monitoring は、Chart Builder ユーザーインターフェイスでこれらの計算を行い、使用する入力 MTS とそれらに適用する分析関数を指定できます。また、[SignalFlow API](https://dev.splunk.com/observability/docs/) を使って、SignalFlow のプログラムを直接実行することもできます。

SignalFlow には、時系列メトリックを入力とし、そのデータポイントに対して計算を行い、計算結果である時系列メトリックを出力する、分析関数の大規模なライブラリが組み込まれています。

!!! info
    SignalFlow の詳細については、[Analyze incoming data using SignalFlow](https://docs.splunk.com/Observability/references/signalflow.html){: target=_blank} を参照してください。

## 2. SignalFlow の表示

チャートビルダーで **View SignalFlow** をクリックします。

![SignalFlow](../images/dashboards/view-signalflow.png)

作業していたチャートを構成する SignalFlow のコードが表示されます。UI内で直接 SignalFlow を編集できます。ドキュメントには、SignalFlow の関数やメソッドの[全てのリスト](https://dev.splunk.com/observability/docs/signalflow/function_method_list)が掲載されています。

また、SignalFlow をコピーして、API や Terraform とやり取りする際に使用して、[Monitoring as Code](../../monitoring-as-code/) を実現することもできます。

![Code](../images/dashboards/show-signalflow.png)

=== "SignalFlow"

    ```Python
    A = data('demo.trans.latency', filter=filter('demo_datacenter', 'Paris')).percentile(pct=95).publish(label='A', enable=False)
    B = data('demo.trans.latency', filter=filter('demo_datacenter', 'Paris')).percentile(pct=95).timeshift('1w').publish(label='B', enable=False)
    C = (A-B).publish(label='C')
    ```

**View Builder** をクリックすると、Chart **Builder** の UI に戻ります。

![View Builder](../images/dashboards/view-builder.png)

この新しいチャートをダッシュボードに保存してみましょう!
