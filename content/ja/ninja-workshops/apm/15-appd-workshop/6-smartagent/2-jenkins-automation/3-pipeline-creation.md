---
title: パイプラインの作成
weight: 3
time: 10 minutes
---

## 概要

GitHubリポジトリには、Smart Agentのライフサイクルを管理するための4つの主要なパイプラインが含まれています。

1. **Deploy Smart Agent** - Smart Agentサービスのインストールと起動
2. **Install Machine Agent** - smartagentctl経由でMachine Agentをインストール
3. **Install Database Agent** - smartagentctl経由でDatabase Agentをインストール
4. **Cleanup All Agents** - /opt/appdynamicsディレクトリを削除

すべてのパイプラインコードは、[sm-jenkins GitHubリポジトリ](https://github.com/chambear2809/sm-jenkins)で入手できます。

## パイプラインファイル

リポジトリには、以下のJenkinsfileパイプライン定義が含まれています。

```
sm-jenkins/
└── pipelines/
    ├── Jenkinsfile.deploy                  # Deploy Smart Agent
    ├── Jenkinsfile.install-machine-agent  # Install Machine Agent
    ├── Jenkinsfile.install-db-agent       # Install Database Agent
    └── Jenkinsfile.cleanup                # Cleanup All Agents
```

## Jenkinsでのパイプライン作成

使用したい各Jenkinsfileについて、以下の手順に従ってJenkinsでパイプラインを作成します。

### 方法1: SCMからのパイプライン（推奨）

この方法では、パイプラインコードをバージョン管理下に保ち、変更を自動的に同期します。

#### ステップ1: リポジトリのフォークまたはクローン

まず、リポジトリを自身のGitHubアカウントまたは組織にフォークするか、元のリポジトリを直接使用します。

**Repository URL**: `https://github.com/chambear2809/sm-jenkins`

#### ステップ2: Jenkinsでパイプラインを作成

1. **Jenkins Dashboard** に移動します
2. **New Item** をクリックします
3. アイテム名を入力します（例: `Deploy-Smart-Agent`）
4. **Pipeline** を選択します
5. **OK** をクリックします

#### ステップ3: パイプラインの構成

パイプラインの構成ページで以下を設定します。

**General Section:**

- **Description**: `Deploys AppDynamics Smart Agent to multiple hosts`
- **Discard old builds** はチェックを外したままにします（または必要に応じて設定）

**Build Triggers:**

- 手動実行のみとする場合はチェックを外したままにします
- 必要に応じてwebhookやポーリングを構成します

**Pipeline Section:**

- **Definition**: `Pipeline script from SCM` を選択します
- **SCM**: `Git` を選択します
- **Repository URL**: `https://github.com/chambear2809/sm-jenkins`
- **Credentials**: プライベートリポジトリを使用する場合は追加します
- **Branch Specifier**: `*/main`（または `*/master`）
- **Script Path**: `pipelines/Jenkinsfile.deploy`

#### ステップ4: 保存

**Save** をクリックしてパイプラインを作成します。

#### ステップ5: 他のパイプラインに対しても繰り返し

作成したい各パイプラインに対して、適切なスクリプトパスを使用してステップ2〜4を繰り返します。

| Pipeline Name | Script Path |
|---------------|-------------|
| Deploy-Smart-Agent | `pipelines/Jenkinsfile.deploy` |
| Install-Machine-Agent | `pipelines/Jenkinsfile.install-machine-agent` |
| Install-Database-Agent | `pipelines/Jenkinsfile.install-db-agent` |
| Cleanup-All-Agents | `pipelines/Jenkinsfile.cleanup` |

### 方法2: 直接パイプラインスクリプト

代わりに、Jenkinsfileの内容を直接Jenkinsにコピーすることもできます。

1. **Create New Item**（方法1と同じ）
2. **Pipeline** セクションで以下を設定します:
   - **Definition**: `Pipeline script` を選択します
   - **Script**: GitHubから Jenkinsfile の内容全体をコピー＆ペーストします
3. **Save**

{{% notice style="tip" %}}
方法1（SCM）は、パイプラインをバージョン管理下に保ち、更新を容易にするため推奨されます。
{{% /notice %}}

## パイプラインパラメーター

各パイプラインは構成可能なパラメーターを受け取ります。メインのデプロイメントパイプラインの主要なパラメーターは以下のとおりです。

### Deploy Smart Agent パイプラインのパラメーター

| Parameter | Default | Description |
|-----------|---------|-------------|
| `SMARTAGENT_ZIP_PATH` | `/var/jenkins_home/smartagent/appdsmartagent.zip` | JenkinsサーバーのSmart Agent ZIPへのパス |
| `REMOTE_INSTALL_DIR` | `/opt/appdynamics/appdsmartagent` | ターゲットホストのインストールディレクトリ |
| `APPD_USER` | `ubuntu` | Smart Agentプロセスを実行するユーザー |
| `APPD_GROUP` | `ubuntu` | Smart Agentプロセスを実行するグループ |
| `SSH_PORT` | `22` | リモートホスト用のSSHポート |
| `AGENT_NAME` | `smartagent` | Smart Agentの名前 |
| `LOG_LEVEL` | `DEBUG` | ログレベル（DEBUG、INFO、WARN、ERROR） |

### Cleanup パイプラインのパラメーター

| Parameter | Default | Description |
|-----------|---------|-------------|
| `REMOTE_INSTALL_DIR` | `/opt/appdynamics/appdsmartagent` | 削除するディレクトリ |
| `SSH_PORT` | `22` | リモートホスト用のSSHポート |
| `CONFIRM_CLEANUP` | `false` | クリーンアップを進めるためにチェックする必要があります |

{{% notice style="warning" %}}
クリーンアップパイプラインには、誤った削除を防ぐための確認パラメーターが含まれています。クリーンアップを実行するには、`CONFIRM_CLEANUP` をチェックする必要があります。
{{% /notice %}}

## パイプライン構造の理解

デプロイメントパイプラインの主要なコンポーネントを確認してみましょう。

### 1. Agent宣言

```groovy
agent { label 'linux' }
```

これにより、`linux` ラベルを持つJenkinsエージェント上でパイプラインが実行されることが保証されます。

### 2. Parametersブロック

```groovy
parameters {
    string(name: 'SMARTAGENT_ZIP_PATH', ...)
    string(name: 'REMOTE_INSTALL_DIR', ...)
    // ... more parameters
}
```

ビルドのトリガー時に設定可能な構成パラメーターを定義します。

### 3. Stages

デプロイメントパイプラインには、以下のステージがあります。

1. **Preparation** - 認証情報からターゲットホストを読み込みます
2. **Extract Smart Agent** - ZIPファイルをステージングディレクトリに展開します
3. **Configure Smart Agent** - config.iniテンプレートを作成します
4. **Deploy to Remote Hosts** - 各ホストにファイルをコピーし、Smart Agentを起動します
5. **Verify Installation** - 全ホストでSmart Agentのステータスを確認します

### 4. Credentialsバインディング

```groovy
withCredentials([
    sshUserPrivateKey(credentialsId: 'ssh-private-key', ...),
    string(credentialsId: 'account-access-key', ...)
]) {
    // Pipeline code with access to credentials
}
```

ログに認証情報を露出させることなく、安全に認証情報を読み込みます。

### 5. Post Actions

```groovy
post {
    success { ... }
    failure { ... }
    always { ... }
}
```

成功・失敗に関わらず、パイプライン完了後に実行するアクションを定義します。

## パイプラインの命名規則

明確さと整理のために、一貫した命名規則を使用します。

**推奨される名前:**

```
01-Deploy-Smart-Agent
02-Install-Machine-Agent
03-Install-Database-Agent
04-Cleanup-All-Agents
```

数値プレフィックスは、Jenkinsダッシュボードでの論理的な順序を維持するのに役立ちます。

## フォルダーによるパイプラインの整理

より良い整理のために、Jenkinsフォルダーを使用できます。

1. **フォルダーの作成**:
   - **New Item** をクリックします
   - 名前を入力します: `AppDynamics Smart Agent`
   - **Folder** を選択します
   - **OK** をクリックします

2. **フォルダー内にパイプラインを作成**:
   - フォルダーに入ります
   - 上記の手順に従ってパイプラインを作成します

**構造の例:**

```
AppDynamics Smart Agent/
├── Deployment/
│   └── 01-Deploy-Smart-Agent
├── Agent Installation/
│   ├── 02-Install-Machine-Agent
│   └── 03-Install-Database-Agent
└── Cleanup/
    └── 04-Cleanup-All-Agents
```

## パイプラインコードの参照

GitHubリポジトリで、完全なパイプラインコードを参照できます。

**メインのデプロイメントパイプライン:**
[https://github.com/chambear2809/sm-jenkins/blob/main/pipelines/Jenkinsfile.deploy](https://github.com/chambear2809/sm-jenkins/blob/main/pipelines/Jenkinsfile.deploy)

**その他のパイプライン:**

- [Jenkinsfile.install-machine-agent](https://github.com/chambear2809/sm-jenkins/blob/main/pipelines/Jenkinsfile.install-machine-agent)
- [Jenkinsfile.install-db-agent](https://github.com/chambear2809/sm-jenkins/blob/main/pipelines/Jenkinsfile.install-db-agent)
- [Jenkinsfile.cleanup](https://github.com/chambear2809/sm-jenkins/blob/main/pipelines/Jenkinsfile.cleanup)

## パイプライン構成のテスト

完全なデプロイメントを実行する前に、パイプライン構成をテストします。

### 1. 単一ホストでのドライラン

1. 1つのIPのみを持つテスト認証情報 `deployment-hosts-test` を作成します
2. パイプラインを一時的に変更して、この認証情報を使用するようにします
3. パイプラインを実行し、単一ホストで動作することを確認します
4. 確認できたら、完全なホストリストを使用するように更新します

### 2. 構文チェック

Jenkinsには組み込みの構文バリデーターが提供されています。

1. パイプラインに移動します
2. **Pipeline Syntax** リンクをクリックします
3. **Declarative Directive Generator** を使用して構文を検証します

## 次のステップ

パイプラインが作成できたので、最初のSmart Agentデプロイメントを実行する準備が整いました！
