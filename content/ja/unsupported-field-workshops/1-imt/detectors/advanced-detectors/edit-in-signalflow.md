---
title: Edit in SignalFlow
linkTitle: 4.2.2 SignalFlow Refactor with Multiple Conditions
weight: 3
---

## 目的

ウィザードで生成されたディテクターを以下のようにリファクタリングします

- 閾値の計算とアラートロジックを分離する
- 単一の `detect()` ステートメントで複数の条件を組み合わせる
- 静的な運用ガードレールを導入する
- 動的な異常閾値をアラートメッセージで再利用できるようにする

---

## Edit in SignalFlow

右上のディテクターアクションメニュー **(⋯)** から、**Edit in SignalFlow** を選択します。

先ほど保存したディテクターの Detector UI にまだいるはずですが、そうでない場合は

以下に移動します

**Alerts & Detectors → Detectors**

ディテクターを探して開き、**Edit in SignalFlow** を選択します。

---

## 生成された SignalFlow

**SignalFlow** タブを選択し、履歴異常ディテクター用に生成された SignalFlow を確認します。

{{% notice title="フォーマットに関する注意" style="info" %}}
```against_periods.detector_mean_std``` 関数のフォーマットは1行になっていることに注意してください。各パラメーターの後に改行を追加するか、以下の整形済み SignalFlow をコピー＆ペーストすると読みやすくなります。
{{% /notice %}}

```python
from signalfx.detectors.against_periods import against_periods

A = data(
  'system.cpu.utilization',
  filter=filter('deployment.environment', 'astronomy-shop')
).publish(label='A')

against_periods.detector_mean_std(
  stream=A,
  window_to_compare='10m',
  space_between_windows='1d',
  num_windows=4,
  fire_num_stddev=2.5,
  clear_num_stddev=2,
  discard_historical_outliers=True,
  orientation='above',
  auto_resolve_after='1h'
).publish('XYZ_AdvancedDetector')
```

---

## リファクタリングする理由

ウィザードは以下を使用してディテクターを生成しました

```
against_periods.detector_mean_std()
```

このヘルパー関数は

- 履歴ベースラインの閾値を計算する  
- fire および clear ロジックを適用する  
- orientation（`above` / `below`）を適用する  
- auto-resolve のタイミングを処理する  
- 単一の呼び出しでディテクターを publish する  

便利ではありますが、この構造では閾値の生成とアラート動作が一体化しています。  
複数条件のロジックを構築するには、閾値の計算と検出ロジックを分離する必要があります。

{{% notice title="SignalFlow Detector Library" style="info" %}}
このラボで使用されるヘルパー関数と閾値ストリームの実装を確認できます。

