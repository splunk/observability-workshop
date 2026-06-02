---
title: トラブルシューティング
linkTitle: 7. トラブルシューティング
weight: 7
time: 15 minutes
description: ThousandEyes シナリオで発生しやすいデプロイ、接続、メトリクスストリーミング、トレース相関の問題を診断します。
---

このセクションでは、Kubernetes 上で ThousandEyes Enterprise Agent をデプロイおよび使用する際に遭遇する可能性のある一般的な問題について説明します。

## DNS 解決エラーでテストが失敗する

テストが DNS 解決エラーで失敗している場合は、ThousandEyes Pod 内から DNS を確認してください。

```bash
# Verify DNS resolution from within the pod
kubectl exec -n te-demo -it <pod-name> -- nslookup api-gateway.default.svc.cluster.local

# Check CoreDNS logs
kubectl logs -n kube-system -l k8s-app=kube-dns
```

**よくある原因:**

- 指定された namespace にサービスが存在しない
- サービス名または namespace のタイプミス
- CoreDNS が正常に動作していない

## 接続拒否エラー

接続拒否エラーが発生している場合は、以下を確認してください。

```bash
# Verify service endpoints exist
kubectl get endpoints -n default api-gateway

# Check if pods are ready
kubectl get pods -n default -l app=api-gateway

# Test connectivity from agent pod
kubectl exec -n te-demo -it <pod-name> -- curl -v http://api-gateway.default.svc.cluster.local:82/api/customer/owners
```

**よくある原因:**

- サービスをバックアップする Pod が存在しない（エンドポイントが空）
- Pod が Ready 状態ではない
- テスト URL で指定されたポートが間違っている
- サービスセレクターが Pod のラベルと一致していない

## ネットワークポリシーがトラフィックをブロックしている

ネットワークポリシーが ThousandEyes エージェントからのトラフィックをブロックしている場合:

```bash
# List network policies
kubectl get networkpolicies -n default

# Describe network policy
kubectl describe networkpolicy <policy-name> -n default
```

**解決策:**
`te-demo` namespace から各サービスへのトラフィックを許可するネットワークポリシーを作成します。

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

ThousandEyes エージェントの Pod が起動しない場合は、Pod のステータスとイベントを確認してください。

```bash
# Get pod status
kubectl get pods -n te-demo

# Describe pod to see events
kubectl describe pod -n te-demo <pod-name>

# Check logs
kubectl logs -n te-demo <pod-name>
```

**よくある原因:**

- リソース不足（メモリ／CPU）
- TEAGENT_ACCOUNT_TOKEN シークレットが無効または存在しない
- セキュリティコンテキストの capabilities が Pod Security Policy で許可されていない
- イメージプルエラー

**解決策:**

- OOMKilled が発生している場合はメモリ制限を引き上げる
- シークレットが正しく作成されているか確認する: `kubectl get secret te-creds -n te-demo -o yaml`
- Pod Security Policy が NET_ADMIN および SYS_ADMIN capabilities を許可しているか確認する
- イメージプルを確認する: `kubectl describe pod -n te-demo <pod-name>`

## エージェントが ThousandEyes ダッシュボードに表示されない

エージェントは動作しているものの、ThousandEyes ダッシュボードに表示されない場合:

```bash
# Check agent logs for connection issues
kubectl logs -n te-demo -l app=thousandeyes --tail=100
```

**よくある原因:**

- TEAGENT_ACCOUNT_TOKEN が無効または不正
- ネットワークの egress がブロックされている（ファイアウォールまたはネットワークポリシー）
- エージェントが ThousandEyes Cloud のサーバーに到達できない

**解決策:**

1. トークンが正しく、適切に base64 エンコードされていることを確認する
2. `*.thousandeyes.com` への egress が許可されているか確認する
3. エージェントがインターネットに到達できることを確認する:

```bash
kubectl exec -n te-demo -it <pod-name> -- curl -v https://api.thousandeyes.com
```

## Splunk Observability Cloud にデータが表示されない

ThousandEyes のデータが Splunk に表示されない場合:

**インテグレーション設定を確認します:**

1. ThousandEyes 側で OpenTelemetry インテグレーションが正しく設定されているかを確認する
2. Splunk の ingest エンドポイント URL が利用中の realm に一致しているかを確認する
3. `X-SF-Token` ヘッダーに有効な Splunk アクセストークンが含まれていることを確認する
4. テストがインテグレーションに割り当てられていることを確認する

**テストの割り当てを確認します:**

```bash
# Use ThousandEyes API to verify integration
curl -v https://api.thousandeyes.com/v7/stream \
  -H "Authorization: Bearer $BEARER_TOKEN"
```

**よくある原因:**

