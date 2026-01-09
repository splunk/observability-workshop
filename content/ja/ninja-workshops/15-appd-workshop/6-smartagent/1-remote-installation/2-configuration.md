---
title: 2. 構成
weight: 2
---

Smart Agent のリモートインストールには、2つの主要な構成ファイルが必要です：Smart Agent 設定用の `config.ini` と、リモートホストと接続パラメータを定義する `remote.yaml` です。

## 構成ファイルの概要

両方の構成ファイルは、Smart Agent のインストールディレクトリに配置する必要があります：

```bash
cd /home/ubuntu/appdsm
```

構成する2つのファイル：
- `config.ini` - すべてのリモートホストにデプロイされる Smart Agent 構成
- `remote.yaml` - リモートホストと SSH 接続設定

## config.ini - Smart Agent 構成

`config.ini` ファイルには、すべてのリモートホストにデプロイされるメインの Smart Agent 構成が含まれています。

**場所：** `/home/ubuntu/appdsm/config.ini`

### Controller 構成

AppDynamics Controller 接続を構成します：

```ini
ControllerURL    = fso-tme.saas.appdynamics.com
ControllerPort   = 443
FMServicePort    = 443
AccountAccessKey = your-access-key-here
AccountName      = your-account-name
EnableSSL        = true
```

**主要パラメータ：**
- `ControllerURL`：AppDynamics SaaS コントローラーエンドポイント
- `ControllerPort`：コントローラーの HTTPS ポート（デフォルト：443）
- `FMServicePort`：Flow Monitoring サービスポート
- `AccountAccessKey`：AppDynamics アカウントアクセスキー
- `AccountName`：AppDynamics アカウント名
- `EnableSSL`：SSL/TLS 暗号化を有効にする（本番環境では `true` にする必要があります）

### Common Configuration

エージェントの ID とポーリング動作を定義します：

```ini
[CommonConfig]
AgentName            = smartagent
PollingIntervalInSec = 300
Tags                 = environment:production,region:us-east
ServiceName          = my-application
```

**パラメータ：**
- `AgentName`：エージェントの名前識別子
- `PollingIntervalInSec`：エージェントがデータをポーリングする頻度（秒単位）
- `Tags`：エージェントを分類するためのカスタムタグ（カンマ区切り）
- `ServiceName`：論理グループ化のためのオプションのサービス名

### Telemetry 設定

ログとプロファイリングを構成します：

```ini
[Telemetry]
LogLevel  = DEBUG
LogFile   = /opt/appdynamics/appdsmartagent/log.log
Profiling = false
```

**パラメータ：**
- `LogLevel`：ログの詳細度（`DEBUG`、`INFO`、`WARN`、`ERROR`）
- `LogFile`：リモートホストでログが書き込まれるパス
- `Profiling`：パフォーマンスプロファイリングを有効にする（`true`/`false`）

### TLS クライアント設定

プロキシと TLS 設定を構成します：

```ini
[TLSClientSetting]
Insecure        = false
AgentHTTPProxy  =
AgentHTTPSProxy =
AgentNoProxy    =
```

**パラメータ：**
- `Insecure`：TLS 証明書の検証をスキップ（本番環境では推奨されません）
- `AgentHTTPProxy`：HTTP プロキシサーバー URL（必要な場合）
- `AgentHTTPSProxy`：HTTPS プロキシサーバー URL（必要な場合）
- `AgentNoProxy`：プロキシをバイパスするホストのカンマ区切りリスト

### Auto Discovery

自動アプリケーション検出を構成します：

```ini
[AutoDiscovery]
RunAutoDiscovery          = false
ExcludeLabels             = process.cpu.usage,process.memory.usage
ExcludeProcesses          =
ExcludeUsers              =
AutoDiscoveryTimeInterval = 4h
AutoInstall               = false
```

**パラメータ：**
- `RunAutoDiscovery`：アプリケーションを自動的に検出する（`true`/`false`）
- `ExcludeLabels`：検出から除外するメトリクス
- `ExcludeProcesses`：監視から除外するプロセス名
- `ExcludeUsers`：監視から除外するユーザーアカウント
- `AutoDiscoveryTimeInterval`：検出を実行する頻度（例：`4h`、`30m`）
- `AutoInstall`：検出されたアプリケーションを自動的にインストール

