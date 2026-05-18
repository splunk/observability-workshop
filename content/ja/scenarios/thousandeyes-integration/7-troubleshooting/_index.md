---
title: トラブルシューティング
linkTitle: 7. トラブルシューティング
weight: 7
time: 15 minutes
description: ThousandEyes シナリオにおけるデプロイ、接続性、メトリクスストリーミング、トレース相関の一般的な問題を診断します。
---

このセクションでは、Kubernetes で ThousandEyes Enterprise Agent をデプロイおよび使用する際に遭遇する可能性のある一般的な問題について説明します。

## DNS 解決エラーによるテスト失敗

テストが DNS 解決エラーで失敗している場合は、ThousandEyes Pod 内から DNS を確認してください

```bash
# Verify DNS resolution from within the pod
kubectl exec -n te-demo -it <pod-name> -- nslookup api-gateway.default.svc.cluster.local

# Check CoreDNS logs
kubectl logs -n kube-system -l k8s-app=kube-dns
```

**一般的な原因**

- 指定された Namespace にサービスが存在しない
- サービス名または Namespace のタイプミス
- CoreDNS が正常に機能していない

## 接続拒否エラー

接続拒否エラーが表示される場合は、以下を確認してください

```bash
# Verify service endpoints exist
kubectl get endpoints -n default api-gateway

# Check if pods are ready
kubectl get pods -n default -l app=api-gateway

# Test connectivity from agent pod
kubectl exec -n te-demo -it <pod-name> -- curl -v http://api-gateway.default.svc.cluster.local:82/api/customer/owners
```

**一般的な原因**

- サービスをバックするPodがない（エンドポイントが空）
- Pod が Ready 状態でない
- テスト URL で間違ったポートが指定されている
- サービスセレクターが Pod ラベルと一致しない

## ネットワークポリシーによるトラフィックのブロック

ネットワークポリシーが ThousandEyes エージェントからのトラフィックをブロックしている場合

```bash
# List network policies
kubectl get networkpolicies -n default

# Describe network policy
kubectl describe networkpolicy <policy-name> -n default
```

**解決策**
`te-demo` Namespace からサービスへのトラフィックを許可するネットワークポリシーを作成します

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-thousandeyes-agent
  namespace: default
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

ThousandEyes エージェント Pod が起動しない場合は、Pod のステータスとイベントを確認してください

```bash
# Get pod status
kubectl get pods -n te-demo

# Describe pod to see events
kubectl describe pod -n te-demo <pod-name>

# Check logs
kubectl logs -n te-demo <pod-name>
```

**一般的な原因**

- リソース不足（メモリ/CPU）
- 無効または欠落している TEAGENT_ACCOUNT_TOKEN シークレット
- Pod Security Policy で許可されていないセキュリティコンテキストのケーパビリティ
- イメージプルエラー

**解決策**

- OOMKilled の場合はメモリ制限を増加する
- シークレットが正しく作成されていることを確認する`kubectl get secret te-creds -n te-demo -o yaml`
- Pod Security Policy が NET_ADMIN および SYS_ADMIN ケーパビリティを許可していることを確認する
- イメージプルを確認する`kubectl describe pod -n te-demo <pod-name>`

## エージェントが ThousandEyes ダッシュボードに表示されない

エージェントは実行されているが ThousandEyes ダッシュボードに表示されない場合

```bash
# Check agent logs for connection issues
kubectl logs -n te-demo -l app=thousandeyes --tail=100
```

**一般的な原因**

- 無効または不正な TEAGENT_ACCOUNT_TOKEN
- ネットワークのエグレスがブロックされている（ファイアウォールまたはネットワークポリシー）
- エージェントが ThousandEyes Cloud サーバーに到達できない

**解決策**

1. トークンが正しく、適切に base64 エンコードされていることを確認する
2. `*.thousandeyes.com` へのエグレスが許可されていることを確認する
3. エージェントがインターネットに到達できることを確認する

```bash
kubectl exec -n te-demo -it <pod-name> -- curl -v https://api.thousandeyes.com
```

## Splunk Observability Cloud にデータが表示されない

ThousandEyes のデータが Splunk に表示されない場合

**インテグレーション設定の確認**

1. ThousandEyes で OpenTelemetry インテグレーションが正しく設定されていることを確認する
2. Splunk インジェストエンドポイント URL がお使いのレルムに対して正しいことを確認する
3. `X-SF-Token` ヘッダーに有効な Splunk アクセストークンが含まれていることを確認する
4. テストがインテグレーションに割り当てられていることを確認する

**テスト割り当ての確認**

```bash
# Use ThousandEyes API to verify integration
curl -v https://api.thousandeyes.com/v7/stream \
  -H "Authorization: Bearer $BEARER_TOKEN"
```

