---
title: 4. Troubleshooting
weight: 4
---

このセクションでは、Smart Agent をリモートホストへデプロイする際に発生しうる一般的な問題と、その解決方法について説明します。

## SSH 接続の問題

### 問題: リモートホストに接続できない

**症状:**

- 接続タイムアウトエラー
- "Permission denied" メッセージ
- ホストキー検証エラー

**解決方法:**

#### 1. SSH キーのパーミッションを確認する

SSH キーには正しいパーミッションが設定されている必要があります。

```bash
chmod 600 /home/ubuntu/.ssh/id_rsa
chmod 644 /home/ubuntu/.ssh/id_rsa.pub
chmod 700 /home/ubuntu/.ssh
```

#### 2. SSH 接続を手動でテストする

各リモートホストへの接続をテストします。

```bash
ssh -i /home/ubuntu/.ssh/id_rsa ubuntu@172.31.1.243
```

これが失敗する場合、問題は smartagentctl ではなく SSH 設定にあります。

#### 3. リモートホストへの到達性を確認する

ネットワーク接続性を確認します。

```bash
ping 172.31.1.243
telnet 172.31.1.243 22
```

#### 4. SSH ユーザーを確認する

`remote.yaml` 内のユーザー名が SSH ユーザーと一致していることを確認します。

```yaml
protocol:
  auth:
    username: ubuntu  # Must match your SSH user
```

#### 5. known_hosts を確認する

ホストキーの検証が有効な場合、ホストが known_hosts に登録されていることを確認します。

```bash
ssh-keyscan 172.31.1.243 >> /home/ubuntu/.ssh/known_hosts
```

または、`remote.yaml` 内で一時的にホストキー検証を無効にします。

```yaml
protocol:
  auth:
    ignore_host_key_validation: true
```

{{% notice title="Warning" style="danger" icon="exclamation-triangle" %}}
ホストキー検証の無効化はテスト目的のみで使用してください。本番環境では必ず有効にしてください。
{{% /notice %}}

## パーミッションの問題

### 問題: インストール時に Permission Denied が発生する

**症状:**

- ディレクトリ作成時の "Permission denied"
- `/opt/appdynamics/` への書き込み不可
- 権限不足エラー

**解決方法:**

#### 1. コントロールノードでの sudo アクセスを確認する

```bash
sudo -v
```

#### 2. Privileged 設定を確認する

`remote.yaml` で `privileged: true` が設定されていることを確認します。

```yaml
protocol:
  auth:
    privileged: true
```

#### 3. リモートユーザーの権限を確認する

リモートユーザーは sudo 権限を持っているか root である必要があります。リモートホスト上で以下をテストします。

```bash
ssh ubuntu@172.31.1.243
sudo mkdir -p /opt/appdynamics/test
sudo rm -rf /opt/appdynamics/test
```

#### 4. リモートディレクトリのパーミッションを確認する

カスタムインストールディレクトリを使用している場合、そのディレクトリが書き込み可能であることを確認します。

```bash
ssh ubuntu@172.31.1.243
ls -la /opt/appdynamics/
```

## Agent が起動しない

### 問題: エージェントのインストールは成功するがエージェントが起動しない

**症状:**

- インストールはエラーなく完了する
- リモートホスト上でエージェントプロセスが動作していない
- コントロールノードのログにエラーがない

**解決方法:**

#### 1. リモートホストのログを確認する

リモートホストに SSH 接続し、エージェントログを確認します。

```bash
ssh ubuntu@172.31.1.243
tail -100 /opt/appdynamics/appdsmartagent/log.log
```

以下を示すエラーメッセージを探します。

- 設定エラー
- ネットワーク接続性の問題
- 依存関係の不足

#### 2. エージェントプロセスを確認する

エージェントプロセスが動作しているか確認します。

```bash
ssh ubuntu@172.31.1.243
ps aux | grep smartagent
```

動作していない場合、手動で起動を試みます。

```bash
ssh ubuntu@172.31.1.243
cd /opt/appdynamics/appdsmartagent
sudo ./smartagent
```

#### 3. 設定ファイルを確認する

