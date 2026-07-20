---
title: 前提条件
linkTitle: 01. 前提条件
weight: 1
time: 5 minutes

---

このワークショップを始める前に、以下のツールがインストールされていること、およびSplunk Observability Cloudアカウントが準備できていることを確認してください。

## 必要な知識

このワークショップでは、以下に関する基本的な知識があることを前提としています

- 基本的なKubernetesの概念（Pod、Deployment、Service）
- HTTPリクエスト/レスポンスのフロー
- 分散トレーシングの概念（Span、Traceなど）

OpenTelemetryの経験が必要です。コンテキスト伝播の課題については、ワークショップの中で説明します。

## 必要なソフトウェア

以下のツールがインスタンスにインストールされます

| ツール | 最小バージョン | 確認方法 |
|------|-----------------|--------|
| [Docker](https://docs.docker.com/get-docker/) | 24.x | `docker --version` |
| [kubectl](https://kubernetes.io/docs/tasks/tools/) | 1.28+ | `kubectl version --client` |
| [k3d](https://k3d.io/) | 5.6+ | `k3d version` |
| [Git](https://git-scm.com/) | 2.x | `git --version` |
| [Helm](https://helm.sh/docs/intro/install/) | 3.12+ | `helm version` |
| [Node.js](https://nodejs.org/)（オプション） | 20.x | `node --version` |

## Splunk Observability Cloudへのアクセス

以下の権限を持つSplunk Observability Cloud組織へのアクセスが必要です

1. **組織アクセストークンの作成** - OTel CollectorとAPMエージェントで使用します
2. **RUMアクセストークンの作成** - ブラウザエージェントで使用します（公開トークン）
3. **APMトレースの表示** - APM → Service Map & APM → Traces
4. **RUMセッションの表示** - Digital Experience → Session Search

### ステップ2の前にこれらの値を確認してください

| 変数 | 確認場所 |
|----------|------------------|
| `SPLUNK_REALM` | 組織のURL（例: `https://app.us0.signalfx.com` の `us0`） |
| `SPLUNK_ACCESS_TOKEN` | Settings → Access Tokens → Create Token（Ingestスコープ） |
| `SPLUNK_RUM_ACCESS_TOKEN` | Data Management → RUM → Create RUM access token |

## 検証チェックリスト

続行する前に、割り当てられたインスタンスで以下のコマンドを実行してください。各セクションには期待される出力が含まれているので、準備ができていることを確認できます。

#### 1. 必要なツールの確認

**期待される出力（バージョンは異なる場合があります）**

{{< tabs >}}
{{% tab title="スクリプト" %}}

```bash
docker --version
kubectl version --client
k3d version
helm version --short
git --version
```

{{% /tab %}}
{{% tab title="出力例" %}}

``` text
Docker version 27.4.0, build bde2b89
Client Version: v1.31.0
k3d version v5.7.4
v3.16.2+gf786678
git version 2.47.0
```

{{% /tab %}}
{{< /tabs >}}

#### 2. 必要なポートが空いていることを確認

{{< tabs >}}
{{% tab title="スクリプト" %}}

```bash
lsof -i :30080 -i :5111 -i :15672 2>/dev/null || echo "Ports 30080, 5111, and 15672 are available"
```

{{% /tab %}}
{{% tab title="出力例" %}}

``` text
Ports 30080, 5111, and 15672 are available
```

**ポートが使用中の場合:** 出力に表示されるプロセス名を確認して停止するか、 `scripts/setup-k3d.sh` を編集して別のポートを使用してください。

{{% /tab %}}
{{< /tabs >}}
