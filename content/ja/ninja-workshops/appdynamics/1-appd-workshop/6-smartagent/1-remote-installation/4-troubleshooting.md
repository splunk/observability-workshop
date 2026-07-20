---
title: 4. トラブルシューティング
weight: 4
---

このセクションでは、Smart Agentをリモートホストにデプロイする際に発生する一般的な問題とその解決方法について説明します。

## SSH接続の問題

### 問題: リモートホストに接続できない

**症状:**

- 接続タイムアウトエラー
- "Permission denied"メッセージ
- ホストキー検証の失敗

**解決策:**

#### 1. SSHキーのパーミッションを確認する

SSHキーには正しいパーミッションが必要です。

```bash
chmod 600 /home/ubuntu/.ssh/id_rsa
chmod 644 /home/ubuntu/.ssh/id_rsa.pub
chmod 700 /home/ubuntu/.ssh
```

#### 2. SSH接続を手動でテストする

各リモートホストへの接続をテストします。

```bash
ssh -i /home/ubuntu/.ssh/id_rsa ubuntu@172.31.1.243
```

これが失敗する場合、問題はsmartAgentctlではなくSSH設定にあります。

#### 3. リモートホストの到達性を確認する

ネットワーク接続を確認します。

```bash
ping 172.31.1.243
telnet 172.31.1.243 22
```

#### 4. SSHユーザーを確認する

`remote.yaml` のユーザー名がSSHユーザーと一致していることを確認します。

```yaml
protocol:
  auth:
    username: ubuntu  # Must match your SSH user
```

#### 5. Known Hostsを確認する

ホストキー検証が有効な場合、ホストがknown_hostsに登録されていることを確認します。

```bash
ssh-keyscan 172.31.1.243 >> /home/ubuntu/.ssh/known_hosts
```

または、`remote.yaml` でホストキー検証を一時的に無効にします。

```yaml
protocol:
  auth:
    ignore_host_key_validation: true
```

{{% notice title="警告" style="danger" icon="exclamation-triangle" %}}
ホストキー検証の無効化はテスト目的でのみ使用してください。本番環境では必ず有効にしてください。
{{% /notice %}}

## パーミッションの問題

### 問題: インストール中にパーミッション拒否が発生する

**症状:**

- ディレクトリ作成時に"Permission denied"が発生する
- `/opt/appdynamics/` に書き込めない
- 権限不足エラー

**解決策:**

#### 1. コントロールノードでのSudoアクセスを確認する

```bash
sudo -v
```

#### 2. Privileged設定を確認する

`remote.yaml` で `privileged: true` が設定されていることを確認します。

```yaml
protocol:
  auth:
    privileged: true
```

#### 3. リモートユーザーのパーミッションを確認する

リモートユーザーにはsudo権限またはroot権限が必要です。リモートホストでテストします。

```bash
ssh ubuntu@172.31.1.243
sudo mkdir -p /opt/appdynamics/test
sudo rm -rf /opt/appdynamics/test
```

#### 4. リモートディレクトリのパーミッションを確認する

カスタムインストールディレクトリを使用している場合、書き込み可能であることを確認します。

```bash
ssh ubuntu@172.31.1.243
ls -la /opt/appdynamics/
```

## エージェントが起動しない

### 問題: エージェントのインストールは成功するが起動しない

**症状:**

- インストールがエラーなく完了する
- リモートホストでエージェントプロセスが実行されていない
- コントロールノードのログにエラーがない

**解決策:**

#### 1. リモートホストのログを確認する

リモートホストにSSH接続してエージェントのログを確認します。

```bash
ssh ubuntu@172.31.1.243
tail -100 /opt/appdynamics/appdsmartagent/log.log
```

以下を示すエラーメッセージを探します。

- 設定エラー
- ネットワーク接続の問題
- 依存関係の不足

#### 2. エージェントプロセスを確認する

