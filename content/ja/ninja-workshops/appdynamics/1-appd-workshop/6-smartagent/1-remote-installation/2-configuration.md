---
title: 2. 設定
weight: 2
---

Smart Agentのリモートインストールには、Smart Agentの設定用の `config.ini` とリモートホストおよび接続パラメータを定義する `remote.yaml` の2つの主要な設定ファイルが必要です。

## 設定ファイルの概要

両方の設定ファイルはSmart Agentのインストールディレクトリに配置します。

```bash
cd /home/ubuntu/appdsm
```

設定する2つのファイル:

- `config.ini` - すべてのリモートホストにデプロイされるSmart Agentの設定
- `remote.yaml` - リモートホストとSSH接続設定

## config.ini - Smart Agent設定

`config.ini` ファイルには、すべてのリモートホストにデプロイされるSmart Agentのメイン設定が含まれます。

**配置場所:** `/home/ubuntu/appdsm/config.ini`

### Controller設定

AppDynamics Controllerへの接続を設定します。

```ini
ControllerURL    = fso-tme.saas.appdynamics.com
ControllerPort   = 443
FMServicePort    = 443
AccountAccessKey = your-access-key-here
AccountName      = your-account-name
EnableSSL        = true
```

**主要パラメータ:**

- `ControllerURL`: AppDynamics SaaS Controllerのエンドポイント
- `ControllerPort`: ControllerのHTTPSポート（デフォルト: 443）
- `FMServicePort`: Flow Monitoringサービスポート
- `AccountAccessKey`: AppDynamicsアカウントのアクセスキー
- `AccountName`: AppDynamicsアカウント名
- `EnableSSL`: SSL/TLS暗号化を有効にする（本番環境では `true` にする）

### Common設定

エージェントのIDとポーリング動作を定義します。

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
- `ServiceName`: 論理的なグループ化のためのオプションのサービス名

### Telemetry設定

ロギングとプロファイリングを設定します。

```ini
[Telemetry]
LogLevel  = DEBUG
LogFile   = /opt/appdynamics/appdsmartagent/log.log
Profiling = false
```

**パラメータ:**

- `LogLevel`: ログの詳細度（`DEBUG`、`INFO`、`WARN`、`ERROR`）
- `LogFile`: リモートホスト上でログが書き込まれるパス
- `Profiling`: パフォーマンスプロファイリングを有効にする（`true`/`false`）

### TLSクライアント設定

プロキシとTLS設定を行います。

```ini
[TLSClientSetting]
Insecure        = false
AgentHTTPProxy  = 
AgentHTTPSProxy = 
AgentNoProxy    = 
```

**パラメータ:**

- `Insecure`: TLS証明書の検証をスキップする（本番環境では非推奨）
- `AgentHTTPProxy`: HTTPプロキシサーバーのURL（必要な場合）
- `AgentHTTPSProxy`: HTTPSプロキシサーバーのURL（必要な場合）
- `AgentNoProxy`: プロキシをバイパスするホストのカンマ区切りリスト

### Auto Discovery

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

- `RunAutoDiscovery`: アプリケーションを自動検出する（`true`/`false`）
- `ExcludeLabels`: 検出から除外するメトリクス
- `ExcludeProcesses`: モニタリングから除外するプロセス名
- `ExcludeUsers`: モニタリングから除外するユーザーアカウント
- `AutoDiscoveryTimeInterval`: 検出を実行する間隔（例: `4h`、`30m`）
- `AutoInstall`: 検出されたアプリケーションを自動インストールする

### Task設定

ネイティブ計装を設定します。

```ini
[TaskConfig]
NativeEnable        = true
UserPortalUserName  = 
UserPortalPassword  = 
UserPortalAuth      = none
AutoUpdateLdPreload = true
```

**パラメータ:**

- `NativeEnable`: ネイティブ計装を有効にする
- `AutoUpdateLdPreload`: LD_PRELOAD設定を自動更新する

## remote.yaml - リモートホスト設定

`remote.yaml` ファイルは、Smart Agentをインストールするリモートホストと接続パラメータを定義します。

**配置場所:** `/home/ubuntu/appdsm/remote.yaml`

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
- 多数のホストへのデプロイを高速化する場合は増やす
- ネットワークやリソースに制約がある場合は減らす

**remote_dir:** リモートホスト上のインストールディレクトリ

- デフォルト: `/opt/appdynamics/appdsmartagent`
- 絶対パスで指定する必要がある
- ユーザーに書き込み権限が必要

### プロトコル設定

**type:** 接続プロトコル

- 値: `ssh`

**auth.username:** 認証用のSSHユーザー名

- 例: `ubuntu`、`ec2-user`、`centos`
- リモートホストで設定されたユーザーと一致する必要がある

**auth.private_key_path:** SSH秘密鍵のパス

- 絶対パスで指定する必要がある
- 鍵にアクセス可能で適切な権限（600）が設定されている必要がある

**auth.privileged:** 昇格された権限でエージェントを実行する

- `true`: root/systemdサービスとしてインストール
- `false`: ユーザープロセスとしてインストール
- 推奨: 本番デプロイでは `true`

**auth.ignore_host_key_validation:** SSHホスト鍵の検証をスキップする

- `true`: 検証をスキップ（テスト時に便利）
- `false`: ホスト鍵を検証（本番環境で推奨）

**auth.known_hosts_path:** SSH known_hostsファイルのパス

- デフォルト: `/home/ubuntu/.ssh/known_hosts`
- ホスト鍵の検証が有効な場合に使用される

### ホスト定義

各ホストエントリに必要な項目:

**host:** リモートマシンのIPアドレスまたはホスト名

- IPv4、IPv6、またはホスト名が使用可能
- コントロールノードから到達可能である必要がある

**port:** SSHポート

- デフォルト: `22`
- SSHが非標準ポートで動作している場合は変更する

**user:** Smart Agentプロセスを所有するユーザーアカウント

- システム全体のインストールでは通常 `root`
- ユーザー固有のインストールでは一般ユーザーも可能

**group:** Smart Agentプロセスを所有するグループ

- 通常はユーザーと同じ（例: `root`）

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
必要に応じていくつでもホストを追加できます。`max_concurrency` 設定により、並列処理されるホスト数が制御されます。
{{% /notice %}}

## 設定の検証

インストールに進む前に、設定ファイルを検証します。

### remote.yamlの確認

```bash
cat /home/ubuntu/appdsm/remote.yaml
```

以下を確認します。

- すべてのホストIPアドレスが正しいこと
- SSH鍵のパスが有効であること
- リモートディレクトリのパスが適切であること

### config.iniの確認

```bash
cat /home/ubuntu/appdsm/config.ini
```

以下を検証します。

- Controller URLとアカウント情報が正しいこと
- ログファイルのパスが有効であること
- 設定が環境要件と一致していること

### YAML構文の検証

YAMLファイルが正しくフォーマットされていることを確認します。

```bash
python3 -c "import yaml; yaml.safe_load(open('/home/ubuntu/appdsm/remote.yaml'))"
```

コマンドがエラーなく完了すれば、YAML構文は有効です。

設定ファイルの準備ができたら、インストールに進みましょう。
