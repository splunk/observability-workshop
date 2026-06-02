---
title: ThousandEyes Agent
linkTitle: 2.1 ThousandEyes Agent
weight: 1
time: 20 minutes
description: ThousandEyes Enterprise Agent を Kubernetes にデプロイし、ThousandEyes Cloud に正しく登録されることを確認します。
---

このセクションでは、ThousandEyes Enterprise Agent を Kubernetes クラスターにデプロイする手順を説明します。

## インストール手順

### Step 1: ThousandEyes トークンの作成

1. ThousandEyes プラットフォーム [app.thousandeyes.com/login](https://app.thousandeyes.com/login) にログインします

2. **Network & App Synthetics > Agent Settings > Enterprise Agents > Add New Enterprise Agent** に移動します

3. **Appliance** タブをクリックします

4. **Account Group Token** をコピーします

5. トークンを Base64 エンコードします:

    {{< tabs >}}
    {{% tab title="Script" %}}

    ```bash
    echo -n 'your-token-here' | base64
    ```

    {{% /tab %}}

    {{% tab title="Example Output" %}}

    ```text
    dXabsfuenBabjeTZ3anVvxgyYds0cas=
    ```

    {{% /tab %}}
    {{< /tabs >}}

6. 次のステップで使用するため、Base64 エンコードされた出力を保存しておきます

    ![Get ThousandEyes Token](../../images/te1.gif?width=45vw)

### Step 2: Secret の作成

Base64 エンコードされたトークンを使って、`credentialsSecret.yaml` という名前のファイルを作成します:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: te-creds
type: Opaque
data:
  TEAGENT_ACCOUNT_TOKEN: <your-base64-encoded-token-here>
```

Secret を適用します:

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl apply -f credentialsSecret.yaml
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
secret/te-creds created
```

{{% /tab %}}
{{< /tabs >}}

### Step 3: Deployment の作成

下記のデプロイメントマニフェストを使って、`thousandEyesDeploy.yaml` という名前のファイルを作成します（`hostname` は `tihard` のように、自分のユーザー名でカスタマイズします）:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
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
      hostname: te-agent-USERNAME
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

{{% notice title="設定の説明" style="info" %}}

- エージェントはネットワークテストを実行するために、昇格された権限（`NET_ADMIN`、`SYS_ADMIN`）を必要とします
- 環境変数 `TEAGENT_INET: "4"` は IPv4 のみのモードを強制します（一部のネットワーク構成で必要です）
- `/sbin/my_init` コマンドはエージェントの適切な初期化とサービス管理に必要です
- `imagePullPolicy: Always` により、常に最新のイメージバージョンが取得されます
- `hostname` フィールドを調整して、ThousandEyes ダッシュボード上でエージェントを一意に識別できるようにします
- ThousandEyes Enterprise Agent はハードウェア要件が比較的高いため、環境に応じて調整が必要になる場合があります
{{% /notice %}}

Deployment を適用します:

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl apply -f thousandEyesDeploy.yaml
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
deployment.apps/thousandeyes created
```

{{% /tab %}}
{{< /tabs >}}

### Step 5: Deployment の確認

エージェントが稼働していることを確認します:

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl get pods
```

{{% /tab %}}
{{% tab title="Example Output" %}}
期待される出力です。起動するまで数回試行が必要な場合があります:

```text
NAME                            READY   STATUS    RESTARTS   AGE
thousandeyes-xxxxxxxxxx-xxxxx   1/1     Running   0          2m
```

{{% /tab %}}
{{< /tabs >}}

{{% notice title="Tip" style="info" %}}
次のコマンドを使用できます:

```bash
watch -n 1 kubectl get pods
```

これで Pod が稼働状態になるまで監視できます。何かの起動を待つ際にはいつでもこの方法を活用してください。
{{% /notice %}}

ログを確認して、エージェントが接続していることを確認します。下記のような出力になるまで少し時間がかかる場合があります。

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl logs -l app=thousandeyes
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
INFO: execution time 20 seconds.
INFO: rootfs setup successfully
********************************* setup_rootfs.sh end *******************************
Starting browserbot in installation mode
Getting image source signatures
Copying blob sha256:dee215ffc666313e1381d3e6e4299a4455503735b8df31c3fa161d2df50860a8
Copying config sha256:ed210e3e4a5bae1237f1bb44d72a05a2f1e5c6bfe7a7e73da179e2534269c459
Writing manifest to image destination
time="2026-05-12T22:08:37Z" level=warning msg="specgen \"cni_networks\" option is deprecated use the \"networks\" map instead"
Starting browserbot in daemon mode
```

{{% /tab %}}
{{< /tabs >}}

### Step 6: ThousandEyes ダッシュボードでの確認

ThousandEyes ダッシュボードで、エージェントが正常に登録されていることを確認します:

**Network & App Synthetics > Agent Settings** に移動して、新しく登録されたエージェントを確認します。
![ThousandEyes Agent List](../../images/te-agents.png?width=45vw)

{{% notice title="Success" style="success" icon="check" %}}
ThousandEyes Enterprise Agent が Kubernetes 上で稼働するようになりました。次に、Splunk Observability Cloud と統合します。
{{% /notice %}}

{{% notice title="トラブルシューティングガイダンス" style="primary" icon="warn" %}}
何らかの理由でエージェントが表示されない場合は、トークンが正しくエンコードされているか（最初のステップ）を確認してください。
{{% /notice %}}

## 背景

ThousandEyes は公式の Kubernetes デプロイメントドキュメントを提供していません。標準的なデプロイ方法は `docker run` コマンドを使用するため、再利用可能な Kubernetes マニフェストへの変換が困難です。このガイドは、本番環境で利用可能な Kubernetes 構成を提供することで、そのギャップを埋めます。
