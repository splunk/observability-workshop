---
title: 4. トラブルシューティング
weight: 4
---

このセクションでは、Smart Agentをリモートホストにデプロイする際に発生する一般的な問題とその解決方法について説明します。

## SSH接続の問題

### 問題: リモートホストに接続できない

**症状:**

- 接続タイムアウトエラー
- "Permission denied" メッセージ
- ホストキー検証の失敗

**解決方法:**

#### 1. SSHキーの権限を確認

SSHキーには正しい権限が必要です:

```bash
chmod 600 /home/ubuntu/.ssh/id_rsa
chmod 644 /home/ubuntu/.ssh/id_rsa.pub
chmod 700 /home/ubuntu/.ssh
```

#### 2. SSH接続を手動でテスト

各リモートホストへの接続をテストします:

```bash
ssh -i /home/ubuntu/.ssh/id_rsa ubuntu@172.31.1.243
```

これが失敗する場合、問題はsmartagentctlではなくSSH設定にあります。

#### 3. リモートホストの到達性を確認

ネットワーク接続性を確認します:

```bash
ping 172.31.1.243
telnet 172.31.1.243 22
```

#### 4. SSHユーザーの確認

`remote.yaml` のユーザー名がSSHユーザーと一致していることを確認します:

```yaml
protocol:
  auth:
    username: ubuntu  # Must match your SSH user
```

#### 5. Known Hosts の確認

ホストキー検証が有効な場合、ホストがknown_hostsに登録されていることを確認します:

```bash
ssh-keyscan 172.31.1.243 >> /home/ubuntu/.ssh/known_hosts
```

または、`remote.yaml` でホストキー検証を一時的に無効化します:

```yaml
protocol:
  auth:
    ignore_host_key_validation: true
```

{{% notice title="警告" style="danger" icon="exclamation-triangle" %}}
ホストキー検証の無効化はテスト目的でのみ使用してください。本番環境では必ず有効にしてください。
{{% /notice %}}

## 権限の問題

### 問題: インストール中に権限が拒否される

**症状:**

- ディレクトリ作成時の "Permission denied"
- `/opt/appdynamics/` への書き込み不可
- 権限不足エラー

**解決方法:**

#### 1. コントロールノードでのSudoアクセスを確認

```bash
sudo -v
```

#### 2. Privileged 設定を確認

`remote.yaml` で `privileged: true` が設定されていることを確認します:

```yaml
protocol:
  auth:
    privileged: true
```

#### 3. リモートユーザーの権限を確認

リモートユーザーにはsudo権限またはroot権限が必要です。リモートホストでテストします:

```bash
ssh ubuntu@172.31.1.243
sudo mkdir -p /opt/appdynamics/test
sudo rm -rf /opt/appdynamics/test
```

#### 4. リモートディレクトリの権限を確認

カスタムインストールディレクトリを使用している場合、書き込み可能であることを確認します:

```bash
ssh ubuntu@172.31.1.243
ls -la /opt/appdynamics/
```

## エージェントが起動しない

### 問題: エージェントのインストールは成功するが起動しない

**症状:**

- インストールはエラーなく完了
- リモートホストでエージェントプロセスが実行されていない
- コントロールノードのログにエラーなし

**解決方法:**

#### 1. リモートホストのログを確認

リモートホストにSSHで接続してエージェントのログを確認します:

```bash
ssh ubuntu@172.31.1.243
tail -100 /opt/appdynamics/appdsmartagent/log.log
```

以下を示すエラーメッセージを探します:

- 設定エラー
- ネットワーク接続の問題
- 依存関係の不足

#### 2. エージェントプロセスの確認

エージェントプロセスが実行中かどうかを確認します:

```bash
ssh ubuntu@172.31.1.243
ps aux | grep smartagent
```

実行されていない場合、手動で起動を試みます:

