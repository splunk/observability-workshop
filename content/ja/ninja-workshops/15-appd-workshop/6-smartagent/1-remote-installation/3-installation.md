---
title: 3. インストールと起動
weight: 3
---

設定ファイルの準備ができたら、`smartagentctl` コマンドラインツールを使用してリモートホストにSmart Agentをインストールし、起動できます。

## インストールプロセスの概要

インストールプロセスは以下の手順で構成されます

1. **接続**: 定義されたすべてのホストへのSSH接続を確立します
2. **転送**: Smart Agentのバイナリと設定をリモートホストにコピーします
3. **インストール**: 各ホストの `/opt/appdynamics/appdsmartagent/` にSmart Agentをインストールします
4. **起動**: 各リモートホストでSmart Agentプロセスを起動します
5. **ログ出力**: コンソールとログファイルに詳細な進捗を出力します

## ステップ1: インストールディレクトリに移動

Smart Agentのインストールディレクトリに移動します

```bash
cd /home/ubuntu/appdsm
```

## ステップ2: 設定ファイルの確認

インストールを開始する前に、設定ファイルが正しく設定されていることを確認します

### リモートホスト設定の確認

```bash
cat remote.yaml
```

すべてのホストIPアドレス、ポート、SSH設定が正しいことを確認します。

### エージェント設定の確認

```bash
cat config.ini
```

コントローラーURL、アカウント認証情報、その他の設定が正確であることを確認します。

## ステップ3: リモートホストで Smart Agent を起動

以下のコマンドを実行して、`remote.yaml` で定義されたすべてのリモートホストでSmart Agentを起動します

```bash
sudo ./smartagentctl start --remote --verbose
```

### コマンドの内訳

- `sudo`: 特権操作に必要です
- `./smartagentctl`: 制御ユーティリティ
- `start`: Smart Agentを起動するコマンド
- `--remote`: リモートホストにデプロイ（`remote.yaml` から読み取り）
- `--verbose`: 詳細なデバッグログを有効化

{{% notice title="注意" style="warning" icon="triangle-exclamation" %}}
`--verbose` フラグの使用を強く推奨します。インストールの進捗に関する詳細な出力が提供され、問題の特定に役立ちます。
{{% /notice %}}

## ステップ4: インストールの監視

`--verbose` フラグにより、以下の詳細な出力が提供されます

- SSH接続ステータス
- ファイル転送の進捗
- 各ホストでのインストール手順
- エージェントの起動ステータス
- エラーや警告

### 期待される出力

以下のような出力が表示されます

```text
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

## ステップ5: インストールの確認

インストールが完了したら、リモートホストでSmart Agentが実行されていることを確認します。

### リモートでのステータス確認

statusコマンドを使用してすべてのリモートホストを確認します

```bash
sudo ./smartagentctl status --remote --verbose
```

各ホストに問い合わせて、Smart Agentが実行中かどうかを報告します。

### コントロールノードのログ確認

コントロールノードのログを確認します

```bash
tail -f /home/ubuntu/appdsm/log.log
```

### リモートホストにSSHで接続して確認

リモートホストにSSHで接続して直接確認することもできます

```bash
ssh ubuntu@172.31.1.243
tail -f /opt/appdynamics/appdsmartagent/log.log
ps aux | grep smartagent
```

## その他のコマンド

### 起動せずにインストールのみ実行

Smart Agentを起動せずにインストールのみ行います

```bash
sudo ./smartagentctl install --remote --verbose
```

バイナリと設定をコピーしますが、エージェントプロセスは起動しません。

### Smart Agent の停止

すべてのリモートホストでSmart Agentを停止します

```bash
sudo ./smartagentctl stop --remote --verbose
```

### システムサービスとしてインストール

Smart Agentをsystemdサービスとしてインストールします（本番環境で推奨）

```bash
sudo ./smartagentctl start --remote --verbose --service
```

サービスとしてインストールした場合

- システム起動時にSmart Agentが自動的に起動します
- `systemctl` コマンドで管理できます
- システムログとの統合が向上します

### Smart Agent のアンインストール

リモートホストからSmart Agentを完全に削除します

```bash
sudo ./smartagentctl uninstall --remote --verbose
```

{{% notice title="警告" style="danger" icon="exclamation-triangle" %}}
uninstallコマンドはリモートホストからすべてのSmart Agentファイルを削除します。重要な設定ファイルやログファイルのバックアップがあることを確認してください。
{{% /notice %}}

## AppDynamics Controller での確認

リモートホストでSmart Agentを起動した後

1. **AppDynamics Controller にログイン**: コントローラーURLに移動します
2. **Servers に移動**: Controller UIのServersセクションを確認します
3. **エージェントの確認**: Smart Agentがリストに表示されます
4. **Metric の確認**: 各ホストからMetricが収集されていることを確認します

### 期待されるタイムライン

- **エージェントの登録**: エージェントは通常、起動後1～2分以内にControllerに表示されます
- **初期 Metric**: 最初のMetricは通常5分以内に到着します
- **完全なデータ**: 最初のポーリング間隔後に完全なデータ収集が開始されます（`config.ini` で設定）

## ログファイルの場所

ログはコントロールノードとリモートホストの両方に書き込まれます

| 場所                   | パス                                          | 説明                           |
|------------------------|-----------------------------------------------|--------------------------------|
| **コントロールノード** | `/home/ubuntu/appdsm/log.log`                 | インストールとデプロイのログ   |
| **リモートホスト**     | `/opt/appdynamics/appdsmartagent/log.log`     | エージェントのランタイムログ   |

## 同時実行数について

`remote.yaml` の `max_concurrency` 設定は並列実行を制御します

- **低い値（1-2）**: 逐次処理、低速だが安全
- **デフォルト（4）**: ほとんどの環境に適したバランス
- **高い値（8以上）**: 多数のホストへの高速デプロイ、より多くのリソースが必要

例: 12台のホストで `max_concurrency: 4` の場合

- 第1バッチ: ホスト1-4を同時に処理
- 第2バッチ: ホスト5-8を同時に処理
- 第3バッチ: ホスト9-12を同時に処理

## 各リモートホストでの処理内容

startコマンドを実行すると、各リモートホストで以下の処理が行われます

1. **ディレクトリの作成**: `/opt/appdynamics/appdsmartagent/` を作成します
2. **ファイル転送**: `smartagent` バイナリ、`config.ini`、ライブラリをコピーします
3. **権限の設定**: 適切なファイル権限を設定します
4. **プロセスの起動**: Smart Agentプロセスを起動します
5. **確認**: プロセスが実行中であることを確認します

## 次のステップ

Smart Agentのインストールと起動が正常に完了した後

1. AppDynamics Controller UIにエージェントが表示されることを確認します
2. Metricが収集されていることを確認します
3. 必要に応じてアプリケーションモニタリングを設定します
4. アラートとDashboardを設定します
5. エージェントの正常性とパフォーマンスを監視します

問題が発生した場合は、トラブルシューティングセクションに進みます。
