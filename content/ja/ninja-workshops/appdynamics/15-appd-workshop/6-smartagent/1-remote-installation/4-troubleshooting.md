---
title: 4. トラブルシューティング
weight: 4
---

このセクションでは、Smart Agent をリモートホストにデプロイする際に発生する可能性のある一般的な問題とその解決方法について説明します。

## SSH 接続の問題

### 問題: リモートホストに接続できない

**症状:**

- 接続タイムアウトエラー
- "Permission denied" メッセージ
- ホストキー検証の失敗

**解決策:**

#### 1. SSH キーのパーミッションを確認する

SSH キーには正しいパーミッションが設定されている必要があります:

```bash
chmod 600 /home/ubuntu/.ssh/id_rsa
chmod 644 /home/ubuntu/.ssh/id_rsa.pub
chmod 700 /home/ubuntu/.ssh
```

#### 2. SSH 接続を手動でテストする

各リモートホストへの接続をテストします:

```bash
ssh -i /home/ubuntu/.ssh/id_rsa ubuntu@172.31.1.243
```

これが失敗する場合、問題は smartagentctl ではなく SSH の設定にあります。

#### 3. リモートホストの到達可能性を確認する

ネットワーク接続を確認します:

```bash
ping 172.31.1.243
telnet 172.31.1.243 22
```

#### 4. SSH ユーザーを確認する

`remote.yaml` のユーザー名が SSH ユーザーと一致していることを確認します:

```yaml
protocol:
  auth:
    username: ubuntu  # Must match your SSH user
```

#### 5. Known Hosts を確認する

ホストキー検証が有効な場合、ホストが known_hosts に登録されていることを確認します:

```bash
ssh-keyscan 172.31.1.243 >> /home/ubuntu/.ssh/known_hosts
```

または、`remote.yaml` でホストキー検証を一時的に無効にします:

```yaml
protocol:
  auth:
    ignore_host_key_validation: true
```

{{% notice title="Warning" style="danger" icon="exclamation-triangle" %}}
ホストキー検証の無効化はテスト目的でのみ使用してください。本番環境では必ず有効にしてください。
{{% /notice %}}

## パーミッションの問題

### 問題: インストール中にパーミッション拒否が発生する

**症状:**

- ディレクトリ作成時の "Permission denied"
- `/opt/appdynamics/` に書き込みできない
- 権限不足エラー

**解決策:**

#### 1. コントロールノードでの Sudo アクセスを確認する

```bash
sudo -v
```

#### 2. Privileged 設定を確認する

`remote.yaml` で `privileged: true` が設定されていることを確認します:

```yaml
protocol:
  auth:
    privileged: true
```

#### 3. リモートユーザーのパーミッションを確認する

リモートユーザーには sudo 権限または root 権限が必要です。リモートホストでテストします:

```bash
ssh ubuntu@172.31.1.243
sudo mkdir -p /opt/appdynamics/test
sudo rm -rf /opt/appdynamics/test
```

#### 4. リモートディレクトリのパーミッションを確認する

カスタムインストールディレクトリを使用している場合、書き込み可能であることを確認します:

```bash
ssh ubuntu@172.31.1.243
ls -la /opt/appdynamics/
```

## エージェントが起動しない

### 問題: エージェントのインストールは成功するが起動しない

**症状:**

- インストールはエラーなく完了する
- リモートホストでエージェントプロセスが実行されていない
- コントロールノードのログにエラーがない

**解決策:**

#### 1. リモートホストのログを確認する

リモートホストに SSH 接続してエージェントのログを確認します:

```bash
ssh ubuntu@172.31.1.243
tail -100 /opt/appdynamics/appdsmartagent/log.log
```

以下を示すエラーメッセージを探します:

- 設定エラー
- ネットワーク接続の問題
- 依存関係の不足

#### 2. エージェントプロセスを確認する

エージェントプロセスが実行中かどうかを確認します:

```bash
ssh ubuntu@172.31.1.243
ps aux | grep smartagent
```

