---
title: 3. インストールと起動
weight: 3
---

設定ファイルの準備ができたので、`smartagentctl` コマンドラインツールを使用してリモートホストに Smart Agent をインストールして起動できます。

## インストールプロセスの概要

インストールプロセスには以下が含まれます

1. **接続**: 定義されたすべてのホストへの SSH 接続を確立します
2. **転送**: Smart Agent のバイナリと設定をリモートホストにコピーします
3. **インストール**: 各ホストの `/opt/appdynamics/appdsmartagent/` に Smart Agent をインストールします
4. **起動**: 各リモートホストで Smart Agent プロセスを起動します
5. **ログ記録**: コンソールとログファイルに詳細な進行状況を出力します

## ステップ 1: インストールディレクトリへ移動

Smart Agent のインストールディレクトリに移動します

```bash
cd /home/ubuntu/appdsm
```

## ステップ 2: 設定ファイルの確認

インストールを開始する前に、設定ファイルが正しくセットアップされていることを確認します

### リモートホスト設定の確認

```bash
cat remote.yaml
```

すべてのホスト IP アドレス、ポート、SSH 設定が正しいことを確認してください。

### エージェント設定の確認

```bash
cat config.ini
```

コントローラー URL、アカウント認証情報、その他の設定が正確であることを確認してください。

## ステップ 3: リモートホストで Smart Agent を起動

以下のコマンドを実行して、`remote.yaml` で定義されたすべてのリモートホストで Smart Agent を起動します

```bash
sudo ./smartagentctl start --remote --verbose
```

### コマンドの詳細

- `sudo`: 特権操作に必要です
- `./smartagentctl`: 制御ユーティリティです
- `start`: Smart Agent を起動するコマンドです
- `--remote`: リモートホストにデプロイします（`remote.yaml` から読み取ります）
- `--verbose`: 詳細なデバッグログを有効にします

{{% notice title="注意" style="warning" icon="triangle-exclamation" %}}
`--verbose` フラグの使用を強く推奨します。インストールの進行状況に関する詳細な出力が提供され、問題の特定に役立ちます。
{{% /notice %}}

## ステップ 4: インストールの監視

`--verbose` フラグにより、以下を含む詳細な出力が提供されます

- SSH 接続ステータス
- ファイル転送の進行状況
- 各ホストでのインストール手順
- エージェントの起動ステータス
- エラーまたは警告

### 期待される出力

以下のような出力が表示されます

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

インストールが完了したら、リモートホストで Smart Agent が実行されていることを確認します。

### リモートでステータスを確認

ステータスコマンドを使用してすべてのリモートホストを確認します

```bash
sudo ./smartagentctl status --remote --verbose
```

このコマンドは各ホストに問い合わせ、Smart Agent が実行中かどうかを報告します。

### コントロールノードでログを確認

コントロールノードでログを表示します

```bash
tail -f /home/ubuntu/appdsm/log.log
```

### リモートホストに SSH して確認

リモートホストに SSH して直接確認することもできます

```bash
ssh ubuntu@172.31.1.243
tail -f /opt/appdynamics/appdsmartagent/log.log
ps aux | grep smartagent
```

## 追加コマンド

### 起動せずにインストール

Smart Agent を起動せずにインストールするには

```bash
sudo ./smartagentctl install --remote --verbose
```

このコマンドはバイナリと設定をコピーしますが、エージェントプロセスは起動しません。

### Smart Agent の停止

すべてのリモートホストで Smart Agent を停止するには

```bash
sudo ./smartagentctl stop --remote --verbose
```

### システムサービスとしてインストール

Smart Agent を systemd サービスとしてインストールするには（本番環境で推奨）

```bash
sudo ./smartagentctl start --remote --verbose --service
```

サービスとしてインストールした場合

- Smart Agent はシステム起動時に自動的に開始されます
- `systemctl` コマンドで管理できます
- システムログとの統合が向上します

### Smart Agent のアンインストール

リモートホストから Smart Agent を完全に削除するには

```bash
sudo ./smartagentctl uninstall --remote --verbose
```

{{% notice title="警告" style="danger" icon="exclamation-triangle" %}}
アンインストールコマンドはリモートホストからすべての Smart Agent ファイルを削除します。重要な設定ファイルやログファイルのバックアップがあることを確認してください。
{{% /notice %}}

## AppDynamics Controller での確認

リモートホストで Smart Agent を起動した後

1. **AppDynamics Controller にログイン**: コントローラー URL に移動します
2. **サーバーに移動**: Controller UI のサーバーセクションを確認します
3. **エージェントを確認**: リストに Smart Agent が表示されていることを確認します
4. **メトリクスを確認**: 各ホストからメトリクスが収集されていることを確認します

### 想定されるタイムライン

- **エージェント登録**: エージェントは通常 1〜2 分以内に Controller に表示されます
- **初期メトリクス**: 最初のメトリクスは通常 5 分以内に到着します
- **完全なデータ**: 完全なデータ収集は最初のポーリング間隔後に開始されます（`config.ini` で設定）

## ログファイルの場所

ログはコントロールノードとリモートホストの両方に書き込まれます

| 場所 | パス | 説明 |
|------|------|------|
| **コントロールノード** | `/home/ubuntu/appdsm/log.log` | インストールとデプロイメントのログ |
| **リモートホスト** | `/opt/appdynamics/appdsmartagent/log.log` | エージェントランタイムログ |

## 並行処理の理解

`remote.yaml` の `max_concurrency` 設定は並列実行を制御します

- **低い値 (1-2)**: 順次処理、低速ですがより安全です
- **デフォルト (4)**: ほとんどの環境に適したバランスです
- **高い値 (8+)**: 多くのホストへの高速デプロイメント、より多くのリソースが必要です

例：12 ホストで `max_concurrency: 4` の場合

- 最初のバッチ: ホスト 1〜4 が同時に処理されます
- 2 番目のバッチ: ホスト 5〜8 が同時に処理されます
- 3 番目のバッチ: ホスト 9〜12 が同時に処理されます

## 各リモートホストで行われる処理

start コマンドを実行すると、各リモートホストで以下が行われます

1. **ディレクトリ作成**: `/opt/appdynamics/appdsmartagent/` を作成します
2. **ファイル転送**: `smartagent` バイナリ、`config.ini`、ライブラリをコピーします
3. **権限設定**: 適切なファイル権限を設定します
4. **プロセス起動**: Smart Agent プロセスを起動します
5. **確認**: プロセスが実行中であることを確認します

## 次のステップ

Smart Agent のインストールと起動が正常に完了した後

1. ✅ AppDynamics Controller UI にエージェントが表示されることを確認します
2. ✅ メトリクスが収集されていることを確認します
3. ✅ 必要に応じてアプリケーション監視を設定します
4. ✅ アラートとダッシュボードを設定します
5. ✅ エージェントの正常性とパフォーマンスを監視します

問題が発生した場合は、トラブルシューティングセクションに進んでください。