- エンドポイント URL の Splunk realm が間違っている
- Splunk アクセストークンが無効または期限切れ
- テストが OpenTelemetry インテグレーションに割り当てられていない
- インテグレーションが有効化または正しく保存されていない

## ThousandEyes に分散トレーシングが表示されない

メトリクスのストリーミングは動作しているものの、ThousandEyes の **Service Map** が空、またはトレースが見つからない場合:

**監視対象エンドポイントを確認します:**

- HTTP ヘッダーを受け入れる
- OpenTelemetry で計装されている
- ダウンストリームへトレースコンテキストを伝播する
- Splunk APM へトレースを送信する

**よくある原因:**

- エンドポイントが HTTP Server や API ターゲットではなくページ URL になっている
- サービスが計装されておらず、ThousandEyes がヘッダーを注入してもトレースが生成されない
- エンドポイントがローカルのヘルスレスポンスのみを返し、ダウンストリームのサービスを呼び出していない

**推奨される修正:**

1. ThousandEyes のテストを、計装済みのバックエンド API ルートに切り替える
2. 該当ルートのトレースが Splunk APM 上に既に存在することを確認する
3. ThousandEyes の分散トレーシングを有効化したうえで、テストを再実行する

## Splunk APM に ThousandEyes リンクが表示されない

Splunk APM でトレースは開けるものの、ThousandEyes のバックリンクやメタデータが表示されない場合:

**よくある原因:**

`b3` プロパゲーターが `trace_state` を上書きし、ThousandEyes が逆方向リンクのために保持しようとする値をクリアしてしまうことがあります。

**修正方法:**

計装対象のサービスに対して、プロパゲーターを明示的に指定します。

```bash
OTEL_PROPAGATORS=baggage,b3,tracecontext
```

環境変数を変更したら、計装対象のワークロードを再起動し、新しいトラフィックを生成してください。

## Splunk APM コネクタの認証エラー

ThousandEyes 側の **Generic Connector** が Splunk APM にクエリできない場合:

**以下を確認します:**

1. コネクタのターゲットが `https://api.<REALM>.signalfx.com` であること
2. コネクタで使用しているトークンが **API** スコープを持っていること
3. トークンを発行したユーザーが Splunk Observability Cloud で必要なロールを持っていること

{{% notice title="トークンに関する注意" style="info" %}}
OpenTelemetry のメトリクスストリームは Splunk の **Ingest** トークンを使用します。一方、ThousandEyes の APM 用 **Generic Connector** は Splunk の **API** トークンを使用します。これらを取り違えることが、インテグレーションが部分的にしか動作しない原因として最も多いものの 1 つです。
{{% /notice %}}

## メモリ使用量が多い

ThousandEyes エージェントの Pod が過剰にメモリを消費している場合:

```bash
# Check current memory usage
kubectl top pod -n te-demo

# Check for OOMKilled events
kubectl describe pod -n te-demo <pod-name> | grep -i oom
```

**解決策:**

1. デプロイメントのメモリ制限を引き上げる:

```yaml
resources:
  limits:
    memory: 4096Mi  # Increase from 3584Mi
  requests:
    memory: 2500Mi  # Increase from 2000Mi
```

1. エージェントに割り当てる同時実行テスト数を減らす
2. エージェントが不要なサービスを実行していないか確認する

## アクセス権限拒否エラー

エージェントのログにアクセス権限拒否エラーが表示される場合:

**セキュリティコンテキストを確認します:**

```bash
kubectl get pod -n te-demo <pod-name> -o jsonpath='{.spec.containers[0].securityContext}'
```

**解決策:**
Pod に必要な capabilities が設定されていることを確認します。

```yaml
securityContext:
  capabilities:
    add:
      - NET_ADMIN
      - SYS_ADMIN
```

{{% notice title="補足" style="info" %}}
厳格な Pod Security Policy が適用されている Kubernetes クラスタでは、これらの capabilities が許可されない場合があります。その場合は、クラスタ管理者と連携して適切なポリシー例外を作成する必要があるかもしれません。
{{% /notice %}}

## サポートを受ける

このガイドで扱われていない問題が発生した場合:

1. **ThousandEyes Support**: ThousandEyes サポートへ連絡 [support.thousandeyes.com](https://support.thousandeyes.com)
2. **Splunk Support**: Splunk Observability Cloud に関する問題は [Splunk Support](https://www.splunk.com/en_us/support-and-services.html) を参照
3. **コミュニティフォーラム**:
   - [ThousandEyes Community](https://community.thousandeyes.com)
   - [Splunk Community](https://community.splunk.com)

{{% notice title="ヒント" style="primary" icon="lightbulb" %}}
サポートを依頼する際は、トラブルシューティングを効率化するため、関連するログ、Pod の詳細情報、エラーメッセージを必ず添えてください。
{{% /notice %}}
