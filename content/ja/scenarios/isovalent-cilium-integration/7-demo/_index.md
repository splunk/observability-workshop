---
title: デモ — Isovalent と Splunk による DNS 問題の調査
linkTitle: デモスクリプト
weight: 7
---

## このデモで示すこと

このデモは、すべての運用チームやプラットフォームチームが経験したことのあるストーリーを伝えます。何かが壊れていて、ユーザーが不満を訴えていて、どこから手をつければよいかわからない状況です。調査は通常の最初のステップ — APM は問題なし、インフラも問題なし — を経て、ネットワークレイヤーへと切り替わります。そこで Isovalent の Hubble オブザーバビリティが Splunk に流れ込み、他のすべてのツールでは完全に見えなかった本当の問題、DNS の過負荷を明らかにします。

アプリケーションは **jobs-app** で、`tenant-jobs` namespace で動作するシミュレートされたマルチサービスの採用プラットフォームです。フロントエンド（`recruiter`、`jobposting`）、中央 API（`coreapi`）、バックグラウンドデータパイプライン（Kafka + `resumes` + `loader`）、そして定期的にインターネットへ HTTP リクエストを行う `crawler` サービスがあります。この crawler がこのストーリーの犯人になります。

{{% notice title="重要なポイント" style="primary" icon="lightbulb" %}}
APM とインフラメトリクスは正常に見えます。根本原因である DNS の過負荷は、アプリケーションレイヤーの下に存在するため、Splunk 内の Isovalent Hubble ダッシュボードを通じてのみ確認できます。
{{% /notice %}}

---

## 開始前の準備

これは誰も部屋にいない間に行ってください。デモが始まるときには、クリーンで正常なダッシュボードの前に座っている状態にしたいのであって、参加者が見ている前で kubectl を操作している状態は避けたいです。

### Jobs App のデプロイ