[View SignalFlow Detector Library Documentation](https://github.com/signalfx/signalflow-library/blob/master/library/signalfx/detectors/against_periods/README.md)
{{% /notice %}}

---

## ステップ 1 – Import の置き換え

以下を削除します

```python
from signalfx.detectors.against_periods import against_periods
```

以下に置き換えます

```python
#import from SignalFx Library
from signalfx.detectors.against_periods import streams
from signalfx.detectors.against_periods import conditions
```

- `streams` は再利用可能な閾値ストリームを生成します。
- `conditions` は `detect()` 内での論理的な組み合わせを可能にします。

---

## ステップ 2 – シグナルストリームの名前変更

わかりやすくするために、シグナル名を `A` から `CPU` に変更します。

以下を置き換えます

```python
A = data('system.cpu.utilization', filter=filter('deployment.environment', 'astronomy-shop')).publish(label='A')
```

以下に変更します

```python
#Calculate/filter CPU
CPU = data('system.cpu.utilization', filter=filter('deployment.environment', 'astronomy-shop')).publish(label='CPU')
```

---

## ステップ 3 – ヘルパー呼び出しを閾値ストリームに変換する

ウィザードで生成されたヘルパーには、保持したい異常チューニング値がすでに含まれています

- `window_to_compare='10m'`
- `space_between_windows='1d'`
- `num_windows=4`
- `fire_num_stddev=2.5`
- `clear_num_stddev=2`
- `discard_historical_outliers=True`

これらの値はそのまま維持します。

以下を見つけます

```python
against_periods.detector_mean_std(
```

関数名のみを以下に置き換えます

```python
#Use the streams.mean_std_thresholds function to establish the built in min/max fire and clear threshold conditions
fire_bot, clear_bot, clear_top, fire_top = streams.mean_std_thresholds(
```

ストリーム引数を更新します

以下を置き換えます

```python
stream=A,
```

以下に変更します

```python
CPU,
```

---

## ヘルパー専用のアラートパラメーターを削除する

`streams.mean_std_thresholds()` は閾値ストリームのみを生成します。  
orientation や auto-resolve などのディテクター動作は実装しません。

以下を削除します

```python
orientation='above',
auto_resolve_after='1h'
```

---

## ヘルパーの Publish を削除する

ヘルパー呼び出しはディテクターを直接 publish します

```python
).publish('XYZ_AdvancedDetector')
```

`streams.mean_std_thresholds()` はディテクターを publish しません。  

```.publish('XYZ_AdvancedDetector')``` を**削除**します。

---

## ステップ 4 – 複数条件の Detect ロジックを追加する

閾値の生成とアラートロジックが分離されたので、検出条件を明示的に定義する必要があります。

まず、静的ガードレールを独自のストリームとして定義します。以下を追加します

```python
#Define static threshold for CPU as a variable
static_threshold = threshold(90)
```

これにより、90% の定数閾値ストリームが作成されます。  
ストリームとして定義することで（`detect()` 内に直接 `threshold(90)` を埋め込む代わりに）、publish、可視化、アラートメッセージでの参照が可能になります。

次に、複数条件の検出ロジックを定義します

```python
#detect when CPU has exceeded the fire_top thresholds established AND CPU exceeds static threshold (90%) for 15 minutes; publish detector
detect(
  CPU > fire_top and when(CPU > static_threshold, lasting='15m')
).publish('custom_CPU_detector')
```

この detect ステートメントは2つの独立した条件を評価します

1. **履歴ベースラインの異常**  
   `CPU > fire_top`  
   10分間の移動平均が、動的に計算された異常閾値を超えています。

2. **持続時間付きの静的運用ガードレール**  
   `when(CPU > static_threshold, lasting='15m')`  
   CPU が15分間連続で90%を超えている必要があります。

ディテクターが発火するには、両方の条件が true と評価される必要があります。

これにより、異常動作と運用閾値がどのように相互作用するかを正確に制御できます。
この構成では以下が導入されます

- **履歴ベースラインの異常:** `CPU > fire_top`
- **静的運用ガードレール:** `CPU > static_threshold`
- **持続的な違反要件:** 15分間
- 明示的なディテクターの publication

---

## ステップ 5 – プレビューとメッセージング用に閾値ストリームを Publish する

ディテクターのプレビューとアラートメッセージングの両方で閾値を表示するには

```python
#publish the fire_top threshold and static_threshold for data visualization
fire_top.publish('CPU_top_threshold')
static_threshold.publish('CPU_static_threshold')
```

---

## 結果

{{< tabs >}}
{{% tab title="結果" %}}

ウィザードの便利なヘルパーを以下のように変換しました

- 明示的な閾値生成  
- 組み合わせ可能な複数条件のアラートロジック  
- 静的ガードレールの適用  
- 持続的な評価ロジック  
- 再利用可能な異常閾値および静的閾値ストリーム  

この構造により、ディテクターの動作においてより高い精度、柔軟性、明確性が得られます。
{{% /tab %}}
{{% tab title="Final SignalFlow" %}}

```python
#import from SignalFx Library
from signalfx.detectors.against_periods import streams
from signalfx.detectors.against_periods import conditions

#Calculate/filter CPU
CPU = data('system.cpu.utilization', filter=filter('deployment.environment', 'astronomy-shop')).publish(label='CPU')

#Use the streams.mean_std_thresholds function to establish the built in min/max fire and clear threshold conditions
fire_bot, clear_bot, clear_top, fire_top = streams.mean_std_thresholds(
  CPU,
  window_to_compare='10m',
  space_between_windows='1d',
  num_windows=4,
  fire_num_stddev=2.5,
  clear_num_stddev=2,
  discard_historical_outliers=True,
)

#Define static threshold for CPU as a variable
static_threshold = threshold(90)

#detect when CPU has exceeded the fire_top thresholds established AND CPU exceeds static threshold (90%) for 15 minutes; publish detector
detect(
  CPU > fire_top and when(CPU > static_threshold, lasting='15m')
).publish('custom_CPU_detector')

#publish the fire_top threshold and static_threshold for data visualization
fire_top.publish('CPU_top_threshold')
static_threshold.publish('CPU_static_threshold')
```

{{% /tab %}}
{{< /tabs >}}

{{% notice title="アラートメッセージでの Static Threshold" style="info" %}}
静的ガードレールが定義され publish されているため

```python
static_threshold.publish('CPU_static_threshold')
```

カスタムアラートメッセージで以下のように利用できます

```
{{inputs.CPU_static_threshold.value}}
```

SignalFlow で publish されたストリームは、アラートメッセージ内で `inputs.<stream_name>.value` としてアクセスできます。
{{% /notice %}}