実行されていない場合は、手動で起動を試みます:

```bash
ssh ubuntu@172.31.1.243
cd /opt/appdynamics/appdsmartagent
sudo ./smartagent
```

#### 3. 設定ファイルを確認する

`config.ini` が正しく転送されたことを確認します:

```bash
ssh ubuntu@172.31.1.243
cat /opt/appdynamics/appdsmartagent/config.ini
```

以下を確認します:

- Controller URL が正しいこと
- アカウント資格情報が有効であること
- すべての必須フィールドが入力されていること

#### 4. Controller への接続をテストする

リモートホストから AppDynamics Controller への接続を確認します:

```bash
ssh ubuntu@172.31.1.243
curl -I https://fso-tme.saas.appdynamics.com
```

#### 5. システムリソースを確認する

リモートホストに十分なリソースがあることを確認します:

```bash
ssh ubuntu@172.31.1.243
df -h  # Check disk space
free -m  # Check memory
```

## 設定エラー

### 問題: 無効な設定

**症状:**

- YAML パースエラー
- 無効な設定パラメータエラー
- 設定エラーによりエージェントが起動しない

**解決策:**

#### 1. YAML 構文を検証する

`remote.yaml` の YAML 構文エラーを確認します:

```bash
python3 -c "import yaml; yaml.safe_load(open('/home/ubuntu/appdsm/remote.yaml'))"
```

よくある YAML の問題:

- 不正なインデント（タブではなくスペースを使用してください）
- コロンの欠落
- 引用符で囲まれていない特殊文字

#### 2. INI ファイルの形式を確認する

`config.ini` の構文エラーを確認します:

```bash
cat /home/ubuntu/appdsm/config.ini
```

よくある INI の問題:

- セクションヘッダーの欠落（例: `[CommonConfig]`）
- 無効なパラメータ名
- 等号の欠落

#### 3. Controller の資格情報を検証する

AppDynamics の資格情報が正しいことを確認します:

- **ControllerURL**: `https://` や `/controller` を含めないでください
- **AccountAccessKey**: 完全なアクセスキーである必要があります
- **AccountName**: アカウント名と正確に一致する必要があります

正しい形式の例:

```ini
ControllerURL    = fso-tme.saas.appdynamics.com
AccountAccessKey = abc123xyz789
AccountName      = fso-tme
```

## エージェントが Controller に表示されない

### 問題: エージェントは起動するが Controller UI に表示されない

**症状:**

- リモートホストでエージェントプロセスが実行されている
- エージェントログにエラーがない
- Controller UI にエージェントが表示されない

**解決策:**

#### 1. 初期登録を待つ

エージェントが起動後、Controller に表示されるまで 1〜5 分かかる場合があります。

#### 2. Controller の設定を確認する

エージェントが Controller に到達できることを確認します:

```bash
ssh ubuntu@172.31.1.243
ping fso-tme.saas.appdynamics.com
curl -I https://fso-tme.saas.appdynamics.com
```

#### 3. エージェントログで接続エラーを確認する

Controller 接続エラーを探します:

```bash
ssh ubuntu@172.31.1.243
grep -i "error\|fail\|controller" /opt/appdynamics/appdsmartagent/log.log
```

#### 4. SSL/TLS 設定を確認する

`config.ini` で SSL が有効になっていることを確認します:

```ini
EnableSSL = true
```

#### 5. ファイアウォールルールを確認する

リモートホストから Controller へのアウトバウンド HTTPS（ポート 443）が許可されていることを確認します。

#### 6. アカウント資格情報を確認する

Controller UI で AccountAccessKey と AccountName が正しいことを再確認します:

- AppDynamics Controller にログインします
- Settings → License に移動します
- アカウント名とアクセスキーを確認します

## パフォーマンスとスケーリングの問題

### 問題: デプロイが遅い、またはタイムアウトする

**症状:**

- デプロイに時間がかかりすぎる
- 多数のホストへのデプロイ時にタイムアウトエラーが発生する
- システムリソースの枯渇

