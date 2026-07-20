---
title: 1. 前提条件
weight: 1
---

リモートホストにSmart Agentをインストールする前に、以下の前提条件が整っていることを確認してください。

## 必要なアクセス権

- **SSHアクセス**: Smart AgentをインストールするすべてのリモートホストへのSSHアクセスが必要です
- **SSH秘密鍵**: 認証用のSSH秘密鍵が設定されていること
- **Sudo権限**: コントロールノードのユーザーがsmartagentctlを実行するためのsudo権限が必要です
- **リモートSSH**: リモートホストでSSHが有効でアクセス可能であること

## ディレクトリ構成

コントロールノードにSmart Agentのインストールディレクトリを設定します。

```bash
cd /home/ubuntu/appdsm
```

ディレクトリには以下が含まれます。

- `smartagentctl` - SmartAgentを管理するコマンドラインユーティリティ
- `smartagent` - SmartAgentバイナリ
- `config.ini` - メイン設定ファイル
- `remote.yaml` - リモートホスト設定ファイル
- `conf/` - 追加の設定ファイル
- `lib/` - 必要なライブラリ

## AppDynamicsアカウント情報

AppDynamicsアカウントから以下の情報が必要です。

- **Controller URL**: AppDynamics SaaSコントローラーのエンドポイント（例: `fso-tme.saas.appdynamics.com`）
- **Account Name**: AppDynamicsのアカウント名
- **Account Access Key**: AppDynamicsのアカウントアクセスキー
- **Controller Port**: 通常、HTTPS接続の場合は443

## ターゲットホストの要件

リモートホストは以下の要件を満たす必要があります。

- **オペレーティングシステム**: Ubuntu/Linuxベースのシステム
- **SSHサーバー**: SSHデーモンが実行中で接続を受け付けていること
- **ユーザーアカウント**: 適切な権限を持つユーザーアカウント（通常はroot）
- **ネットワークアクセス**: AppDynamics Controllerに到達できること
- **ディスク容量**: Smart Agentのインストールに十分な容量（通常100MB未満）

## セキュリティに関する考慮事項

作業を進める前に、以下のセキュリティベストプラクティスを確認してください。

1. **SSH鍵**: 強力なSSH鍵を使用します（RSA 4096ビットまたはED25519）
2. **アクセスキー**: AccountAccessKeyを安全に保管します
3. **ホスト鍵の検証**: 本番環境では、ホスト鍵の検証を計画します
4. **SSL/TLS**: コントローラーとの通信には常にSSL/TLSを使用します
5. **ログファイル**: 機密情報を含むログファイルへのアクセスを制限します

## 前提条件の確認

### SSH接続の確認

リモートホストへのSSH接続をテストします。

```bash
ssh -i /home/ubuntu/.ssh/id_rsa ubuntu@<remote-host-ip>
```

### SSH鍵のパーミッション確認

SSH鍵に適切なパーミッションが設定されていることを確認します。

```bash
chmod 600 /home/ubuntu/.ssh/id_rsa
```

### ネットワーク接続の確認

リモートホストが相互に、またインターネットに到達できることを確認します。

```bash
ping <remote-host-ip>
```

### Sudoアクセスの確認

sudo権限があることを確認します。

```bash
sudo -v
```

すべての前提条件が満たされていれば、設定に進む準備ができています。