### Task Configuration

ネイティブ計装を構成します：

```ini
[TaskConfig]
NativeEnable        = true
UserPortalUserName  =
UserPortalPassword  =
UserPortalAuth      = none
AutoUpdateLdPreload = true
```

**パラメータ：**
- `NativeEnable`：ネイティブ計装を有効にする
- `AutoUpdateLdPreload`：LD_PRELOAD 設定を自動的に更新

## remote.yaml - リモートホスト構成

`remote.yaml` ファイルは、Smart Agent がインストールされるリモートホストと接続パラメータを定義します。

**場所：** `/home/ubuntu/appdsm/remote.yaml`

### 構成例

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

**max_concurrency：** 同時に処理するホストの最大数
- デフォルト：`4`
- 多くのホストへの高速デプロイのために増加
- ネットワークまたはリソースの制約がある場合は減少

**remote_dir：** リモートホストのインストールディレクトリ
- デフォルト：`/opt/appdynamics/appdsmartagent`
- 絶対パスである必要があります
- ユーザーは書き込み権限を持っている必要があります

### Protocol 構成

**type：** 接続プロトコル
- 値：`ssh`

**auth.username：** 認証用の SSH ユーザー名
- 例：`ubuntu`、`ec2-user`、`centos`
- リモートホストで構成されているユーザーと一致する必要があります

**auth.private_key_path：** SSH 秘密鍵へのパス
- 絶対パスである必要があります
- キーはアクセス可能で適切なパーミッション（600）を持っている必要があります

**auth.privileged：** 昇格した権限でエージェントを実行
- `true`：root/systemd サービスとしてインストール
- `false`：ユーザープロセスとしてインストール
- 推奨：本番デプロイでは `true`

**auth.ignore_host_key_validation：** SSH ホストキー検証をスキップ
- `true`：検証をスキップ（テストに便利）
- `false`：ホストキーを検証（本番環境で推奨）

**auth.known_hosts_path：** SSH known_hosts ファイルへのパス
- デフォルト：`/home/ubuntu/.ssh/known_hosts`
- ホストキー検証が有効な場合に使用

### ホスト定義

各ホストエントリには以下が必要です：

**host：** リモートマシンの IP アドレスまたはホスト名
- IPv4、IPv6、またはホスト名が使用可能
- Control Node から到達可能である必要があります

**port：** SSH ポート
- デフォルト：`22`
- SSH が非標準ポートで実行されている場合は変更

**user：** Smart Agent プロセスを所有するユーザーアカウント
- システム全体のインストールでは通常 `root`
- ユーザー固有のインストールでは通常のユーザーも可能

**group：** Smart Agent プロセスを所有するグループ
- 通常はユーザーと一致（例：`root`）

### ホストの追加

追加のリモートホストを追加するには、`hosts` リストに追加します：

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

{{% notice title="Tip" style="info" icon="info-circle" %}}
必要な数だけホストを追加できます。`max_concurrency` 設定で並列処理されるホスト数を制御します。
{{% /notice %}}

## 構成の確認

インストールを進める前に、構成ファイルを確認してください：

### remote.yaml の確認

```bash
cat /home/ubuntu/appdsm/remote.yaml
```

以下を確認します：
- すべてのホスト IP アドレスが正しいこと
- SSH キーパスが有効であること
- リモートディレクトリパスが適切であること

### config.ini の確認

```bash
cat /home/ubuntu/appdsm/config.ini
```

以下を確認します：
- Controller URL とアカウント情報が正しいこと
- ログファイルパスが有効であること
- 設定が環境要件に一致していること

### YAML 構文の検証

YAML ファイルが正しくフォーマットされていることを確認します：

```bash
python3 -c "import yaml; yaml.safe_load(open('/home/ubuntu/appdsm/remote.yaml'))"
```

コマンドがエラーなしで完了すれば、YAML 構文は有効です。

構成ファイルの準備ができたら、インストールを進めることができます。