`config.ini` が正しく転送されているか確認します。

```bash
ssh ubuntu@172.31.1.243
cat /opt/appdynamics/appdsmartagent/config.ini
```

以下を確認します。

- Controller URL が正しい
- アカウント認証情報が有効である
- 必須フィールドがすべて入力されている

#### 4. Controller への接続をテストする

リモートホストから AppDynamics Controller への接続を確認します。

```bash
ssh ubuntu@172.31.1.243
curl -I https://fso-tme.saas.appdynamics.com
```

#### 5. システムリソースを確認する

リモートホストに十分なリソースがあることを確認します。

```bash
ssh ubuntu@172.31.1.243
df -h  # Check disk space
free -m  # Check memory
```

## 設定エラー

### 問題: 設定が無効である

**症状:**

- YAML パースエラー
- 無効な設定パラメータエラー
- 設定エラーによりエージェントが起動しない

**解決方法:**

#### 1. YAML 構文を検証する

`remote.yaml` の YAML 構文エラーを確認します。

```bash
python3 -c "import yaml; yaml.safe_load(open('/home/ubuntu/appdsm/remote.yaml'))"
```

YAML でよくある問題:

- 不正なインデント (タブではなくスペースを使用)
- コロンの欠落
- 引用符で囲まれていない特殊文字

#### 2. INI ファイルの形式を確認する

`config.ini` の構文エラーを確認します。

```bash
cat /home/ubuntu/appdsm/config.ini
```

INI でよくある問題:

- セクションヘッダーの欠落 (例: `[CommonConfig]`)
- 無効なパラメータ名
- イコール記号の欠落

#### 3. Controller の認証情報を検証する

AppDynamics の認証情報が正しいことを確認します。

- **ControllerURL**: `https://` や `/controller` を含めるべきではありません
- **AccountAccessKey**: 完全なアクセスキーである必要があります
- **AccountName**: アカウント名と完全一致する必要があります

正しい形式の例:

```ini
ControllerURL    = fso-tme.saas.appdynamics.com
AccountAccessKey = abc123xyz789
AccountName      = fso-tme
```

## Agent が Controller に表示されない

### 問題: エージェントは起動するが Controller UI に表示されない

**症状:**

- リモートホスト上でエージェントプロセスが動作している
- エージェントログにエラーがない
- Controller UI にエージェントが表示されない

**解決方法:**

#### 1. 初回登録を待つ

エージェントは起動後、Controller に表示されるまでに 1〜5 分かかる場合があります。

#### 2. Controller の設定を確認する

エージェントが Controller に到達できるかを確認します。

```bash
ssh ubuntu@172.31.1.243
ping fso-tme.saas.appdynamics.com
curl -I https://fso-tme.saas.appdynamics.com
```

#### 3. エージェントログで接続エラーを確認する

Controller への接続エラーを探します。

```bash
ssh ubuntu@172.31.1.243
grep -i "error\|fail\|controller" /opt/appdynamics/appdsmartagent/log.log
```

#### 4. SSL/TLS 設定を確認する

`config.ini` で SSL が有効になっていることを確認します。

```ini
EnableSSL = true
```

#### 5. ファイアウォールルールを確認する

リモートホストから Controller へのアウトバウンド HTTPS (ポート 443) が許可されていることを確認します。

#### 6. アカウント認証情報を確認する

Controller UI で AccountAccessKey と AccountName が正しいかを再確認します。

- AppDynamics Controller にログインします
- Settings → License に移動します
- アカウント名とアクセスキーを確認します

## パフォーマンスとスケーリングの問題

### 問題: デプロイが遅い、またはタイムアウトする

**症状:**

- デプロイに時間がかかりすぎる
- 多数のホストにデプロイする際のタイムアウトエラー
- システムリソースの枯渇

**解決方法:**

#### 1. 同時実行数を調整する

問題が発生する場合は `remote.yaml` の `max_concurrency` を減らします。

```yaml
max_concurrency: 2  # Lower value for slower, more stable deployment
```

リソースに余裕がある場合は、より高速なデプロイのために増やします。

