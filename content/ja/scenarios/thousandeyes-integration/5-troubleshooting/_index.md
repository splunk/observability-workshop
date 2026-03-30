---
title: トラブルシューティング
linkTitle: 7. トラブルシューティング
weight: 7
time: 15 minutes
description: ThousandEyes シナリオにおけるデプロイメント、接続性、メトリクスストリーミング、トレース相関の一般的な問題を診断します。
---

このセクションでは、KubernetesでThousandEyes Enterprise Agentをデプロイおよび使用する際に遭遇する可能性のある一般的な問題について説明します。

## DNS 解決エラーでテストが失敗する

テストがDNS解決エラーで失敗している場合は、ThousandEyes Pod内からDNSを確認してください：

```bash
# Verify DNS resolution from within the pod
kubectl exec -n te-demo -it <pod-name> -- nslookup api-gateway.production.svc.cluster.local

# Check CoreDNS logs
kubectl logs -n kube-system -l k8s-app=kube-dns
```

**一般的な原因：**

- 指定されたnamespaceにサービスが存在しない
- サービス名またはnamespaceの入力ミス
- CoreDNSが正常に機能していない

## 接続拒否エラー

接続拒否エラーが発生している場合は、以下を確認してください：

```bash
# Verify service endpoints exist
kubectl get endpoints -n production api-gateway

# Check if pods are ready
kubectl get pods -n production -l app=api-gateway

# Test connectivity from agent pod
kubectl exec -n te-demo -it <pod-name> -- curl -v http://api-gateway.production.svc.cluster.local:8080/health
```

**一般的な原因：**

- サービスをバックアップするPodがない（endpointsが空）
- PodがReady状態でない
- テストURLで間違ったポートが指定されている
- サービスセレクターがPodラベルと一致しない

## Network Policy がトラフィックをブロックしている

Network PolicyがThousandEyesエージェントからのトラフィックをブロックしている場合：

```bash
# List network policies
kubectl get networkpolicies -n production

# Describe network policy
kubectl describe networkpolicy <policy-name> -n production
```

**解決策：**
`te-demo` namespaceからサービスへのトラフィックを許可するNetwork Policyを作成します：

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-thousandeyes-agent
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api-gateway
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: te-demo
    ports:
    - protocol: TCP
      port: 8080
```

## エージェント Pod が起動しない

ThousandEyesエージェントPodが起動しない場合は、Podのステータスとイベントを確認してください：

```bash
# Get pod status
kubectl get pods -n te-demo

# Describe pod to see events
kubectl describe pod -n te-demo <pod-name>

# Check logs
kubectl logs -n te-demo <pod-name>
```

**一般的な原因：**

- リソース不足（memory/CPU）
- 無効または欠落しているTEAGENT_ACCOUNT_TOKENシークレット
- Pod Security Policyによってセキュリティコンテキストのケイパビリティが許可されていない
- イメージプルエラー

**解決策：**

- OOMKilledの場合はメモリ制限を増やす
- シークレットが正しく作成されているか確認する：`kubectl get secret te-creds -n te-demo -o yaml`
- Pod Security PolicyがNET_ADMINおよびSYS_ADMINケイパビリティを許可しているか確認する
- イメージプルを確認する：`kubectl describe pod -n te-demo <pod-name>`

## エージェントが ThousandEyes ダッシュボードに表示されない

エージェントは実行中だがThousandEyesダッシュボードに表示されない場合：

```bash
# Check agent logs for connection issues
kubectl logs -n te-demo -l app=thousandeyes --tail=100
```

**一般的な原因：**

- 無効または不正なTEAGENT_ACCOUNT_TOKEN
- ネットワークのEgressがブロックされている（ファイアウォールまたはNetwork Policy）
- エージェントがThousandEyes Cloudサーバーに到達できない

**解決策：**

1. トークンが正しく、適切にbase64エンコードされているか確認する
2. `*.thousandeyes.com` へのEgressが許可されているか確認する
3. エージェントがインターネットに到達できるか確認する：

```bash
kubectl exec -n te-demo -it <pod-name> -- curl -v https://api.thousandeyes.com
```

## データが Splunk Observability Cloud に表示されない

ThousandEyesのデータがSplunkに表示されない場合：

**統合の設定を確認：**

1. ThousandEyesでOpenTelemetry統合が正しく設定されているか確認する
2. SplunkインジェストエンドポイントURLがお使いのRealmに対して正しいか確認する
3. `X-SF-Token` ヘッダーに有効なSplunkアクセストークンが含まれているか確認する
4. テストが統合に割り当てられているか確認する

**テストの割り当てを確認：**

```bash
# Use ThousandEyes API to verify integration
curl -v https://api.thousandeyes.com/v7/stream \
  -H "Authorization: Bearer $BEARER_TOKEN"