まだデプロイしていない場合は、[isovalent-demo-jobs-app](https://github.com/isovalent/demo-jobs-app) リポジトリから jobs-app Helm チャートをデプロイします

```bash
helm dependency build .
helm upgrade --install jobs-app . --namespace tenant-jobs --create-namespace
```

### すべてが動作していることの確認

デモ中に驚かないよう、以下のチェックを実行します

```bash
# Confirm your nodes are healthy
kubectl get nodes

# Confirm Cilium and Hubble are running on both nodes
kubectl get pods -n kube-system | grep -E "(cilium|hubble)"

# Confirm the Splunk OTel Collector is running — this is what ships metrics to Splunk
kubectl get pods -n otel-splunk

# Confirm the jobs-app is fully deployed and healthy
kubectl get pods -n tenant-jobs
```

{{% notice title="重要" style="warning" %}}
続行する前に、すべての Pod が `Running` 状態である必要があります。OTel Collector が起動していない場合、Splunk にメトリクスが表示されず、デモが成功しません。
{{% /notice %}}

### アプリを正常なベースラインにリセットする

crawler が穏やかで通常のペースで動作していることを確認します — 1 レプリカ、0.5〜5 秒ごとにクロールします

```bash
helm upgrade jobs-app . --namespace tenant-jobs --reuse-values \
  --set crawler.replicas=1 \
  --set crawler.crawlFrequencyLowerBound=0.5 \
  --set crawler.crawlFrequencyUpperBound=5 \
  --set resumes.replicas=1
```

その後、**少なくとも 5 分間待ちます**。Splunk がクリーンなベースラインを取り込むのに時間が必要で、これにより作成するスパイクが視覚的に明確になります。これを省略すると、チャートが明確なストーリーを伝えません。

### 問題の注入

デモ開始の約 5〜10 分前（またはデモ中にライブで効果を出すために）、以下を実行します

```bash
helm upgrade jobs-app . --namespace tenant-jobs --reuse-values \
  --set crawler.replicas=5 \
  --set crawler.crawlFrequencyLowerBound=0.2 \
  --set crawler.crawlFrequencyUpperBound=0.3 \
  --set resumes.replicas=2
```

これにより crawler が 1 Pod から 5 Pod にスケールアップし、クロール間隔が 0.2〜0.3 秒に短縮されます。各 crawler Pod は `api.github.com` に HTTP リクエストを行い、そのリクエストのたびに DNS ルックアップが必要です。5 つの Pod が毎秒複数回 DNS を叩くと、持続的に約 15〜25 DNS クエリ/秒が生成されます。これは DNS プロキシを飽和させ、レスポンスレイテンシーの蓄積を引き起こすのに十分です。namespace 内の DNS に依存する他のサービスが断続的な障害を経験し始めます。これがまさにチケットに書かれている内容です。

---

## Act 1 — チケットの到着

まず状況を描写します。まだ何もクリックする必要はありません — シーンを設定するだけです。

> *「普通の午後で、ITSM チケットが入ってきます。jobs アプリケーションチームによると、エンドユーザーが recruiter と job posting のページで断続的な 500 エラーを報告しており、過去 15 分ほどでロード時間が著しく悪化しているとのことです。P2 にエスカレートされました。調査しましょう。」*

| | |
| - | - |
| **チケット** | INC-4072 |
| **優先度** | P2 — High |
| **概要** | jobs-app で断続的な障害とレスポンスタイムの低下 |
| **説明** | Recruiter と job posting のページが断続的に 500 エラーを返しています。ユーザーは過去 15 分間でページロードが著しく遅くなったと報告しています。エンジニアリングチームは最近のデプロイを行っていません。 |
| **報告者** | Application Support Team |
| **影響を受ける namespace** | tenant-jobs |

> *「最近のデプロイはなし — これが実は興味深い点です。原因として明確な変更イベントがありません。つまり、何が変わったかを自分たちで突き止める必要があります。まずどこから始めますか？ APM です。」*

---

## Act 2 — APM の確認（行き止まり）

ここはほとんどの人が最初に見に行く場所であり、それがポイントです。APM を表示し、役に立たないことを確認し、より深い何かが必要であるという根拠を構築します。

**移動先** Splunk Observability Cloud → **APM** → **Service Map**

`tenant-jobs` 環境のサービスマップはトポロジーを示します`recruiter` と `jobposting` はどちらも `coreapi` を呼び出し、coreapi は Elasticsearch に接続します。`resumes` と `loader` サービスはバックグラウンドで Kafka 経由で通信しています。

> *「こちらがサービスマップです。すべてのサービスが稼働しています — すべてレスポンスを返し、すべて接続されています。実際に数字が何を示しているか見てみましょう。*
>
> *リクエストレートは正常に見えます。レイテンシーはわずかに上昇しているかもしれませんが、ユーザーに見えるエラーを説明するほどではありません。次に coreapi のエラーレートを見てください — 約 10% です。これが問題だと思うかもしれませんが、違います。このアプリにはセットアップの一部として設定可能なエラーレートが組み込まれています。10% はベースラインであり、リグレッションではありません。*
>
> *つまり APM が教えてくれているのは：サービスは生きている、トラフィックは流れている、エラーレートは変わっていない。アプリケーショントレースには根本原因を示すものがありません。インフラを見てみましょう。」*

{{% notice title="APM がこれを検知できない理由" style="info" %}}
APM はアプリケーションコードを計装します — サービスの内部で何が起きているかを観察します。接続が確立される*前に*ネットワークレイヤーで何が起きているかは見えません。DNS 解決、接続の切断、パケットレベルのイベントは設計上 APM からは見えません。
{{% /notice %}}

---

## Act 3 — インフラの確認（行き止まり）

インフラを表示し、問題がないことを確認し、まだ答えがないフラストレーションを聴衆に感じてもらいます。

**移動先** Splunk Observability Cloud → **Infrastructure** → **Kubernetes** → Cluster: `isovalent-demo`

> *「クラスター自体を見てみましょう。リソース制約があるかもしれません — ノードが高負荷になっている、Pod が OOMKill されている、そういったことです。*
>
> *両方のノードは正常に見えます。CPU とメモリは十分に通常の範囲内です。Pod を掘り下げてみると — すべて Running 状態で、再起動なし、退避もされていません。コンテナ自体もリソースリミットに達していません。*
>
> *ここで少し困った状況になります。チケットにはユーザーがエラーを見ていると書いてあります。APM はアプリが動いていると言っています。インフラはクラスターが正常だと言っています。さて、どうすればよいでしょうか？*
>
> *これは実はとても一般的な状況です。アプリケーションレイヤーの下、インフラレイヤーの下に存在する問題のクラスがあります — ネットワークレベルで起きていることで、従来の監視ツールでは見えないものです。DNS 障害、接続の切断、ポリシー拒否、トラフィックの非対称。これらはトレースや Pod メトリクスには表示されません。ネットワーク自体を観察できるものが必要です。そこで Isovalent の出番です。」*

---

## Act 4 — ネットワークが真実を語る

これがデモの核心です。ここはじっくり時間をかけてください。

**移動先** Splunk Observability Cloud → **Dashboards** → **Hubble by Isovalent**

> *「Cilium — すべてのノードで動作している CNI、ネットワーキングレイヤー — には Hubble というビルトインのオブザーバビリティコンポーネントがあります。Hubble は eBPF を使用して、クラスター内のすべてのネットワークフローをリアルタイムで監視します。サンプリングではなく、近似でもなく — すべての接続、すべての DNS リクエスト、すべてのパケットドロップを監視します。そして OpenTelemetry Collector がこれらの Hubble メトリクスをスクレイプして Splunk に転送するよう設定したので、先ほど APM やインフラを見ていたのと同じプラットフォーム上ですべてを確認できます。*
>
> *Hubble ダッシュボードを開きましょう。」*

### DNS クエリが制御不能

**DNS Queries チャートを指し、次に DNS Overview タブに移動します。**

> *「ありました。DNS クエリ量を見てください — 約 15 分前に急激にスパイクしています。このタイムスタンプはチケットが作成された時刻と完全に一致します。*
>
> *表示されているのは `hubble_dns_queries_total` で、ソース namespace ごとに分割されています。スパイクは完全に `tenant-jobs` — 私たちのアプリケーション namespace — から来ています。アプリケーション内の何かが大量の DNS トラフィックを生成し始め、DNS プロキシが処理に追いつけなくなりました。*
>
> *しかし右下を見てください — Missing DNS Responses チャートです。これはアラートが発火しているものです。値が大きくマイナスになっています。つまり DNS クエリが送信されているのにレスポンスが返ってきていないということです。DNS プロキシが圧倒されて、接続が静かにタイムアウトしています。これがユーザーに 500 エラーとして現れている波及効果です。」*

![Hubble DNS Overview showing Missing DNS Responses alert firing as values go deeply negative](images/Missing%20DNS%20Response.png)

### Top DNS Queries が犯人を明らかにする

**Top 10 DNS Queries チャートを指します。**

> *「では、これらすべての DNS リクエストを生成しているものを特定しましょう。Top 10 DNS Queries チャートは最も頻繁にクエリされるドメインを分類しており、1 つの名前が圧倒的に目立っています`api.github.com` です。*
>
> *これはクラスター内部のサービスではありません — 外部エンドポイントです。そしてアプリ内で外部エンドポイントと通信するのは crawler サービスだけです。crawler はジョブシミュレーションの一環として外部 URL に HTTP リクエストを行います。HTTP リクエストを行うたびに、まず DNS で `api.github.com` を解決する必要があります。*
>
> *通常これは問題ありません。1 つの crawler Pod が数秒ごとにリクエストを行うのは完全に管理可能です。しかし、どれほど積極的に動作しているかについて、明らかに何かが変わっています。」*

### Dropped Flows が影響範囲を示す

**Dropped Flows チャートを指します。**

> *「Dropped Flows チャートは別の注目すべきことを示しています。Hubble は成功した接続を追跡するだけでなく、拒否またはドロップされたすべての接続と、その理由コードをキャプチャします。DNS スパイクとまったく同じ時間にドロップの増加が見られます。*
>
> *これらのドロップは DNS 過負荷の下流の結果です。namespace 内のサービスが接続を試み、DNS が遅すぎるか失敗している場合、それらの接続試行はタイムアウトしてドロップされます。これが APM でレイテンシーの上昇として見えていたものです — しかし APM はその下に DNS の問題があることを知る由もありませんでした。」*

### ネットワークフロー量がパターンを確認する

**Metrics & Monitoring タブに移動します。**

> *「Metrics & Monitoring タブを見ると、全体像がさらに明確になります。ノードあたりの処理フロー数が垂直に上昇しています — これは生のネットワークトラフィック量です。Forwarded vs Dropped チャートは、それらのフローのかなりの割合が転送されずにドロップされていることを示しています。Drop Reason の内訳は TTL_EXCEEDED と DROP_REASON_UNKNOWN の混合を示しています — DNS タイムアウトがカスケードしている場合にまさに予想されるものです。特定の時点で何かが変わり、その時点以降のすべてがベースラインと異なって見えます。」*

![Hubble Metrics & Monitoring showing flow spike, forwarded vs dropped, and drop reasons](images/Increase%20of%20Flows.png)

### L7 HTTP トラフィックが興味深いストーリーを語る

**L7 HTTP Metrics タブに移動します。**

> *「L7 HTTP Metrics タブで指摘する価値のあるものがあります。これは実は APM が役に立たなかった理由を補強しています。受信リクエスト量はゼロではありません — トラフィックはまだ流れています。成功率チャートはほとんど緑に見えます。HTTP レベルの可視性だけを見ていた場合、アプリは問題ないと結論づけるかもしれません。*
>
> *しかし Incoming Requests by Source チャートを見てください。crawler が不釣り合いに多くのトラフィックを生成しています — 他のサービスから分離しているのが見えます。HTTP リクエストは正常に行えています。だから APM はフラグを立てません。問題は 1 つ下のレイヤー、DNS で、HTTP 接続が確立される前に起きています。」*

![Hubble L7 HTTP Metrics showing crawler traffic spike with high request volume](images/Increase%20in%20Requests.png)

---

## Act 5 — 根本原因の確認

ここで点と点をつなぎ、証明します。

> *「全体像はこうです：ある時点で、crawler サービスが 1 レプリカから 5 にスケールアップされ、クロール間隔が非常に積極的に設定されました — 0.2〜0.3 秒ごとです。5 つの Pod がそれぞれ毎秒複数回 `api.github.com` を解決するために DNS ルックアップを実行しています。合計すると、持続的に毎秒 15〜25 の DNS クエリです。DNS プロキシは単一のワークロードからそのような負荷を処理するように設計されていないため、キューイング、スローダウン、そして最終的にリクエストのドロップを始めます。namespace 内で DNS 解決が必要なすべてのサービスが巻き添えになります。*
>
> *確認してみましょう。」*

```bash
# Confirm the current crawler replica count — you'll see 5
kubectl get deploy crawler -n tenant-jobs

# Pull the environment config to see the crawl frequency settings
kubectl get deploy crawler -n tenant-jobs \
  -o jsonpath='{.spec.template.spec.containers[0].env}' | jq .
```

**オプションで、Cilium by Isovalent ダッシュボード → Policy: L7 Proxy タブに切り替えます。**

> *「Hubble 側ではなく Cilium 側からこれを見たい場合は、Cilium by Isovalent ダッシュボードに切り替えて Policy: L7 Proxy タブを見てください。FQDN — つまり DNS — の L7 Request Processing Rate が 21,000 リクエストを超えています。これは毎分ではありません。DNS プロキシが膨大な量の FQDN ルックアップを処理しており、すべてが受信され転送されているため、バックアップし始めたのです。このビューでは DNS Proxy Upstream Reply のレイテンシーも表示され、プロキシが圧力を受けていることを確認できます。」*

![Cilium Policy: L7 Proxy showing FQDN request processing rate spiking to 21k+](images/L7%20Procesing%20Rate%20Increase.png)

> *「これです。5 レプリカ、0.2〜0.3 秒ごとにクロール。*
>
> *APM はこれを見ることができません。コードを計装しているのであって、DNS ではないからです。インフラ監視もこれを見ることができません。Pod は正常だからです — 設定通りに正確に動作しています。これを検知できる唯一のツールは、eBPF レベルで動作し、すべてのパケット、すべての DNS リクエスト、すべての接続試行をリアルタイムで監視するものです。それが Hubble です。そして Splunk に接続したので、他のすべてに使用しているのと同じダッシュボードで検知できました。」*

---

## Act 6 — ライブで修正する

この部分はチャートがリアルタイムで回復するのを見られるので満足感があります。

> *「修正は簡単です — crawler をスケールダウンして通常のクロール間隔に戻します。」*

```bash
helm upgrade jobs-app . --namespace tenant-jobs --reuse-values \
  --set crawler.replicas=1 \
  --set crawler.crawlFrequencyLowerBound=0.5 \
  --set crawler.crawlFrequencyUpperBound=5 \
  --set resumes.replicas=1
```

**Hubble by Isovalent** ダッシュボードに戻り、1 分間そのままにします。

> *「DNS Queries チャートを見てください — ほぼ即座に下がっていくのが見えます。1〜2 分以内にベースラインに戻ります。Dropped flows はゼロになります。ネットワークフロー量は通常に戻ります。*
>
> *そして今 APM に戻れば、レイテンシーが正常化し、エラーレートが期待される 10% のベースラインに落ち着いているのが見えるでしょう。*
>
> *チケットをクローズできます。根本原因：crawler の設定ミスによる DNS 飽和。解決策：Helm 経由で crawler のレプリカ数とクロール間隔を元に戻しました。解決までの時間：チケットが作成されてから約 15 分。」*

{{% notice title="修復完了" style="success" %}}
DNS クエリレートがベースラインに戻り、dropped flows がクリアされ、アプリケーションの正常性が回復します — すべて Hubble ダッシュボードでライブで確認できます。
{{% /notice %}}

---

## Act 7 — これが本当に意味すること

最後にズームアウトして、価値の訴求を具体的に感じてもらいます。

> *「ここで何が起きたか考えてみましょう。本番環境スタイルの本格的な問題がありました — エンドユーザーにとって何かが壊れている — そして標準的なプレイブックを実行しました。APM は問題ないと言いました。インフラも問題ないと言いました。Hubble なしでは、次のステップはおそらくウォールームの呼び出し、ログを見つめる人々、namespace を完全に再起動して問題が解消されることを祈ることだったでしょう。*
>
> *代わりに、Hubble ダッシュボードを開いた瞬間から 3 分以内に発見できました。私たちが賢いからではなく、適切なレイヤーへの可視性があったからです。*
>
> *これが機能する理由は eBPF です。Cilium の Hubble コンポーネントは Linux カーネルにフックし、ネットワークイベントをソースで観察します — アプリケーションコードに到達する前に、Pod ログに表示される前に、APM のトレースになる前に。そしてこれらのメトリクスを OpenTelemetry Collector を通じて Splunk に送信することで、APM データやインフラデータと同じプラットフォーム上に並びます。ツールを切り替えたり、5 つの異なるダッシュボード間でコンテキストスイッチする必要はありません。以前はなかった可視性のレイヤーを追加し、チームがすでに知っているワークフロー内に保持します。*
>
> *これがこのストーリーです。ネットワークオブザーバビリティはニッチな需要ではありません — APM とインフラ監視が残すギャップです。Isovalent がそのギャップを埋め、Splunk がそれを可視化する場所です。」*

---

## クイックリファレンス

**問題の注入**（デモの約 10 分前に実行）

```bash
helm upgrade jobs-app . -n tenant-jobs --reuse-values \
  --set crawler.replicas=5 \
  --set crawler.crawlFrequencyLowerBound=0.2 \
  --set crawler.crawlFrequencyUpperBound=0.3 \
  --set resumes.replicas=2
```

**修復**（Act 6 でライブ実行）

```bash
helm upgrade jobs-app . -n tenant-jobs --reuse-values \
  --set crawler.replicas=1 \
  --set crawler.crawlFrequencyLowerBound=0.5 \
  --set crawler.crawlFrequencyUpperBound=5 \
  --set resumes.replicas=1
```

**設定ミスの確認**

```bash
kubectl get deploy crawler -n tenant-jobs
kubectl get deploy crawler -n tenant-jobs \
  -o jsonpath='{.spec.template.spec.containers[0].env}' | jq .
```

**Splunk ナビゲーションパス**
APM → Service Map → *（問題なしを表示）* → Infrastructure → Kubernetes → *（問題なしを表示）* → Dashboards → Hubble by Isovalent → *（DNS スパイクを表示）*

## タイミングガイド

| セクション | おおよその時間 |
| ------- | ------------ |
| Act 1 — チケット | 約 1 分 |
| Act 2 — APM（行き止まり） | 約 2〜3 分 |
| Act 3 — インフラ（行き止まり） | 約 1〜2 分 |
| Act 4 — Hubble ダッシュボード | 約 4〜5 分 |
| Act 5 — 根本原因の確認 | 約 2 分 |
| Act 6 — ライブ修正 | 約 2 分 |
| Act 7 — 価値のまとめ | 約 2 分 |
| **合計** | **約 14〜17 分** |