```bash
ssh ubuntu@172.31.1.243
cd /opt/appdynamics/appdsmartagent
sudo ./smartagent
```

#### 3. 設定ファイルの確認

`config.ini` が正しく転送されたことを確認します:

```bash
ssh ubuntu@172.31.1.243
cat /opt/appdynamics/appdsmartagent/config.ini
```

以下を確認します:

- コントローラーURLが正しいこと
- アカウント認証情報が有効であること
- 必須フィールドがすべて入力されていること

#### 4. コントローラーへの接続テスト

リモートホストからAppDynamics Controllerへの接続を確認します:

```bash
ssh ubuntu@172.31.1.243
curl -I https://fso-tme.saas.appdynamics.com
```

#### 5. システムリソースの確認

リモートホストに十分なリソースがあることを確認します:

```bash
ssh ubuntu@172.31.1.243
df -h  # Check disk space
free -m  # Check memory
```

## 設定エラー

### 問題: 無効な設定

**症状:**

- YAML解析エラー
- 無効な設定パラメーターエラー
- 設定エラーでエージェントが起動に失敗

**解決方法:**

#### 1. YAML構文の検証

`remote.yaml` のYAML構文エラーを確認します:

```bash
python3 -c "import yaml; yaml.safe_load(open('/home/ubuntu/appdsm/remote.yaml'))"
```

一般的なYAMLの問題:

- インデントの誤り（タブではなくスペースを使用）
- コロンの欠落
- 引用符で囲まれていない特殊文字

#### 2. INIファイル形式の確認

`config.ini` の構文エラーを確認します:

```bash
cat /home/ubuntu/appdsm/config.ini
```

一般的なINIの問題:

- セクションヘッダーの欠落（例: `[CommonConfig]`）
- 無効なパラメーター名
- 等号の欠落

#### 3. コントローラー認証情報の検証

AppDynamicsの認証情報が正しいことを確認します:

- **ControllerURL**: `https://` や `/controller` を含めないこと
- **AccountAccessKey**: 完全なアクセスキーであること
- **AccountName**: アカウント名と正確に一致すること

正しい形式の例:

```ini
ControllerURL    = fso-tme.saas.appdynamics.com
AccountAccessKey = abc123xyz789
AccountName      = fso-tme
```

## エージェントが Controller に表示されない

### 問題: エージェントが起動するが Controller UI に表示されない

**症状:**

- リモートホストでエージェントプロセスが実行中
- エージェントログにエラーなし
- Controller UIにエージェントが表示されない

**解決方法:**

#### 1. 初期登録を待つ

エージェントが起動してからControllerに表示されるまで1～5分かかる場合があります。

#### 2. コントローラー設定の確認

エージェントがコントローラーに到達できることを確認します:

```bash
ssh ubuntu@172.31.1.243
ping fso-tme.saas.appdynamics.com
curl -I https://fso-tme.saas.appdynamics.com
```

#### 3. エージェントログで接続エラーを確認

コントローラー接続エラーを確認します:

```bash
ssh ubuntu@172.31.1.243
grep -i "error\|fail\|controller" /opt/appdynamics/appdsmartagent/log.log
```

#### 4. SSL/TLS設定の確認

`config.ini` でSSLが有効になっていることを確認します:

```ini
EnableSSL = true
```

#### 5. ファイアウォールルールの確認

リモートホストからControllerへのアウトバウンドHTTPS（ポート443）が許可されていることを確認します。

#### 6. アカウント認証情報の確認

Controller UIでAccountAccessKeyとAccountNameが正しいことを再確認します:

- AppDynamics Controllerにログインします
- Settings > Licenseに移動します
- アカウント名とアクセスキーを確認します

## パフォーマンスとスケーリングの問題

### 問題: デプロイが遅い、またはタイムアウトする

**症状:**

- デプロイに時間がかかりすぎる
- 多数のホストへのデプロイ時にタイムアウトエラー
- システムリソースの枯渇

