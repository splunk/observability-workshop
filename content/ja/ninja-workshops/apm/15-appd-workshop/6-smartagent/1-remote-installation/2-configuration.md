---
title: 2. 設定
weight: 2
---

Smart Agent のリモートインストールには、2 つの主要な設定ファイルが必要です。Smart Agent の設定用の `config.ini` と、リモートホストおよび接続パラメータを定義する `remote.yaml` です。

## 設定ファイルの概要

両方の設定ファイルは Smart Agent インストールディレクトリ内に配置する必要があります。

```bash
cd /home/ubuntu/appdsm
```

設定する 2 つのファイルは次のとおりです。

- `config.ini` - すべてのリモートホストにデプロイされる Smart Agent 設定
- `remote.yaml` - リモートホストおよび SSH 接続設定

## config.ini - Smart Agent の設定

`config.ini` ファイルには、すべてのリモートホストにデプロイされる Smart Agent のメイン設定が含まれます。

**場所:** `/home/ubuntu/appdsm/config.ini`

### Controller の設定

AppDynamics Controller への接続を設定します。

```ini
ControllerURL    = fso-tme.saas.appdynamics.com
ControllerPort   = 443
FMServicePort    = 443
AccountAccessKey = your-access-key-here
AccountName      = your-account-name
EnableSSL        = true
```

**主要なパラメータ:**

- `ControllerURL`: AppDynamics SaaS コントローラーのエンドポイント
- `ControllerPort`: コントローラー用の HTTPS ポート (デフォルト: 443)
- `FMServicePort`: Flow Monitoring サービスのポート
- `AccountAccessKey`: AppDynamics アカウントのアクセスキー
- `AccountName`: AppDynamics アカウント名
- `EnableSSL`: SSL/TLS 暗号化を有効化 (本番環境では `true` を推奨)

### 共通設定

エージェントのアイデンティティとポーリング動作を定義します。

```ini
[CommonConfig]
AgentName            = smartagent
PollingIntervalInSec = 300
Tags                 = environment:production,region:us-east
ServiceName          = my-application
```

**パラメータ:**

- `AgentName`: エージェントの名前識別子
- `PollingIntervalInSec`: エージェントがデータをポーリングする頻度 (秒単位)
- `Tags`: エージェントを分類するためのカスタムタグ (カンマ区切り)
- `ServiceName`: 論理的なグループ化のためのオプションのサービス名

### Telemetry 設定

ロギングとプロファイリングを設定します。

```ini
[Telemetry]
LogLevel  = DEBUG
LogFile   = /opt/appdynamics/appdsmartagent/log.log
Profiling = false
```

**パラメータ:**

- `LogLevel`: ロギングの詳細度 (`DEBUG`, `INFO`, `WARN`, `ERROR`)
- `LogFile`: リモートホストでログが書き込まれるパス
- `Profiling`: パフォーマンスプロファイリングの有効化 (`true`/`false`)

### TLS クライアント設定

プロキシおよび TLS の設定を行います。

```ini
[TLSClientSetting]
Insecure        = false
AgentHTTPProxy  = 
AgentHTTPSProxy = 
AgentNoProxy    = 
```

**パラメータ:**

- `Insecure`: TLS 証明書の検証をスキップ (本番環境では非推奨)
- `AgentHTTPProxy`: HTTP プロキシサーバーの URL (必要な場合)
- `AgentHTTPSProxy`: HTTPS プロキシサーバーの URL (必要な場合)
- `AgentNoProxy`: プロキシをバイパスするホストのカンマ区切りリスト

### 自動検出

アプリケーションの自動検出を設定します。

```ini
[AutoDiscovery]
RunAutoDiscovery          = false
ExcludeLabels             = process.cpu.usage,process.memory.usage
ExcludeProcesses          = 
ExcludeUsers              = 
AutoDiscoveryTimeInterval = 4h
AutoInstall               = false
```

**パラメータ:**

- `RunAutoDiscovery`: アプリケーションを自動検出する (`true`/`false`)
- `ExcludeLabels`: 検出から除外するメトリクス
- `ExcludeProcesses`: 監視から除外するプロセス名
- `ExcludeUsers`: 監視から除外するユーザーアカウント
- `AutoDiscoveryTimeInterval`: 検出を実行する頻度 (例: `4h`、`30m`)
- `AutoInstall`: 検出されたアプリケーションを自動インストール

### タスク設定

ネイティブインスツルメンテーションを設定します。

```ini
[TaskConfig]
NativeEnable        = true
UserPortalUserName  = 
UserPortalPassword  = 
UserPortalAuth      = none
AutoUpdateLdPreload = true
```