```

**一般的な原因：**

- エンドポイントURLのSplunk Realmが間違っている
- 無効または期限切れのSplunkアクセストークン
- テストがOpenTelemetry統合に割り当てられていない
- 統合が適切に有効化または保存されていない

## 分散トレーシングが ThousandEyes に表示されない

メトリクスストリームは機能しているが、ThousandEyesの **Service Map** が空であるか、トレースが見つからない場合：

**監視対象のエンドポイントを確認：**

- HTTPヘッダーを受け入れること
- OpenTelemetryで計装されていること
- トレースコンテキストを下流に伝播すること
- Splunk APMにトレースを送信すること

**一般的な原因：**

- エンドポイントがHTTP ServerまたはAPIターゲットではなくページURLである
- サービスが計装されていないため、ThousandEyesはヘッダーを注入できるがトレースは出力されない
- エンドポイントがローカルのヘルスレスポンスのみを返し、下流サービスを実行しない

**推奨される修正：**

1. ThousandEyesテストを計装されたバックエンドAPIルートに切り替える
2. そのルートのトレースが既にSplunk APMに存在することを確認する
3. ThousandEyes分散トレーシングを有効にした後、テストを再実行する

## Splunk APM に ThousandEyes リンクが表示されない

トレースがSplunk APMで開くが、ThousandEyesのバックリンクやメタデータが表示されない場合：

**一般的な原因：**

`b3` プロパゲーターが `trace_state` を上書きし、ThousandEyesがリバースリンクのために保持することを期待している値をクリアする可能性があります。

**修正：**

計装されたサービスでプロパゲーターを明示的に設定します：

```bash
OTEL_PROPAGATORS=baggage,b3,tracecontext
```

環境変数を変更した後、計装されたワークロードを再起動し、新しいトラフィックを生成します。

## Splunk APM Connector の認証エラー

ThousandEyesの **Generic Connector** がSplunk APMにクエリできない場合：

**以下を確認してください：**

1. コネクターのターゲットが `https://api.<REALM>.signalfx.com` であること
2. コネクターで使用されているトークンが **API** スコープを持っていること
3. トークンを作成するユーザーがSplunk Observability Cloudで必要なロールを持っていること

{{% notice title="トークンに関する注意" style="info" %}}
OpenTelemetryメトリクスストリームはSplunk **Ingest** トークンを使用します。APM用のThousandEyes **Generic Connector** はSplunk **API** トークンを使用します。これらを混同することは、部分的な統合の最も一般的な原因の一つです。
{{% /notice %}}

## メモリ使用量が高い

ThousandEyesエージェントPodが過剰なメモリを消費している場合：

```bash
# Check current memory usage
kubectl top pod -n te-demo

# Check for OOMKilled events
kubectl describe pod -n te-demo <pod-name> | grep -i oom
```

**解決策：**

1. デプロイメントでメモリ制限を増やす：

```yaml
resources:
  limits:
    memory: 4096Mi  # Increase from 3584Mi
  requests:
    memory: 2500Mi  # Increase from 2000Mi
```

2. エージェントに割り当てられた同時テストの数を減らす
3. エージェントが不要なサービスを実行していないか確認する

## Permission Denied エラー

エージェントのログにPermission Deniedエラーが表示される場合：

**セキュリティコンテキストを確認：**

```bash
kubectl get pod -n te-demo <pod-name> -o jsonpath='{.spec.containers[0].securityContext}'
```

**解決策：**
Podに必要なケイパビリティがあることを確認します：

```yaml
securityContext:
  capabilities:
    add:
      - NET_ADMIN
      - SYS_ADMIN
```

{{% notice title="注意" style="info" %}}
厳格なPod Security Policyを持つ一部のKubernetesクラスターでは、これらのケイパビリティが許可されない場合があります。適切なポリシー例外を作成するために、クラスター管理者と協力する必要があるかもしれません。
{{% /notice %}}

## サポートを受ける

このガイドでカバーされていない問題に遭遇した場合：

1. **ThousandEyes Support**: [support.thousandeyes.com](https://support.thousandeyes.com) でThousandEyesサポートに連絡してください
2. **Splunk Support**: Splunk Observability Cloudの問題については、[Splunk Support](https://www.splunk.com/en_us/support-and-services.html) をご覧ください
3. **コミュニティフォーラム**:
   - [ThousandEyes Community](https://community.thousandeyes.com)
   - [Splunk Community](https://community.splunk.com)

{{% notice title="ヒント" style="primary" icon="lightbulb" %}}
サポートを求める際は、より効果的にトラブルシューティングできるよう、関連するログ、Podの説明、エラーメッセージを必ず含めてください。
{{% /notice %}}