エージェントプロセスが実行中か確認します。

```bash
ssh ubuntu@172.31.1.243
ps aux | grep smartagent
```

実行されていない場合、手動で起動を試みます。

```bash
ssh ubuntu@172.31.1.243
cd /opt/appdynamics/appdsmartagent
sudo ./smartagent
```

#### 3. 設定ファイルを確認する

`config.ini` が正しく転送されたことを確認します。

```bash
ssh ubuntu@172.31.1.243
cat /opt/appdynamics/appdsmartagent/config.ini
```

以下を確認します。

- Controller URLが正しいこと
- アカウント認証情報が有効であること
- すべての必須フィールドが入力されていること

#### 4. Controllerへの接続をテストする

リモートホストからAppDynamics Controllerへの接続を確認します。

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

### 問題: 無効な設定

**症状:**

- YAMLパースエラー
- 無効な設定パラメータエラー
- 設定エラーでエージェントが起動に失敗する

**解決策:**

#### 1. YAML構文を検証する

`remote.yaml` のYAML構文エラーを確認します。

```bash
python3 -c "import yaml; yaml.safe_load(open('/home/ubuntu/appdsm/remote.yaml'))"
```

よくあるYAMLの問題:

- 不正なインデント（タブではなくスペースを使用すること）
- コロンの欠落
- クォートされていない特殊文字

#### 2. INIファイルのフォーマットを確認する

`config.ini` の構文エラーを確認します。

```bash
cat /home/ubuntu/appdsm/config.ini
```

よくあるINIの問題:

- セクションヘッダーの欠落（例: `[CommonConfig]`）
- 無効なパラメータ名
- 等号の欠落

#### 3. Controller認証情報を検証する

AppDynamicsの認証情報が正しいことを確認します。

- **ControllerURL**: `https://` や `/controller` を含めないこと
- **AccountAccessKey**: 完全なアクセスキーであること
- **AccountName**: アカウント名と正確に一致すること

正しいフォーマットの例:

```ini
ControllerURL    = fso-tme.saas.appdynamics.com
AccountAccessKey = abc123xyz789
AccountName      = fso-tme
```

## エージェントがControllerに表示されない

### 問題: エージェントは起動するがController UIに表示されない

**症状:**

- リモートホストでエージェントプロセスが実行中
- エージェントログにエラーがない
- Controller UIにエージェントが表示されない

**解決策:**

#### 1. 初回登録を待つ

エージェントは起動後、Controllerに表示されるまで1〜5分かかる場合があります。

#### 2. Controller設定を確認する

エージェントがControllerに到達できることを確認します。

```bash
ssh ubuntu@172.31.1.243
ping fso-tme.saas.appdynamics.com
curl -I https://fso-tme.saas.appdynamics.com
```

#### 3. エージェントログで接続エラーを確認する

Controller接続エラーを探します。

```bash
ssh ubuntu@172.31.1.243
grep -i "error\|fail\|controller" /opt/appdynamics/appdsmartagent/log.log
```

#### 4. SSL/TLS設定を確認する

`config.ini` でSSLが有効になっていることを確認します。

```ini
EnableSSL = true
```

#### 5. ファイアウォールルールを確認する

リモートホストからControllerへのアウトバウンドHTTPS（ポート443）が許可されていることを確認します。

#### 6. アカウント認証情報を確認する

Controller UIでAccountAccessKeyとAccountNameが正しいことを再確認します。

- AppDynamics Controllerにログインします
- Settings → Licenseに移動します
- アカウント名とアクセスキーを確認します

## パフォーマンスとスケーリングの問題

### 問題: デプロイが遅いまたはタイムアウトする

**症状:**

- デプロイに時間がかかりすぎる
- 多数のホストへのデプロイ時にタイムアウトエラーが発生する
- システムリソースの枯渇

**解決策:**

#### 1. 同時実行数を調整する

問題が発生している場合、`remote.yaml` の `max_concurrency` を減らします。

