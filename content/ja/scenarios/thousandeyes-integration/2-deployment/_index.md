---
title: デプロイメント
linkTitle: 2. デプロイメント
weight: 2
time: 20 minutes
description: ThousandEyes Enterprise Agent を Kubernetes にデプロイし、ThousandEyes Cloud に正しく登録されることを確認します。
---

このセクションでは、KubernetesクラスターにThousandEyes Enterprise Agentをデプロイする手順を説明します。

## コンポーネント

デプロイメントは2つのファイルで構成されています：

### 1. シークレットファイル (`credentialsSecret.yaml`)

ThousandEyesエージェントトークン（base64エンコード済み）を含みます。このシークレットは、エージェントをThousandEyes Cloudで認証するためにデプロイメントから参照されます。

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: te-creds
type: Opaque
data:
  TEAGENT_ACCOUNT_TOKEN: <base64-encoded-token>
```

### 2. デプロイメントマニフェスト (`thousandEyesDeploy.yaml`)

以下の主要な設定でEnterprise AgentのPod構成を定義します：

- **Namespace**: `te-demo`（必要に応じてカスタマイズ）
- **Image**: Docker Hubの `thousandeyes/enterprise-agent:latest`
- **Hostname**: `te-agent-aleccham`（ThousandEyesダッシュボードに表示されます）
- **Capabilities**: ネットワークテストに `NET_ADMIN` と `SYS_ADMIN` が必要
- **Resources**:
  - メモリ制限: 3584Mi
  - メモリ要求: 2000Mi

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  namespace: te-demo
  name: thousandeyes
  labels:
    app: thousandeyes
spec:
  replicas: 1
  selector:
    matchLabels:
      app: thousandeyes
  template:
    metadata:
      labels:
        app: thousandeyes
    spec:
      hostname: te-agent-aleccham
      containers:
      - name: thousandeyes
        image: 'thousandeyes/enterprise-agent:latest'
        imagePullPolicy: Always
        command:
          - /sbin/my_init
        securityContext:
          capabilities:
            add:
              - NET_ADMIN
              - SYS_ADMIN
        env:
          - name: TEAGENT_ACCOUNT_TOKEN
            valueFrom:
              secretKeyRef:
                name: te-creds
                key: TEAGENT_ACCOUNT_TOKEN
          - name: TEAGENT_INET
            value: "4"
        resources:
          limits:
            memory: 3584Mi
          requests:
            memory: 2000Mi
```

{{% notice title="重要な注意事項" style="warning" %}}

- エージェントはネットワークテストを実行するために昇格した権限（`NET_ADMIN`、`SYS_ADMIN`）が必要です
- `TEAGENT_INET: "4"` 環境変数はIPv4専用モードを強制します（一部のネットワーク構成で必要）
- `/sbin/my_init` コマンドは、エージェントの適切な初期化とサービス管理に必要です
- `imagePullPolicy: Always` は常に最新のイメージバージョンをプルすることを保証します
- ThousandEyesダッシュボードでエージェントを一意に識別するために `hostname` フィールドを調整してください
- Kubernetes環境に合わせて `namespace` を変更してください
- ThousandEyes Enterprise Agentは比較的高いハードウェア要件があります。環境に応じてこれらを調整する必要がある場合があります
{{% /notice %}}

## インストール手順

### ステップ 1: ThousandEyes トークンの作成

1. [app.thousandeyes.com/login](https://app.thousandeyes.com/login) でThousandEyesプラットフォームにログインします

2. **Cloud & Enterprise Agents > Agent Settings > Add New Enterprise Agent** に移動します

3. **Account Group Token** をコピーします

4. トークンをBase64エンコードします：

   ```bash
   echo -n 'your-token-here' | base64
   ```

5. 次のステップのためにbase64エンコードされた出力を保存します

![Get ThousandEyes Token](../images/te1.gif)

### ステップ 2: Namespace の作成

Namespaceを作成します（存在しない場合）：

```bash
kubectl create namespace te-demo
```

### ステップ 3: シークレットの作成

base64エンコードされたトークンを含む `credentialsSecret.yaml` という名前のファイルを作成します：

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: te-creds
  namespace: te-demo
type: Opaque
data:
  TEAGENT_ACCOUNT_TOKEN: <your-base64-encoded-token-here>
```

シークレットを適用します：

```bash
kubectl apply -f credentialsSecret.yaml
```

### ステップ 4: デプロイメントの作成

上記のデプロイメントマニフェストを含む `thousandEyesDeploy.yaml` という名前のファイルを作成します（必要に応じてhostnameとnamespaceをカスタマイズしてください）。

デプロイメントを適用します：

```bash
kubectl apply -f thousandEyesDeploy.yaml
```

### ステップ 5: デプロイメントの確認

エージェントが実行中であることを確認します：

```bash
kubectl get pods -n te-demo
```

期待される出力：

```
NAME                            READY   STATUS    RESTARTS   AGE
thousandeyes-xxxxxxxxxx-xxxxx   1/1     Running   0          2m
```

エージェントが接続していることを確認するためにログをチェックします：

```bash
kubectl logs -n te-demo -l app=thousandeyes
```

### ステップ 6: ThousandEyes ダッシュボードでの確認

ThousandEyesダッシュボードでエージェントが正常に登録されたことを確認します：

**Cloud & Enterprise Agents > Agent Settings** に移動して、新しく登録されたエージェントを確認します。

{{% notice title="成功" style="success" icon="check" %}}
ThousandEyes Enterprise AgentがKubernetesで実行されています！次に、Splunk Observability Cloudとの統合を行います。
{{% /notice %}}

## 背景

ThousandEyesは公式のKubernetesデプロイメントドキュメントを提供していません。標準的なデプロイメント方法は `docker run` コマンドを使用するため、再利用可能なKubernetesマニフェストに変換することが困難です。このガイドは、本番環境対応のKubernetes構成を提供することでそのギャップを埋めます。