**パラメータ:**

- `NativeEnable`: ネイティブインスツルメンテーションを有効化
- `AutoUpdateLdPreload`: LD_PRELOAD 設定を自動更新

## remote.yaml - リモートホストの設定

`remote.yaml` ファイルでは、Smart Agent をインストールするリモートホストと接続パラメータを定義します。

**場所:** `/home/ubuntu/appdsm/remote.yaml`

### 設定例

```yaml
max_concurrency: 4
remote_dir: "/opt/appdynamics/appdsmartagent"
protocol:
  type: ssh
  auth:
    username: ubuntu
    private_key_path: /home/ubuntu/.ssh/id_rsa
    privileged: true
    ignore_host_key_validation: true
    known_hosts_path: /home/ubuntu/.ssh/known_hosts
hosts:
  - host: "172.31.1.243"
    port: 22
    user: root
    group: root
  - host: "172.31.1.48"
    port: 22
    user: root
    group: root
  - host: "172.31.1.142"
    port: 22
    user: root
    group: root
  - host: "172.31.1.5"
    port: 22
    user: root
    group: root
```

### グローバル設定

**max_concurrency:** 同時に処理するホストの最大数

- デフォルト: `4`
- 多数のホストへ高速にデプロイする場合は増やします
- ネットワークやリソースの制約がある場合は減らします

**remote_dir:** リモートホスト上のインストールディレクトリ

- デフォルト: `/opt/appdynamics/appdsmartagent`
- 絶対パスである必要があります
- ユーザーには書き込み権限が必要です

### プロトコル設定

**type:** 接続プロトコル

- 値: `ssh`

**auth.username:** 認証用の SSH ユーザー名

- 例: `ubuntu`、`ec2-user`、`centos`
- リモートホストで設定されているユーザーと一致する必要があります

**auth.private_key_path:** SSH 秘密鍵のパス

- 絶対パスである必要があります
- 鍵にアクセスでき、適切なパーミッション (600) が設定されている必要があります

**auth.privileged:** 昇格された権限でエージェントを実行

- `true`: root / systemd サービスとしてインストール
- `false`: ユーザープロセスとしてインストール
- 推奨: 本番デプロイでは `true`

**auth.ignore_host_key_validation:** SSH ホストキー検証をスキップ

- `true`: 検証をスキップ (テストに便利)
- `false`: ホストキーを検証 (本番環境で推奨)

**auth.known_hosts_path:** SSH known_hosts ファイルのパス

- デフォルト: `/home/ubuntu/.ssh/known_hosts`
- ホストキー検証が有効な場合に使用されます

### ホスト定義

各ホストエントリには以下が必要です。

**host:** リモートマシンの IP アドレスまたはホスト名

- IPv4、IPv6、またはホスト名が使用可能です
- 制御ノードから到達可能である必要があります

**port:** SSH ポート

- デフォルト: `22`
- SSH が標準以外のポートで動作している場合は変更します

**user:** Smart Agent プロセスを所有するユーザーアカウント

- システム全体のインストールでは通常 `root`
- ユーザー固有のインストールでは一般ユーザーも指定可能

**group:** Smart Agent プロセスを所有するグループ

- 通常はユーザーと一致します (例: `root`)

### ホストの追加

リモートホストを追加するには、`hosts` リストに追記します。

```yaml
hosts:
  - host: "10.0.1.10"
    port: 22
    user: root
    group: root
  - host: "10.0.1.11"
    port: 22
    user: root
    group: root
```

{{% notice title="ヒント" style="info" icon="info-circle" %}}
必要に応じて任意の数のホストを追加できます。`max_concurrency` 設定によって並列処理されるホスト数が制御されます。
{{% /notice %}}

## 設定の確認

インストールに進む前に、設定ファイルを確認します。

### remote.yaml の確認

```bash
cat /home/ubuntu/appdsm/remote.yaml
```

次の点を確認します。

- すべてのホスト IP アドレスが正しいこと
- SSH キーのパスが有効であること
- リモートディレクトリのパスが適切であること

### config.ini の確認

```bash
cat /home/ubuntu/appdsm/config.ini
```

次の点を確認します。

- Controller URL とアカウント情報が正しいこと
- ログファイルのパスが有効であること
- 設定が環境要件に合致していること

### YAML 構文の検証

YAML ファイルが正しくフォーマットされていることを確認します。

```bash
python3 -c "import yaml; yaml.safe_load(open('/home/ubuntu/appdsm/remote.yaml'))"
```

コマンドがエラーなく完了すれば、YAML 構文は有効です。

設定ファイルの準備が完了したら、インストールに進みます。