```yaml
max_concurrency: 2  # Lower value for slower, more stable deployment
```

リソースに余裕がある場合、より高速なデプロイのために増やします。

```yaml
max_concurrency: 8  # Higher value for faster deployment
```

#### 2. バッチでデプロイする

非常に大規模なデプロイの場合、ホストを複数のグループに分割します。

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

各バッチを個別にデプロイします。

#### 3. ネットワーク帯域幅を確認する

デプロイ中のネットワーク使用量を監視します。

```bash
iftop
```

帯域幅が飽和している場合、同時実行数を減らすか、オフピーク時間にデプロイします。

## ログ分析

### コントロールノードのログを確認する

デプロイの詳細ログを表示します。

```bash
tail -f /home/ubuntu/appdsm/log.log
```

以下を探します。

- SSH接続の失敗
- ファイル転送エラー
- パーミッション拒否エラー
- タイムアウトメッセージ

### リモートホストのログを確認する

リモートホストでエージェントのランタイムログを表示します。

```bash
ssh ubuntu@172.31.1.243
tail -f /opt/appdynamics/appdsmartagent/log.log
```

以下を探します。

- Controller接続エラー
- 設定エラー
- エージェント起動の失敗
- ネットワークの問題

### ログの詳細度を上げる

より詳細なログを取得するには、`config.ini` で `LogLevel` を `DEBUG` に設定します。

```ini
[Telemetry]
LogLevel = DEBUG
```

## ヘルプの入手

問題が解決しない場合:

1. **ドキュメントを確認する**: smartagentctlのヘルプを参照します

   ```bash
   ./smartagentctl --help
   ./smartagentctl start --help
   ```

2. **AppDynamicsドキュメントを参照する**: AppDynamicsドキュメントポータルにアクセスします

3. **ログファイルを確認する**: コントロールノードとリモートホストの両方のログを必ず確認します

4. **コンポーネントを個別にテストする**:
   - SSH接続を個別にテストします
   - 単一ホストでエージェントの起動を手動でテストします
   - Controllerへの接続を独立して確認します

5. **診断情報を収集する**:
   - コントロールノードのログ
   - リモートホストのログ
   - 設定ファイル（機密データは編集済み）
   - エラーメッセージとスタックトレース

## よくあるエラーメッセージ

| エラーメッセージ | 原因 | 解決策 |
|--------------|-------|----------|
| "Permission denied (publickey)" | SSHキー認証の失敗 | SSHキーのパスとパーミッションを確認する |
| "Connection refused" | SSHポートにアクセスできない | ファイアウォールルールとSSHデーモンを確認する |
| "No such file or directory" | 設定ファイルが見つからない | 設定ファイルの存在とパスが正しいことを確認する |
| "YAML parse error" | 無効なYAML構文 | パーサーでYAML構文を検証する |
| "Controller unreachable" | ネットワーク接続の問題 | リモートホストからControllerへの接続をテストする |
| "Invalid credentials" | アカウントキーまたは名前が間違っている | AppDynamicsの認証情報を確認する |

## トラブルシューティングのベストプラクティス

1. **常に--verboseフラグを使用する**: デバッグのための詳細な出力を提供します
2. **最初に単一ホストでテストする**: スケーリングする前に1つのホストにデプロイします
3. **すぐにログを確認する**: デプロイ直後にログを確認します
4. **前提条件を確認する**: デプロイ前にすべての要件が満たされていることを確認します
5. **接続を個別にテストする**: SSHとネットワーク接続を独立して確認します
6. **手動コマンドを使用する**: 問題を切り分けるためにSSHとエージェントの手動起動をテストします

{{% notice title="ヒント" style="info" icon="lightbulb" %}}
トラブルシューティングでは、より複雑な問題に進む前に、最も簡単なテスト（例: ping、SSH接続）から始めてください。
{{% /notice %}}
