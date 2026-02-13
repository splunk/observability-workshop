---
title: 1. 前提条件
weight: 1
---

リモートホストにSmart Agentをインストールする前に、以下の前提条件が満たされていることを確認してください：

## 必要なアクセス

- **SSH アクセス**：Smart Agentをインストールする予定のすべてのリモートホストへのSSHアクセスが必要です
- **SSH 秘密鍵**：認証用に構成されたSSH秘密鍵
- **Sudo 権限**：Control Nodeユーザーはsmartagentctlを実行するためにsudo権限が必要です
- **リモート SSH**：リモートホストでSSHが有効になっており、アクセス可能である必要があります

## ディレクトリ構造

Smart Agentのインストールディレクトリは、Control Nodeに設定されている必要があります：

```bash
cd /home/ubuntu/appdsm
```

ディレクトリには以下が含まれます：

- `smartagentctl` - SmartAgentを管理するためのコマンドラインユーティリティ
- `smartagent` - SmartAgentバイナリ
- `config.ini` - メイン構成ファイル
- `remote.yaml` - リモートホスト構成ファイル
- `conf/` - 追加の構成ファイル
- `lib/` - 必要なライブラリ

## AppDynamics アカウント情報

AppDynamicsアカウントから以下の情報が必要です：

- **Controller URL**：AppDynamics SaaSコントローラーエンドポイント（例：`fso-tme.saas.appdynamics.com`）
- **Account Name**：AppDynamicsアカウント名
- **Account Access Key**：AppDynamicsアカウントアクセスキー
- **Controller Port**：通常、HTTPS接続の場合は443

## ターゲットホストの要件

リモートホストは以下の要件を満たす必要があります：

- **オペレーティングシステム**：Ubuntu/Linuxベースのシステム
- **SSH サーバー**：SSHデーモンが実行中で接続を受け入れている状態
- **ユーザーアカウント**：適切な権限を持つユーザーアカウント（通常はroot）
- **ネットワークアクセス**：AppDynamics Controllerに到達できること
- **ディスク容量**：Smart Agentのインストールに十分な容量（通常100MB未満）

## セキュリティに関する考慮事項

続行する前に、以下のセキュリティベストプラクティスを確認してください：

1. **SSH キー**：強力なSSHキーを使用（RSA 4096ビットまたはED25519）
2. **アクセスキー**：AccountAccessKeyを安全に保管
3. **ホストキー検証**：本番環境では、ホストキーの検証を計画
4. **SSL/TLS**：コントローラー通信には常にSSL/TLSを使用
5. **ログファイル**：機密情報を含むログファイルへのアクセスを制限

## 前提条件の確認

### SSH 接続の確認

リモートホストへのSSH接続をテストします：

```bash
ssh -i /home/ubuntu/.ssh/id_rsa ubuntu@<remote-host-ip>
```

### SSH キーのパーミッションの確認

SSHキーに適切なパーミッションがあることを確認します：

```bash
chmod 600 /home/ubuntu/.ssh/id_rsa
```

### ネットワーク接続の確認

リモートホストが相互に、およびインターネットに到達できることを確認します：

```bash
ping <remote-host-ip>
```

### Sudo アクセスの確認

sudo権限があることを確認します：

```bash
sudo -v
```

すべての前提条件が満たされていれば、構成を開始する準備ができています。
