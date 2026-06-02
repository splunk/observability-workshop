---
title: 1. 前提条件
weight: 1
---

リモートホストへの Smart Agent のインストールを開始する前に、以下の前提条件が整っていることを確認してください。

## 必要なアクセス権

- **SSH アクセス**: Smart Agent をインストールする予定のすべてのリモートホストに対して SSH アクセスが必要です
- **SSH 秘密鍵**: 認証用に構成された SSH 秘密鍵
- **sudo 権限**: コントロールノードのユーザーに smartagentctl を実行するための sudo 権限が必要です
- **リモート SSH**: リモートホストで SSH が有効化され、アクセス可能である必要があります

## ディレクトリ構造

Smart Agent のインストールディレクトリは、コントロールノード上に配置する必要があります。

```bash
cd /home/ubuntu/appdsm
```

ディレクトリには以下が含まれます。

- `smartagentctl` - SmartAgent を管理するためのコマンドラインユーティリティ
- `smartagent` - SmartAgent のバイナリ
- `config.ini` - メイン構成ファイル
- `remote.yaml` - リモートホスト構成ファイル
- `conf/` - 追加の構成ファイル
- `lib/` - 必要なライブラリ

## AppDynamics アカウント情報

AppDynamics アカウントから以下の情報が必要です。

- **Controller URL**: AppDynamics SaaS コントローラーのエンドポイント（例: `fso-tme.saas.appdynamics.com`）
- **Account Name**: AppDynamics のアカウント名
- **Account Access Key**: AppDynamics のアカウントアクセスキー
- **Controller Port**: 通常は HTTPS 接続用の 443

## ターゲットホストの要件

リモートホストは以下の要件を満たしている必要があります。

- **オペレーティングシステム**: Ubuntu/Linux ベースのシステム
- **SSH サーバー**: SSH デーモンが起動しており、接続を受け付けている
- **ユーザーアカウント**: 適切な権限を持つユーザーアカウント（通常は root）
- **ネットワークアクセス**: AppDynamics Controller に到達可能であること
- **ディスク容量**: Smart Agent のインストールに十分な空き容量（通常は 100MB 未満）

## セキュリティ上の考慮事項

作業を進める前に、以下のセキュリティのベストプラクティスを確認してください。

1. **SSH 鍵**: 強力な SSH 鍵を使用する（RSA 4096 ビットまたは ED25519）
2. **アクセスキー**: AccountAccessKey を安全に保管する
3. **ホスト鍵の検証**: 本番環境ではホスト鍵を検証する計画を立てる
4. **SSL/TLS**: コントローラーとの通信には常に SSL/TLS を使用する
5. **ログファイル**: 機密情報を含むログファイルへのアクセスを制限する

## 前提条件の確認

### SSH 接続性の確認

リモートホストへの SSH 接続をテストします。

```bash
ssh -i /home/ubuntu/.ssh/id_rsa ubuntu@<remote-host-ip>
```

### SSH 鍵のパーミッション確認

SSH 鍵に適切なパーミッションが設定されていることを確認します。

```bash
chmod 600 /home/ubuntu/.ssh/id_rsa
```

### ネットワーク接続性の確認

リモートホスト同士、およびインターネットに到達できることを確認します。

```bash
ping <remote-host-ip>
```

### sudo アクセスの確認

sudo 権限があることを確認します。

```bash
sudo -v
```

すべての前提条件が満たされていれば、構成のステップに進む準備が整っています。