**解決方法:**

#### 1. 同時実行数の調整

問題が発生している場合、`remote.yaml` の `max_concurrency` を減らします:

```yaml
max_concurrency: 2  # Lower value for slower, more stable deployment
```

リソースに余裕がある場合、より高速なデプロイのために増やします:

```yaml
max_concurrency: 8  # Higher value for faster deployment
```

#### 2. バッチに分けてデプロイ

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

#### 3. ネットワーク帯域幅の確認

デプロイ中のネットワーク使用量を監視します:

```bash
iftop
```

帯域幅が飽和している場合、同時実行数を減らすか、ピーク外の時間帯にデプロイします。

## ログ分析

### コントロールノードのログ確認

詳細なデプロイログを確認します:

```bash
tail -f /home/ubuntu/appdsm/log.log
```

以下を確認します:

- SSH接続の失敗
- ファイル転送エラー
- 権限拒否エラー
- タイムアウトメッセージ

### リモートホストのログ確認

リモートホストのエージェントランタイムログを確認します:

```bash
ssh ubuntu@172.31.1.243
tail -f /opt/appdynamics/appdsmartagent/log.log
```

以下を確認します:

- コントローラー接続エラー
- 設定エラー
- エージェント起動の失敗
- ネットワークの問題

### ログの詳細度を上げる

より詳細なログが必要な場合、`config.ini` で `LogLevel` を `DEBUG` に設定します:

```ini
[Telemetry]
LogLevel = DEBUG
```

## ヘルプの取得

問題が解決しない場合:

1. **ドキュメントの確認**: smartagentctlのヘルプを確認します:

   ```bash
   ./smartagentctl --help
   ./smartagentctl start --help
   ```

2. **AppDynamics ドキュメントの確認**: AppDynamicsドキュメントポータルを参照します

3. **ログファイルの確認**: コントロールノードとリモートホストの両方のログを必ず確認します

4. **コンポーネントを個別にテスト**:
   - SSH接続性を個別にテストします
   - 単一のホストでエージェントの起動を手動でテストします
   - コントローラーへの接続性を個別に確認します

5. **診断情報の収集**:
   - コントロールノードのログ
   - リモートホストのログ
   - 設定ファイル（機密データは削除）
   - エラーメッセージとスタックトレース

## 一般的なエラーメッセージ

| エラーメッセージ | 原因 | 解決方法 |
| --- | --- | --- |
| "Permission denied (publickey)" | SSHキー認証の失敗 | SSHキーのパスと権限を確認 |
| "Connection refused" | SSHポートにアクセスできない | ファイアウォールルールとSSHデーモンを確認 |
| "No such file or directory" | 設定ファイルが見つからない | 設定ファイルの存在とパスが正しいことを確認 |
| "YAML parse error" | 無効なYAML構文 | YAMLパーサーで構文を検証 |
| "Controller unreachable" | ネットワーク接続の問題 | リモートホストからコントローラーへの接続性をテスト |
| "Invalid credentials" | アカウントキーまたは名前が不正 | AppDynamics の認証情報を確認 |

## トラブルシューティングのベストプラクティス

1. **常に --verbose フラグを使用**: デバッグのための詳細な出力を提供します
2. **最初に単一のホストでテスト**: スケールアウトする前に1台のホストにデプロイします
3. **すぐにログを確認**: デプロイ直後にログを確認します
4. **前提条件の確認**: デプロイ前にすべての要件が満たされていることを確認します
5. **接続性を個別にテスト**: SSHとネットワーク接続性を個別に確認します
6. **手動コマンドを使用**: 手動でのSSHとエージェント起動をテストして問題を切り分けます

{{% notice title="ヒント" style="info" icon="lightbulb" %}}
トラブルシューティングでは、より複雑な問題に移る前に、最も簡単なテスト（例: ping、SSH接続性）から始めてください。
{{% /notice %}}
