---
title: 1. 前提条件
weight: 1
---

リモートホストに Smart Agent をインストールする前に、以下の前提条件が満たされていることを確認してください：

## 必要なアクセス

- **SSH アクセス**：Smart Agent をインストールする予定のすべてのリモートホストへの SSH アクセスが必要です
- **SSH 秘密鍵**：認証用に構成された SSH 秘密鍵
- **Sudo 権限**：Control Node ユーザーは smartagentctl を実行するために sudo 権限が必要です
- **リモート SSH**：リモートホストで SSH が有効になっており、アクセス可能である必要があります

## ディレクトリ構造

Smart Agent のインストールディレクトリは、Control Node に設定されている必要があります：

```bash
cd /home/ubuntu/appdsm
```

ディレクトリには以下が含まれます：

- `smartagentctl` - SmartAgent を管理するためのコマンドラインユーティリティ
- `smartagent` - SmartAgent バイナリ
- `config.ini` - メイン構成ファイル
- `remote.yaml` - リモートホスト構成ファイル
- `conf/` - 追加の構成ファイル
- `lib/` - 必要なライブラリ

## AppDynamics アカウント情報

AppDynamics アカウントから以下の情報が必要です：

- **Controller URL**：AppDynamics SaaS コントローラーエンドポイント（例：`fso-tme.saas.appdynamics.com`）
- **Account Name**：AppDynamics アカウント名
- **Account Access Key**：AppDynamics アカウントアクセスキー
- **Controller Port**：通常、HTTPS 接続の場合は 443

## ターゲットホストの要件

リモートホストは以下の要件を満たす必要があります：

- **オペレーティングシステム**：Ubuntu/Linux ベースのシステム
- **SSH サーバー**：SSH デーモンが実行中で接続を受け入れている状態
- **ユーザーアカウント**：適切な権限を持つユーザーアカウント（通常は root）
- **ネットワークアクセス**：AppDynamics Controller に到達できること
- **ディスク容量**：Smart Agent のインストールに十分な容量（通常 100MB 未満）

## セキュリティに関する考慮事項

続行する前に、以下のセキュリティベストプラクティスを確認してください：

1. **SSH キー**：強力な SSH キーを使用（RSA 4096 ビットまたは ED25519）
2. **アクセスキー**：AccountAccessKey を安全に保管
3. **ホストキー検証**：本番環境では、ホストキーの検証を計画
4. **SSL/TLS**：コントローラー通信には常に SSL/TLS を使用
5. **ログファイル**：機密情報を含むログファイルへのアクセスを制限

## 前提条件の確認

### SSH 接続の確認

リモートホストへの SSH 接続をテストします：

```bash
ssh -i /home/ubuntu/.ssh/id_rsa ubuntu@<remote-host-ip>
```

### SSH キーのパーミッションの確認

SSH キーに適切なパーミッションがあることを確認します：

```bash
chmod 600 /home/ubuntu/.ssh/id_rsa
```

### ネットワーク接続の確認

リモートホストが相互に、およびインターネットに到達できることを確認します：

```bash
ping <remote-host-ip>
```

### Sudo アクセスの確認

sudo 権限があることを確認します：

```bash
sudo -v
```

すべての前提条件が満たされていれば、構成を開始する準備ができています。
