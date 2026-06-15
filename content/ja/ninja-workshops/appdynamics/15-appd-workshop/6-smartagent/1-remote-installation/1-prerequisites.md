---
title: 1. 前提条件
weight: 1
---

リモートホストに Smart Agent をインストールする前に、以下の前提条件が整っていることを確認してください。

## 必要なアクセス

- **SSH アクセス**: Smart Agent をインストールする予定のすべてのリモートホストへの SSH アクセスが必要です
- **SSH 秘密鍵**: 認証用に設定された SSH 秘密鍵が必要です
- **Sudo 権限**: コントロールノードのユーザーには smartagentctl を実行するための sudo 権限が必要です
- **リモート SSH**: リモートホストで SSH が有効になっており、アクセス可能である必要があります

## ディレクトリ構造

コントロールノードに Smart Agent のインストールディレクトリを設定する必要があります

```bash
cd /home/ubuntu/appdsm
```

ディレクトリには以下が含まれています

- `smartagentctl` - SmartAgent を管理するためのコマンドラインユーティリティ
- `smartagent` - SmartAgent バイナリ
- `config.ini` - メイン設定ファイル
- `remote.yaml` - リモートホスト設定ファイル
- `conf/` - 追加の設定ファイル
- `lib/` - 必要なライブラリ

## AppDynamics アカウント情報

AppDynamics アカウントから以下の情報が必要です

- **Controller URL**: AppDynamics SaaS コントローラーのエンドポイント（例`fso-tme.saas.appdynamics.com`）
- **Account Name**: AppDynamics のアカウント名
- **Account Access Key**: AppDynamics のアカウントアクセスキー
- **Controller Port**: 通常、HTTPS 接続の場合は 443

## ターゲットホストの要件

リモートホストは以下の要件を満たす必要があります

- **オペレーティングシステム**: Ubuntu/Linux ベースのシステム
- **SSH サーバー**: SSH デーモンが実行中で接続を受け付けている状態
- **ユーザーアカウント**: 適切な権限を持つユーザーアカウント（通常は root）
- **ネットワークアクセス**: AppDynamics Controller に到達可能であること
- **ディスク容量**: Smart Agent のインストールに十分な容量（通常 100MB 未満）

## セキュリティに関する考慮事項

作業を進める前に、以下のセキュリティのベストプラクティスを確認してください

1. **SSH 鍵**: 強力な SSH 鍵を使用してください（RSA 4096 ビットまたは ED25519）
2. **アクセスキー**: AccountAccessKey を安全に保管してください
3. **ホスト鍵の検証**: 本番環境では、ホスト鍵の検証を計画してください
4. **SSL/TLS**: コントローラーとの通信には常に SSL/TLS を使用してください
5. **ログファイル**: 機密情報を含むログファイルへのアクセスを制限してください

## 前提条件の確認

### SSH 接続の確認

リモートホストへの SSH 接続をテストします

```bash
ssh -i /home/ubuntu/.ssh/id_rsa ubuntu@<remote-host-ip>
```

### SSH 鍵の権限の確認

SSH 鍵に適切な権限が設定されていることを確認します

```bash
chmod 600 /home/ubuntu/.ssh/id_rsa
```

### ネットワーク接続の確認

リモートホストが相互に通信でき、インターネットに到達できることを確認します

```bash
ping <remote-host-ip>
```

### Sudo アクセスの確認

sudo 権限があることを確認します

```bash
sudo -v
```

すべての前提条件が満たされていれば、設定に進む準備ができています！