**解決策:**

#### 1. 同時実行数を調整する

問題が発生している場合は、`remote.yaml` の `max_concurrency` を減らします:

```yaml
max_concurrency: 2  # Lower value for slower, more stable deployment
```

リソースに余裕がある場合は、デプロイを高速化するために増やします:

```yaml
max_concurrency: 8  # Higher value for faster deployment
```

#### 2. バッチでデプロイする

非常に大規模なデプロイの場合、ホストを複数のグループに分割します:

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

デプロイ中のネットワーク使用量を監視します:

```bash
iftop
```

帯域幅が飽和している場合は、同時実行数を減らすか、オフピーク時間帯にデプロイします。

## ログ分析

### コントロールノードのログを確認する

デプロイの詳細ログを表示します:

```bash
tail -f /home/ubuntu/appdsm/log.log
```

以下を探します:

- SSH 接続の失敗
- ファイル転送エラー
- パーミッション拒否エラー
- タイムアウトメッセージ

### リモートホストのログを確認する

リモートホストでエージェントのランタイムログを表示します:

```bash
ssh ubuntu@172.31.1.243
tail -f /opt/appdynamics/appdsmartagent/log.log
```

以下を探します:

- Controller 接続エラー
- 設定エラー
- エージェント起動の失敗
- ネットワークの問題

### ログの詳細度を上げる

より詳細なログを取得するには、`config.ini` で `LogLevel` を `DEBUG` に設定します:

```ini
[Telemetry]
LogLevel = DEBUG
```

## ヘルプを得る

問題が解決しない場合:

1. **ドキュメントを確認する**: smartagentctl のヘルプを確認します:

   ```bash
   ./smartagentctl --help
   ./smartagentctl start --help
   ```

2. **AppDynamics ドキュメントを確認する**: AppDynamics ドキュメントポータルにアクセスします

3. **ログファイルを確認する**: コントロールノードとリモートホストの両方のログを必ず確認します

4. **コンポーネントを個別にテストする**:
   - SSH 接続を個別にテストする
   - 単一ホストでエージェントの起動を手動でテストする
   - Controller への接続を個別に確認する

5. **診断情報を収集する**:
   - コントロールノードのログ
   - リモートホストのログ
   - 設定ファイル（機密データは編集済み）
   - エラーメッセージとスタックトレース

## よくあるエラーメッセージ

| エラーメッセージ | 原因 | 解決策 |
|--------------|-------|----------|
| "Permission denied (publickey)" | SSH キー認証の失敗 | SSH キーのパスとパーミッションを確認します |
| "Connection refused" | SSH ポートにアクセスできない | ファイアウォールルールと SSH デーモンを確認します |
| "No such file or directory" | 設定ファイルが見つからない | 設定ファイルの存在とパスの正確さを確認します |
| "YAML parse error" | 無効な YAML 構文 | パーサーで YAML 構文を検証します |
| "Controller unreachable" | ネットワーク接続の問題 | リモートホストから Controller への接続をテストします |
| "Invalid credentials" | アカウントキーまたは名前が間違っている | AppDynamics の資格情報を確認します |

## トラブルシューティングのベストプラクティス

1. **常に --verbose フラグを使用する**: デバッグ用の詳細な出力を提供します
2. **最初に単一ホストでテストする**: スケーリング前に 1 台のホストにデプロイします
3. **すぐにログを確認する**: デプロイ直後にログを確認します
4. **前提条件を確認する**: デプロイ前にすべての要件が満たされていることを確認します
5. **接続を個別にテストする**: SSH とネットワークの接続を個別に確認します
6. **手動コマンドを使用する**: 問題を切り分けるために手動で SSH とエージェント起動をテストします

{{% notice title="Tip" style="info" icon="lightbulb" %}}
トラブルシューティングでは、より複雑な問題に移る前に、最もシンプルなテスト（例: ping、SSH 接続）から始めてください。
{{% /notice %}}