**一般的な原因**

- エンドポイント URL の Splunk レルムが間違っている
- 無効または期限切れの Splunk アクセストークン
- テストが OpenTelemetry インテグレーションに割り当てられていない
- インテグレーションが有効化または正しく保存されていない

## ThousandEyes で分散トレーシングが表示されない

メトリクスストリームは動作しているが、ThousandEyes の **Service Map** が空であるか、トレースが見つからない場合

**監視対象エンドポイントの確認**

- HTTP ヘッダーを受け付けること
- OpenTelemetry で計装されていること
- トレースコンテキストを下流に伝搬していること
- Splunk APM にトレースを送信していること

**一般的な原因**

- エンドポイントが HTTP Server や API ターゲットではなく、ページ URL である
- サービスが計装されていないため、ThousandEyes がヘッダーを注入できてもトレースが生成されない
- エンドポイントがローカルのヘルスレスポンスのみを返し、下流のサービスを呼び出さない

**推奨される修正**

1. ThousandEyes テストを計装済みのバックエンド API ルートに切り替える
2. そのルートのトレースが Splunk APM に既に存在することを確認する
3. ThousandEyes 分散トレーシングを有効にした後、テストを再実行する

## Splunk APM で ThousandEyes リンクが表示されない

Splunk APM でトレースは開けるが、ThousandEyes のバックリンクやメタデータが表示されない場合

**一般的な原因**

`b3` プロパゲーターが `trace_state` を上書きし、ThousandEyes がリバースリンクのために保持する必要がある値をクリアすることがあります。

**修正**

計装されたサービスでプロパゲーターを明示的に設定します

```bash
OTEL_PROPAGATORS=baggage,b3,tracecontext
```

環境変数を変更した後、計装されたワークロードを再起動し、新しいトラフィックを生成してください。

## Splunk APM Connector 認証エラー

ThousandEyes の **Generic Connector** が Splunk APM にクエリできない場合

**以下を確認してください**

1. コネクターのターゲットが `https://api.<REALM>.signalfx.com` であること
2. コネクターで使用されているトークンが **API** スコープを持っていること
3. トークンを作成したユーザーが Splunk Observability Cloud で必要なロールを持っていること

{{% notice title="トークンに関する注意" style="info" %}}
OpenTelemetry メトリクスストリームは Splunk **Ingest** トークンを使用します。ThousandEyes の **Generic Connector** for APM は Splunk **API** トークンを使用します。これらを混同することは、インテグレーションが部分的にしか機能しない最も一般的な原因の一つです。
{{% /notice %}}

## メモリ使用量が高い

ThousandEyes エージェント Pod が過剰なメモリを消費している場合

```bash
# Check current memory usage
kubectl top pod -n te-demo

# Check for OOMKilled events
kubectl describe pod -n te-demo <pod-name> | grep -i oom
```

**解決策**

1. デプロイメントのメモリ制限を増加する

```yaml
resources:
  limits:
    memory: 4096Mi  # Increase from 3584Mi
  requests:
    memory: 2500Mi  # Increase from 2000Mi
```

2. エージェントに割り当てられた同時テスト数を減らす
3. エージェントが不要なサービスを実行していないか確認する

## Permission Denied エラー

エージェントログに Permission Denied エラーが表示される場合

**セキュリティコンテキストの確認**

```bash
kubectl get pod -n te-demo <pod-name> -o jsonpath='{.spec.containers[0].securityContext}'
```

**解決策**
Pod に必要なケーパビリティがあることを確認します

```yaml
securityContext:
  capabilities:
    add:
      - NET_ADMIN
      - SYS_ADMIN
```

{{% notice title="注意" style="info" %}}
厳格な Pod Security Policy を持つ一部の Kubernetes クラスターでは、これらのケーパビリティが許可されない場合があります。適切なポリシー例外を作成するために、クラスター管理者と協力する必要がある場合があります。
{{% /notice %}}

## ヘルプの取得

このガイドで取り上げられていない問題が発生した場合

1. **ThousandEyes サポート**: [support.thousandeyes.com](https://support.thousandeyes.com) で ThousandEyes サポートに問い合わせてください
2. **Splunk サポート**: Splunk Observability Cloud の問題については、[Splunk Support](https://www.splunk.com/en_us/support-and-services.html) にアクセスしてください
3. **コミュニティフォーラム**:
   - [ThousandEyes Community](https://community.thousandeyes.com)
   - [Splunk Community](https://community.splunk.com)

{{% notice title="ヒント" style="primary" icon="lightbulb" %}}
ヘルプを求める際は、より効果的にトラブルシューティングできるよう、関連するログ、Pod の説明、エラーメッセージを必ず含めてください。
{{% /notice %}}