```yaml
max_concurrency: 8  # Higher value for faster deployment
```

#### 2. バッチでデプロイする

非常に大規模なデプロイでは、ホストを複数のグループに分割します。

**remote-batch1.yaml:**

```yaml
hosts:
  - host: "172.31.1.1"
  - host: "172.31.1.2"
  - host: "172.31.1.3"
```

**remote-batch2.yaml:**

```yaml
hosts:
  - host: "172.31.1.4"
  - host: "172.31.1.5"
  - host: "172.31.1.6"
```

その後、各バッチを個別にデプロイします。

#### 3. ネットワーク帯域幅を確認する

デプロイ中のネットワーク使用状況を監視します。

```bash
iftop
```

帯域幅が飽和している場合、同時実行数を減らすか、オフピーク時間帯にデプロイします。

## ログ分析

### コントロールノードのログを確認する

詳細なデプロイログを表示します。

```bash
tail -f /home/ubuntu/appdsm/log.log
```

以下を探します。

- SSH 接続の失敗
- ファイル転送エラー
- パーミッション拒否エラー
- タイムアウトメッセージ

### リモートホストのログを確認する

リモートホスト上のエージェントランタイムログを表示します。

```bash
ssh ubuntu@172.31.1.243
tail -f /opt/appdynamics/appdsmartagent/log.log
```

以下を探します。

- Controller への接続エラー
- 設定エラー
- エージェントの起動失敗
- ネットワークの問題

### ログの詳細度を上げる

より詳細なロギングのため、`config.ini` で `LogLevel` を `DEBUG` に設定します。

```ini
[Telemetry]
LogLevel = DEBUG
```

## ヘルプの取得

それでも問題が解決しない場合:

1. **ドキュメントを確認する**: smartagentctl のヘルプを確認します。

   ```bash
   ./smartagentctl --help
   ./smartagentctl start --help
   ```

2. **AppDynamics ドキュメントを確認する**: AppDynamics のドキュメントポータルを参照します。

3. **ログファイルを確認する**: コントロールノードとリモートホストの両方のログを必ず確認します。

4. **コンポーネントを個別にテストする**:
   - SSH 接続性を個別にテストする
   - 単一ホストでエージェントの起動を手動でテストする
   - Controller への接続性を個別に検証する

5. **診断情報を収集する**:
   - コントロールノードのログ
   - リモートホストのログ
   - 設定ファイル (機密データはマスクする)
   - エラーメッセージとスタックトレース

## 一般的なエラーメッセージ

| エラーメッセージ | 原因 | 解決方法 |
|--------------|-------|----------|
| "Permission denied (publickey)" | SSH キー認証の失敗 | SSH キーのパスとパーミッションを確認する |
| "Connection refused" | SSH ポートにアクセスできない | ファイアウォールルールと SSH デーモンを確認する |
| "No such file or directory" | 設定ファイルの欠落 | 設定ファイルが存在しパスが正しいことを確認する |
| "YAML parse error" | 無効な YAML 構文 | パーサーで YAML 構文を検証する |
| "Controller unreachable" | ネットワーク接続性の問題 | リモートホストから Controller への接続をテストする |
| "Invalid credentials" | アカウントキーまたは名前が誤っている | AppDynamics の認証情報を確認する |

## トラブルシューティングのベストプラクティス

1. **常に --verbose フラグを使用する**: デバッグのための詳細な出力を提供します
2. **まず単一ホストでテストする**: スケールする前に 1 台のホストにデプロイします
3. **すぐにログを確認する**: デプロイ直後にログを確認します
4. **前提条件を確認する**: デプロイ前にすべての要件が満たされていることを確認します
5. **接続性を個別にテストする**: SSH とネットワークの接続性を個別に検証します
6. **手動コマンドを使用する**: 手動の SSH とエージェント起動をテストして問題を切り分けます

{{% notice title="Tip" style="info" icon="lightbulb" %}}
トラブルシューティングを行う際は、複雑な問題に取り組む前に、まず最も単純なテスト (例: ping、SSH 接続性) から始めてください。
{{% /notice %}}
