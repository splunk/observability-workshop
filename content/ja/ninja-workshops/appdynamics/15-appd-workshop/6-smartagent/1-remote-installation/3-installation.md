---
title: 3. インストールと起動
weight: 3
---

設定ファイルの準備ができたら、`smartagentctl` コマンドラインツールを使用してリモートホストに Smart Agent をインストールして起動できます。

## インストールプロセスの概要

インストールプロセスには以下が含まれます:

1. **接続**: 定義されたすべてのホストへの SSH 接続を確立します
2. **転送**: Smart Agent のバイナリと設定をリモートホストにコピーします
3. **インストール**: 各ホストの `/opt/appdynamics/appdsmartagent/` に Smart Agent をインストールします
4. **起動**: 各リモートホストで Smart Agent プロセスを起動します
5. **ログ記録**: コンソールとログファイルに詳細な進捗を出力します

## ステップ 1: インストールディレクトリへの移動

Smart Agent のインストールディレクトリに移動します:

```bash
cd /home/ubuntu/appdsm
```

## ステップ 2: 設定ファイルの確認

インストールを開始する前に、設定ファイルが正しくセットアップされていることを確認します:

### リモートホスト設定の確認

```bash
cat remote.yaml
```

すべてのホスト IP アドレス、ポート、および SSH 設定が正しいことを確認してください。

### エージェント設定の確認

```bash
cat config.ini
```

コントローラー URL、アカウント認証情報、およびその他の設定が正確であることを確認してください。

## ステップ 3: リモートホストで Smart Agent を起動する

以下のコマンドを実行して、`remote.yaml` で定義されたすべてのリモートホストで Smart Agent を起動します:

```bash
sudo ./smartagentctl start --remote --verbose
```

### コマンドの詳細

- `sudo`: 特権操作に必要です
- `./smartagentctl`: 制御ユーティリティ
- `start`: Smart Agent を起動するコマンド
- `--remote`: リモートホストにデプロイします（`remote.yaml` から読み込み）
- `--verbose`: 詳細なデバッグログを有効にします

{{% notice title="注意" style="warning" icon="triangle-exclamation" %}}
`--verbose` フラグの使用を強く推奨します。インストールの進行状況に関する詳細な出力が提供され、問題の特定に役立ちます。
{{% /notice %}}

## ステップ 4: インストールの監視

`--verbose` フラグにより、以下を含む詳細な出力が提供されます:

- SSH 接続ステータス
- ファイル転送の進捗
- 各ホストでのインストール手順
- エージェントの起動ステータス
- エラーや警告

### 期待される出力

以下のような出力が表示されます:

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

### リモートでのステータス確認

status コマンドを使用してすべてのリモートホストを確認します:

```bash
sudo ./smartagentctl status --remote --verbose
```

これにより、各ホストに問い合わせを行い、Smart Agent が実行中かどうかを報告します。

### コントロールノードでのログ確認

コントロールノードでログを表示します:

```bash
tail -f /home/ubuntu/appdsm/log.log
```

### リモートホストに SSH 接続して確認

リモートホストに SSH 接続して直接確認することもできます:

```bash
ssh ubuntu@172.31.1.243
tail -f /opt/appdynamics/appdsmartagent/log.log
ps aux | grep smartagent
```

## その他のコマンド

### 起動せずにインストール

Smart Agent を起動せずにインストールするには:

```bash
sudo ./smartagentctl install --remote --verbose
```

これにより、バイナリと設定がコピーされますが、エージェントプロセスは起動しません。

### Smart Agent の停止

すべてのリモートホストで Smart Agent を停止するには:

```bash
sudo ./smartagentctl stop --remote --verbose
```

### システムサービスとしてインストール

Smart Agent を systemd サービスとしてインストールするには（本番環境で推奨）:

```bash
sudo ./smartagentctl start --remote --verbose --service
```

サービスとしてインストールした場合:

- Smart Agent はシステム起動時に自動的に開始されます
- `systemctl` コマンドで管理できます
- システムログとの統合が向上します

### Smart Agent のアンインストール

リモートホストから Smart Agent を完全に削除するには:

```bash
sudo ./smartagentctl uninstall --remote --verbose
```

{{% notice title="警告" style="danger" icon="exclamation-triangle" %}}
uninstall コマンドはリモートホストからすべての Smart Agent ファイルを削除します。重要な設定ファイルやログファイルのバックアップがあることを確認してください。
{{% /notice %}}

## AppDynamics Controller での確認

リモートホストで Smart Agent を起動した後:

1. **AppDynamics Controller にログイン**: コントローラー URL に移動します
2. **サーバーに移動**: Controller UI の Servers セクションを確認します
3. **エージェントの確認**: Smart Agent がリストに表示されていることを確認します
4. **メトリクスの確認**: 各ホストからメトリクスが収集されていることを確認します

### 予想されるタイムライン

- **エージェント登録**: エージェントは通常 1〜2 分以内に Controller に表示されます
- **初期メトリクス**: 最初のメトリクスは通常 5 分以内に到着します
- **完全なデータ**: 完全なデータ収集は最初のポーリング間隔後に開始されます（`config.ini` で設定）

## ログファイルの場所

ログはコントロールノードとリモートホストの両方に書き込まれます:

| 場所 | パス | 説明 |
|------|------|------|
| **コントロールノード** | `/home/ubuntu/appdsm/log.log` | インストールとデプロイのログ |
| **リモートホスト** | `/opt/appdynamics/appdsmartagent/log.log` | エージェントのランタイムログ |

## 並行処理の理解

`remote.yaml` の `max_concurrency` 設定は並列実行を制御します:

- **低い値 (1-2)**: 順次処理、遅いですがより安全です
- **デフォルト (4)**: ほとんどの環境に適したバランスです
- **高い値 (8+)**: 多数のホストへのデプロイが高速ですが、より多くのリソースが必要です

例: 12 台のホストで `max_concurrency: 4` の場合:

- 最初のバッチ: ホスト 1〜4 を同時に処理
- 2 番目のバッチ: ホスト 5〜8 を同時に処理
- 3 番目のバッチ: ホスト 9〜12 を同時に処理

## 各リモートホストで行われること

start コマンドを実行すると、各リモートホストで以下が実行されます:

1. **ディレクトリの作成**: `/opt/appdynamics/appdsmartagent/` を作成します
2. **ファイルの転送**: `smartagent` バイナリ、`config.ini`、およびライブラリをコピーします
3. **権限の設定**: 適切なファイル権限を設定します
4. **プロセスの起動**: Smart Agent プロセスを起動します
5. **検証**: プロセスが実行中であることを確認します

## 次のステップ

Smart Agent のインストールと起動が正常に完了したら:

1. ✅ AppDynamics Controller UI にエージェントが表示されることを確認します
2. ✅ メトリクスが収集されていることを確認します
3. ✅ 必要に応じてアプリケーション監視を設定します
4. ✅ アラートとダッシュボードを設定します
5. ✅ エージェントの健全性とパフォーマンスを監視します

問題が発生した場合は、トラブルシューティングセクションに進んでください。
