---
title: 2. 設定
weight: 2
---

Smart Agent のリモートインストールには、Smart Agent の設定用の `config.ini` とリモートホストおよび接続パラメータを定義する `remote.yaml` の2つの主要な設定ファイルが必要です。

## 設定ファイルの概要

両方の設定ファイルは Smart Agent のインストールディレクトリに配置する必要があります:

```bash
cd /home/ubuntu/appdsm
```

設定する2つのファイル:

- `config.ini` - すべてのリモートホストにデプロイされる Smart Agent の設定
- `remote.yaml` - リモートホストと SSH 接続の設定

## config.ini - Smart Agent の設定

`config.ini` ファイルには、すべてのリモートホストにデプロイされる Smart Agent のメイン設定が含まれています。

**場所:** `/home/ubuntu/appdsm/config.ini`

### Controller の設定

AppDynamics Controller への接続を設定します:

```ini
ControllerURL    = fso-tme.saas.appdynamics.com
ControllerPort   = 443
FMServicePort    = 443
AccountAccessKey = your-access-key-here
AccountName      = your-account-name
EnableSSL        = true
```

**主要パラメータ:**

- `ControllerURL`: AppDynamics SaaS Controller のエンドポイント
- `ControllerPort`: Controller の HTTPS ポート（デフォルト: 443）
- `FMServicePort`: Flow Monitoring サービスのポート
- `AccountAccessKey`: AppDynamics アカウントのアクセスキー
- `AccountName`: AppDynamics アカウント名
- `EnableSSL`: SSL/TLS 暗号化を有効にする（本番環境では `true` にする必要があります）

### 共通設定

エージェントの識別情報とポーリング動作を定義します:

```ini
[CommonConfig]
AgentName            = smartagent
PollingIntervalInSec = 300
Tags                 = environment:production,region:us-east
ServiceName          = my-application
```

**パラメータ:**

- `AgentName`: エージェントの名前識別子
- `PollingIntervalInSec`: エージェントがデータをポーリングする間隔（秒単位）
- `Tags`: エージェントを分類するためのカスタムタグ（カンマ区切り）
- `ServiceName`: 論理グループ化のためのオプションのサービス名

### テレメトリ設定

ログとプロファイリングを設定します:

```ini
[Telemetry]
LogLevel  = DEBUG
LogFile   = /opt/appdynamics/appdsmartagent/log.log
Profiling = false
```

**パラメータ:**

- `LogLevel`: ログの詳細レベル（`DEBUG`、`INFO`、`WARN`、`ERROR`）
- `LogFile`: リモートホストでログが書き込まれるパス
- `Profiling`: パフォーマンスプロファイリングを有効にする（`true`/`false`）

### TLS クライアント設定

プロキシと TLS の設定を行います:

```ini
[TLSClientSetting]
Insecure        = false
AgentHTTPProxy  = 
AgentHTTPSProxy = 
AgentNoProxy    = 
```

**パラメータ:**

- `Insecure`: TLS 証明書の検証をスキップする（本番環境では推奨されません）
- `AgentHTTPProxy`: HTTP プロキシサーバーの URL（必要な場合）
- `AgentHTTPSProxy`: HTTPS プロキシサーバーの URL（必要な場合）
- `AgentNoProxy`: プロキシをバイパスするホストのカンマ区切りリスト

### 自動検出

アプリケーションの自動検出を設定します:

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

- `RunAutoDiscovery`: アプリケーションを自動検出する（`true`/`false`）
- `ExcludeLabels`: 検出から除外するメトリクス
- `ExcludeProcesses`: 監視から除外するプロセス名
- `ExcludeUsers`: 監視から除外するユーザーアカウント
- `AutoDiscoveryTimeInterval`: 検出を実行する間隔（例: `4h`、`30m`）
- `AutoInstall`: 検出されたアプリケーションを自動インストールする

### タスク設定

ネイティブインストルメンテーションを設定します:

```ini
[TaskConfig]
NativeEnable        = true
UserPortalUserName  = 
UserPortalPassword  = 
UserPortalAuth      = none
AutoUpdateLdPreload = true
```

**パラメータ:**

- `NativeEnable`: ネイティブインストルメンテーションを有効にする
- `AutoUpdateLdPreload`: LD_PRELOAD 設定を自動更新する

## remote.yaml - リモートホストの設定

`remote.yaml` ファイルは、Smart Agent がインストールされるリモートホストと接続パラメータを定義します。

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
- 多数のホストへのデプロイを高速化するには値を増やします
- ネットワークやリソースの制約がある場合は値を減らします

**remote_dir:** リモートホスト上のインストールディレクトリ

- デフォルト: `/opt/appdynamics/appdsmartagent`
- 絶対パスである必要があります
- ユーザーが書き込み権限を持っている必要があります

### プロトコル設定

**type:** 接続プロトコル

- 値: `ssh`

**auth.username:** 認証用の SSH ユーザー名

- 例: `ubuntu`、`ec2-user`、`centos`
- リモートホストで設定されているユーザーと一致する必要があります

**auth.private_key_path:** SSH 秘密鍵のパス

- 絶対パスである必要があります
- 鍵はアクセス可能で適切なパーミッション（600）が設定されている必要があります

**auth.privileged:** 昇格した権限でエージェントを実行する

- `true`: root/systemd サービスとしてインストール
- `false`: ユーザープロセスとしてインストール
- 推奨: 本番デプロイでは `true`

**auth.ignore_host_key_validation:** SSH ホスト鍵の検証をスキップする

- `true`: 検証をスキップ（テスト時に便利）
- `false`: ホスト鍵を検証（本番環境で推奨）

**auth.known_hosts_path:** SSH known_hosts ファイルのパス

- デフォルト: `/home/ubuntu/.ssh/known_hosts`
- ホスト鍵の検証が有効な場合に使用されます

### ホスト定義

各ホストエントリには以下が必要です:

**host:** リモートマシンの IP アドレスまたはホスト名

- IPv4、IPv6、またはホスト名を使用できます
- コントロールノードから到達可能である必要があります

**port:** SSH ポート

- デフォルト: `22`
- SSH が非標準ポートで実行されている場合は変更します

**user:** Smart Agent プロセスを所有するユーザーアカウント

- システム全体のインストールでは通常 `root`
- ユーザー固有のインストールでは一般ユーザーも使用可能

**group:** Smart Agent プロセスを所有するグループ

- 通常はユーザーと一致します（例: `root`）

### ホストの追加

リモートホストを追加するには、`hosts` リストに追記します:

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
必要な数だけホストを追加できます。`max_concurrency` 設定で並列処理されるホスト数を制御します。
{{% /notice %}}

## 設定の確認

インストールに進む前に、設定ファイルを確認します:

### remote.yaml の確認

```bash
cat /home/ubuntu/appdsm/remote.yaml
```

以下を確認してください:

- すべてのホスト IP アドレスが正しいこと
- SSH 鍵のパスが有効であること
- リモートディレクトリのパスが適切であること

### config.ini の確認

```bash
cat /home/ubuntu/appdsm/config.ini
```

以下を検証してください:

- Controller の URL とアカウント情報が正しいこと
- ログファイルのパスが有効であること
- 設定が環境の要件と一致していること

### YAML 構文の検証

YAML ファイルが正しくフォーマットされていることを確認します:

```bash
python3 -c "import yaml; yaml.safe_load(open('/home/ubuntu/appdsm/remote.yaml'))"
```

コマンドがエラーなしで完了すれば、YAML 構文は有効です。

設定ファイルの準備ができたら、インストールに進むことができます！
