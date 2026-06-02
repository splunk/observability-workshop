---
title: 3. インストールと起動
weight: 3
---

設定ファイルの準備が完了したので、`smartagentctl` コマンドラインツールを使用してリモートホストに Smart Agent をインストールして起動できます。

## インストールプロセスの概要

インストールプロセスには以下が含まれます。

1. **接続**: 定義されたすべてのホストに対して SSH 接続を確立します
2. **転送**: Smart Agent のバイナリと設定をリモートホストにコピーします
3. **インストール**: 各ホストの `/opt/appdynamics/appdsmartagent/` に Smart Agent をインストールします
4. **起動**: 各リモートホストで Smart Agent プロセスを起動します
5. **ロギング**: コンソールとログファイルに詳細な進行状況を出力します

## ステップ 1: インストールディレクトリへの移動

Smart Agent インストールディレクトリに移動します。

```bash
cd /home/ubuntu/appdsm
```

## ステップ 2: 設定ファイルの確認

インストールを開始する前に、設定ファイルが正しくセットアップされていることを確認します。

### リモートホスト設定の確認

```bash
cat remote.yaml
```

すべてのホスト IP アドレス、ポート、SSH 設定が正しいことを確認してください。

### エージェント設定の確認

```bash
cat config.ini
```

コントローラーの URL、アカウント認証情報、その他の設定が正確であることを確認してください。

## ステップ 3: リモートホストでの Smart Agent の起動

`remote.yaml` で定義されたすべてのリモートホストで Smart Agent を起動するには、次のコマンドを実行します。

```bash
sudo ./smartagentctl start --remote --verbose
```

### コマンドの内訳

- `sudo`: 特権操作に必要です
- `./smartagentctl`: 制御ユーティリティです
- `start`: Smart Agent を起動するコマンドです
- `--remote`: リモートホストへデプロイします（`remote.yaml` から読み込みます）
- `--verbose`: 詳細なデバッグログを有効にします

{{% notice title="注意" style="warning" icon="triangle-exclamation" %}}
`--verbose` フラグは、インストールの進行状況に関する詳細な出力を提供し、問題の特定に役立つため、強く推奨されます。
{{% /notice %}}

## ステップ 4: インストールの監視

`--verbose` フラグは、以下を含む詳細な出力を提供します。

- SSH 接続ステータス
- ファイル転送の進行状況
- 各ホストでのインストール手順
- エージェントの起動ステータス
- エラーや警告

### 期待される出力

次のような出力が表示されるはずです。

```
Starting Smart Agent deployment to remote hosts...
Connecting to 172.31.1.243:22...
Connection successful: 172.31.1.243
Transferring Smart Agent binaries...
Installing Smart Agent on 172.31.1.243...
Starting Smart Agent on 172.31.1.243...
Smart Agent started successfully on 172.31.1.243

Connecting to 172.31.1.48:22...
...
```

## ステップ 5: インストールの確認

インストールが完了したら、リモートホストで Smart Agent が稼働していることを確認します。

### リモートでのステータス確認

status コマンドを使用して、すべてのリモートホストを確認します。

```bash
sudo ./smartagentctl status --remote --verbose
```

これにより、各ホストにクエリを実行し、Smart Agent が稼働しているかどうかを報告します。

### コントロールノードでのログ確認

コントロールノードでログを表示します。

```bash
tail -f /home/ubuntu/appdsm/log.log
```

### リモートホストへの SSH 接続による確認

リモートホストに SSH で接続して、直接確認することもできます。

```bash
ssh ubuntu@172.31.1.243
tail -f /opt/appdynamics/appdsmartagent/log.log
ps aux | grep smartagent
```

## 追加コマンド

### 起動せずにインストール

Smart Agent を起動せずにインストールするには、以下を実行します。

```bash
sudo ./smartagentctl install --remote --verbose
```

これは、バイナリと設定をコピーしますが、エージェントプロセスは起動しません。

### Smart Agent の停止

すべてのリモートホストで Smart Agent を停止するには、以下を実行します。

```bash
sudo ./smartagentctl stop --remote --verbose
```

### システムサービスとしてのインストール

Smart Agent を systemd サービスとしてインストールするには（本番環境では推奨）、以下を実行します。

```bash
sudo ./smartagentctl start --remote --verbose --service
```

サービスとしてインストールした場合、

- Smart Agent はシステム起動時に自動的に開始します
- `systemctl` コマンドを使用して管理できます
- システムロギングとの統合が向上します

### Smart Agent のアンインストール

リモートホストから Smart Agent を完全に削除するには、以下を実行します。

```bash
sudo ./smartagentctl uninstall --remote --verbose
```

{{% notice title="警告" style="danger" icon="exclamation-triangle" %}}
uninstall コマンドは、リモートホストからすべての Smart Agent ファイルを削除します。重要な設定ファイルやログファイルのバックアップがあることを確認してください。
{{% /notice %}}

## AppDynamics Controller での確認

リモートホストで Smart Agent を起動した後、

1. **AppDynamics Controller へのログイン**: コントローラーの URL に移動します
2. **Servers への移動**: Controller UI の Servers セクションを確認します
3. **エージェントの確認**: リストに Smart Agent が表示されるはずです
4. **メトリクスの確認**: 各ホストからメトリクスが収集されていることを確認します

### 期待されるタイムライン

- **エージェント登録**: エージェントは通常 1〜2 分以内に Controller に表示されます
- **初期メトリクス**: 最初のメトリクスは通常 5 分以内に到着します
- **完全なデータ**: 完全なデータ収集は、最初のポーリング間隔（`config.ini` で設定）の後に開始します

## ログファイルの場所

ログはコントロールノードとリモートホストの両方に書き込まれます。

| 場所 | パス | 説明 |
|----------|------|-------------|
| **コントロールノード** | `/home/ubuntu/appdsm/log.log` | インストールおよびデプロイのログ |
| **リモートホスト** | `/opt/appdynamics/appdsmartagent/log.log` | エージェントのランタイムログ |

## 並列処理について

`remote.yaml` の `max_concurrency` 設定は、並列実行を制御します。

- **低い値 (1〜2)**: 順次処理、低速だが安全
- **デフォルト (4)**: ほとんどの環境で適切なバランス
- **高い値 (8 以上)**: 多数のホストへの高速デプロイ、より多くのリソースが必要

例: 12 個のホストと `max_concurrency: 4` の場合、

- 第 1 バッチ: ホスト 1〜4 が同時に処理されます
- 第 2 バッチ: ホスト 5〜8 が同時に処理されます
- 第 3 バッチ: ホスト 9〜12 が同時に処理されます

## 各リモートホストで何が起こるか

start コマンドを実行すると、各リモートホストで以下が発生します。

1. **ディレクトリ作成**: `/opt/appdynamics/appdsmartagent/` を作成します
2. **ファイル転送**: `smartagent` バイナリ、`config.ini`、ライブラリをコピーします
3. **権限設定**: 適切なファイル権限を設定します
4. **プロセス開始**: Smart Agent プロセスを起動します
5. **検証**: プロセスが稼働していることを確認します

## 次のステップ

Smart Agent のインストールと起動が成功したら、

1. ✅ AppDynamics Controller UI にエージェントが表示されることを確認します
2. ✅ メトリクスが収集されていることを確認します
3. ✅ 必要に応じてアプリケーション監視を設定します
4. ✅ アラートとダッシュボードをセットアップします
5. ✅ エージェントのヘルスとパフォーマンスを監視します

問題が発生した場合は、Troubleshooting セクションに進んでください。
