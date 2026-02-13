---
title: パイプライン作成
weight: 3
time: 10 minutes
---

## 概要

GitHubリポジトリには、Smart Agentのライフサイクル管理のための4つのメインパイプラインが含まれています:

1. **Deploy Smart Agent** - Smart Agentサービスのインストールと起動
2. **Install Machine Agent** - smartagentctlによるMachine Agentのインストール
3. **Install Database Agent** - smartagentctlによるDatabase Agentのインストール
4. **Cleanup All Agents** - /opt/appdynamicsディレクトリの削除

すべてのパイプラインコードは [sm-jenkins GitHub リポジトリ](https://github.com/chambear2809/sm-jenkins) で公開されています。

## パイプラインファイル

リポジトリには以下のJenkinsfileパイプライン定義が含まれています:

```text
sm-jenkins/
└── pipelines/
    ├── Jenkinsfile.deploy                  # Deploy Smart Agent
    ├── Jenkinsfile.install-machine-agent  # Install Machine Agent
    ├── Jenkinsfile.install-db-agent       # Install Database Agent
    └── Jenkinsfile.cleanup                # Cleanup All Agents
```

## Jenkins でのパイプライン作成

使用したい各Jenkinsfileに対して、以下の手順でJenkinsにパイプラインを作成します。

### 方法1: SCM からのパイプライン（推奨）

この方法では、パイプラインコードをバージョン管理に保持し、変更を自動的に同期します。

#### ステップ1: リポジトリのフォークまたはクローン

まず、リポジトリを自分のGitHubアカウントまたは組織にフォークするか、元のリポジトリを直接使用します。

**リポジトリ URL**: `https://github.com/chambear2809/sm-jenkins`

#### ステップ2: Jenkins でパイプラインを作成

1. **Jenkins Dashboard** に移動します
2. **New Item** をクリックします
3. アイテム名を入力します（例: `Deploy-Smart-Agent`）
4. **Pipeline** を選択します
5. **OK** をクリックします

#### ステップ3: パイプラインの設定

パイプライン設定ページで以下を設定します:

**General セクション:**

- **Description**: `Deploys AppDynamics Smart Agent to multiple hosts`
- **Discard old builds** はチェックしないままにします（または必要に応じて設定）

**Build Triggers:**

- 手動実行のみの場合はチェックしないままにします
- 必要に応じてWebhookやポーリングを設定します

**Pipeline セクション:**

- **Definition**: `Pipeline script from SCM` を選択します
- **SCM**: `Git` を選択します
- **Repository URL**: `https://github.com/chambear2809/sm-jenkins`
- **Credentials**: プライベートリポジトリの場合は追加します
- **Branch Specifier**: `*/main`（または `*/master`）
- **Script Path**: `pipelines/Jenkinsfile.deploy`

#### ステップ4: 保存

**Save** をクリックしてパイプラインを作成します。

#### ステップ5: 他のパイプラインでも繰り返す

作成したい各パイプラインに対して、適切なスクリプトパスを使用してステップ2-4を繰り返します:

| パイプライン名 | スクリプトパス |
| --- | --- |
| Deploy-Smart-Agent | `pipelines/Jenkinsfile.deploy` |
| Install-Machine-Agent | `pipelines/Jenkinsfile.install-machine-agent` |
| Install-Database-Agent | `pipelines/Jenkinsfile.install-db-agent` |
| Cleanup-All-Agents | `pipelines/Jenkinsfile.cleanup` |

### 方法2: パイプラインスクリプトの直接入力

または、Jenkinsfileの内容をJenkinsに直接コピーすることもできます。

1. **New Item を作成** します（方法1と同様）
2. **Pipeline** セクションで:
   - **Definition**: `Pipeline script` を選択します
   - **Script**: GitHubからJenkinsfileの内容全体をコピー/ペーストします
3. **Save** をクリックします

{{% notice style="tip" %}}
方法1（SCM）を推奨します。パイプラインをバージョン管理に保持でき、更新が容易になります。
{{% /notice %}}

## パイプラインパラメータ

各パイプラインは設定可能なパラメータを受け付けます。メインデプロイパイプラインの主要なパラメータを以下に示します:

### Deploy Smart Agent パイプラインのパラメータ

| パラメータ | デフォルト値 | 説明 |
| --- | --- | --- |
| `SMARTAGENT_ZIP_PATH` | `/var/jenkins_home/smartagent/appdsmartagent.zip` | Jenkins サーバー上の Smart Agent ZIP のパス |
| `REMOTE_INSTALL_DIR` | `/opt/appdynamics/appdsmartagent` | ターゲットホストのインストールディレクトリ |
| `APPD_USER` | `ubuntu` | Smart Agent プロセスを実行するユーザー |
| `APPD_GROUP` | `ubuntu` | Smart Agent プロセスを実行するグループ |
| `SSH_PORT` | `22` | リモートホストの SSH ポート |
| `AGENT_NAME` | `smartagent` | Smart Agent 名 |
| `LOG_LEVEL` | `DEBUG` | ログレベル（DEBUG、INFO、WARN、ERROR） |

### Cleanup パイプラインのパラメータ

| パラメータ | デフォルト値 | 説明 |
| --- | --- | --- |
| `REMOTE_INSTALL_DIR` | `/opt/appdynamics/appdsmartagent` | 削除するディレクトリ |
| `SSH_PORT` | `22` | リモートホストの SSH ポート |
| `CONFIRM_CLEANUP` | `false` | クリーンアップを実行するにはチェックが必要 |

{{% notice style="warning" %}}
Cleanupパイプラインには、誤って削除することを防ぐための確認パラメータがあります。クリーンアップを実行するには `CONFIRM_CLEANUP` にチェックを入れる必要があります。
{{% /notice %}}

## パイプライン構造の理解

デプロイパイプラインの主要なコンポーネントを見ていきます:

### 1. エージェント宣言

```groovy
agent { label 'linux' }
```

これにより、パイプラインが `linux` ラベルを持つJenkinsエージェントで実行されることが保証されます。

### 2. パラメータブロック

```groovy
parameters {
    string(name: 'SMARTAGENT_ZIP_PATH', ...)
    string(name: 'REMOTE_INSTALL_DIR', ...)
    // ... その他のパラメータ
}
```

ビルドをトリガーする際に設定できるパラメータを定義します。

### 3. ステージ

デプロイパイプラインには以下のステージがあります:

1. **Preparation** - 認証情報からターゲットホストを読み込み
2. **Extract Smart Agent** - ZIPファイルをステージングディレクトリに展開
3. **Configure Smart Agent** - config.iniテンプレートを作成
4. **Deploy to Remote Hosts** - 各ホストにファイルをコピーしSmart Agentを起動
5. **Verify Installation** - すべてのホストでSmart Agentの状態を確認

### 4. 認証情報バインディング

```groovy
withCredentials([
    sshUserPrivateKey(credentialsId: 'ssh-private-key', ...),
    string(credentialsId: 'account-access-key', ...)
]) {
    // 認証情報にアクセスできるパイプラインコード
}
```

ログに公開することなく、安全に認証情報を読み込みます。

### 5. Post アクション

```groovy
post {
    success { ... }
    failure { ... }
    always { ... }
}
```

パイプライン完了後に、成功・失敗に関わらず実行するアクションを定義します。

## パイプラインの命名規則

明確さと整理のために、一貫した命名規則を使用します:

**推奨名称:**

```text
01-Deploy-Smart-Agent
02-Install-Machine-Agent
03-Install-Database-Agent
04-Cleanup-All-Agents
```

数字のプレフィックスにより、Jenkinsダッシュボードで論理的な順序を維持できます。

## フォルダーによるパイプラインの整理

より良い整理のために、Jenkinsフォルダーを使用できます:

1. **フォルダーを作成**:
   - **New Item** をクリックします
   - 名前を入力します: `AppDynamics Smart Agent`
   - **Folder** を選択します
   - **OK** をクリックします

2. **フォルダー内にパイプラインを作成**:
   - フォルダーに入ります
   - 上記の手順でパイプラインを作成します

**構成例:**

```text
AppDynamics Smart Agent/
├── Deployment/
│   └── 01-Deploy-Smart-Agent
├── Agent Installation/
│   ├── 02-Install-Machine-Agent
│   └── 03-Install-Database-Agent
└── Cleanup/
    └── 04-Cleanup-All-Agents
```

## パイプラインコードの表示

完全なパイプラインコードはGitHubリポジトリで確認できます:

**メインデプロイパイプライン:**
[https://github.com/chambear2809/sm-jenkins/blob/main/pipelines/Jenkinsfile.deploy](https://github.com/chambear2809/sm-jenkins/blob/main/pipelines/Jenkinsfile.deploy)

**その他のパイプライン:**

- [Jenkinsfile.install-machine-agent](https://github.com/chambear2809/sm-jenkins/blob/main/pipelines/Jenkinsfile.install-machine-agent)
- [Jenkinsfile.install-db-agent](https://github.com/chambear2809/sm-jenkins/blob/main/pipelines/Jenkinsfile.install-db-agent)
- [Jenkinsfile.cleanup](https://github.com/chambear2809/sm-jenkins/blob/main/pipelines/Jenkinsfile.cleanup)

## パイプライン設定のテスト

本番デプロイを実行する前に、パイプライン設定をテストします:

### 1. 単一ホストでのドライラン

1. IPが1つだけのテスト認証情報 `deployment-hosts-test` を作成します
2. パイプラインをこの認証情報を使用するよう一時的に変更します
3. パイプラインを実行し、単一ホストで動作することを確認します
4. 確認後、完全なホストリストに更新します

### 2. 構文チェック

Jenkinsには組み込みの構文バリデーターがあります:

1. パイプラインに移動します
2. **Pipeline Syntax** リンクをクリックします
3. **Declarative Directive Generator** を使用して構文を検証します

## 次のステップ

パイプラインが作成できたら、最初のSmart Agentデプロイを実行する準備が整いました。
