---
title: パイプラインの作成
weight: 3
time: 10 minutes
---

## 概要

GitHubリポジトリには、Smart Agentのライフサイクルを管理するための4つの主要パイプラインが含まれています。

1. **Deploy Smart Agent** - Smart Agentサービスをインストールして起動します
2. **Install Machine Agent** - smartagentctl経由でMachine Agentをインストールします
3. **Install Database Agent** - smartagentctl経由でDatabase Agentをインストールします
4. **Cleanup All Agents** - /opt/appdynamicsディレクトリを削除します

すべてのパイプラインコードは[sm-jenkins GitHubリポジトリ](https://github.com/chambear2809/sm-jenkins)で利用可能です。

## パイプラインファイル

リポジトリには以下のJenkinsfileパイプライン定義が含まれています。

```
sm-jenkins/
└── pipelines/
    ├── Jenkinsfile.deploy                  # Deploy Smart Agent
    ├── Jenkinsfile.install-machine-agent  # Install Machine Agent
    ├── Jenkinsfile.install-db-agent       # Install Database Agent
    └── Jenkinsfile.cleanup                # Cleanup All Agents
```

## Jenkinsでパイプラインを作成する

使用したい各Jenkinsfileについて、以下の手順でJenkinsにパイプラインを作成します。

### 方法1: SCMからのパイプライン（推奨）

この方法では、パイプラインコードをバージョン管理下に置き、変更を自動的に同期します。

#### ステップ1: リポジトリをフォークまたはクローンする

まず、リポジトリを自分のGitHubアカウントまたは組織にフォークするか、元のリポジトリを直接使用します。

**Repository URL**: `https://github.com/chambear2809/sm-jenkins`

#### ステップ2: Jenkinsでパイプラインを作成する

1. **Jenkins Dashboard** に移動します
2. **New Item** をクリックします
3. アイテム名を入力します（例: `Deploy-Smart-Agent`）
4. **Pipeline** を選択します
5. **OK** をクリックします

#### ステップ3: パイプラインを設定する

パイプライン設定ページで以下を設定します。

**General Section:**

- **Description**: `Deploys AppDynamics Smart Agent to multiple hosts`
- **Discard old builds** はチェックしないままにします（または必要に応じて設定します）

**Build Triggers:**

- 手動実行のみの場合はチェックしないままにします
- 必要に応じてwebhook/pollingを設定します

**Pipeline Section:**

- **Definition**: `Pipeline script from SCM` を選択します
- **SCM**: `Git` を選択します
- **Repository URL**: `https://github.com/chambear2809/sm-jenkins`
- **Credentials**: プライベートリポジトリを使用する場合は追加します
- **Branch Specifier**: `*/main`（または `*/master`）
- **Script Path**: `pipelines/Jenkinsfile.deploy`

#### ステップ4: 保存

**Save** をクリックしてパイプラインを作成します。

#### ステップ5: 他のパイプラインでも繰り返す

作成したい各パイプラインについて、適切なスクリプトパスを使用してステップ2〜4を繰り返します。

| Pipeline Name | Script Path |
|---------------|-------------|
| Deploy-Smart-Agent | `pipelines/Jenkinsfile.deploy` |
| Install-Machine-Agent | `pipelines/Jenkinsfile.install-machine-agent` |
| Install-Database-Agent | `pipelines/Jenkinsfile.install-db-agent` |
| Cleanup-All-Agents | `pipelines/Jenkinsfile.cleanup` |

### 方法2: パイプラインスクリプトを直接入力

Jenkinsfileの内容を直接Jenkinsにコピーすることもできます。

1. **Create New Item**（方法1と同じ）
2. **Pipeline** セクションで以下を設定します
   - **Definition**: `Pipeline script` を選択します
   - **Script**: GitHubからJenkinsfileの内容全体をコピー/ペーストします
3. **Save**

{{% notice style="tip" %}}
方法1（SCM）を推奨します。パイプラインをバージョン管理下に置き、更新を容易にするためです。
{{% /notice %}}

## パイプラインパラメータ

各パイプラインは設定可能なパラメータを受け付けます。以下はメインのデプロイパイプラインの主要パラメータです。

### Deploy Smart Agentパイプラインのパラメータ

| パラメータ | デフォルト値 | 説明 |
|-----------|---------|-------------|
| `SMARTAGENT_ZIP_PATH` | `/var/jenkins_home/smartagent/appdsmartagent.zip` | JenkinsサーバーでのSmart Agent ZIPのパス |
| `REMOTE_INSTALL_DIR` | `/opt/appdynamics/appdsmartagent` | ターゲットホストでのインストールディレクトリ |
| `APPD_USER` | `ubuntu` | Smart Agentプロセスを実行するユーザー |
| `APPD_GROUP` | `ubuntu` | Smart Agentプロセスを実行するグループ |
| `SSH_PORT` | `22` | リモートホストのSSHポート |
| `AGENT_NAME` | `smartagent` | Smart Agent名 |
| `LOG_LEVEL` | `DEBUG` | ログレベル（DEBUG, INFO, WARN, ERROR） |

### Cleanupパイプラインのパラメータ

| パラメータ | デフォルト値 | 説明 |
|-----------|---------|-------------|
| `REMOTE_INSTALL_DIR` | `/opt/appdynamics/appdsmartagent` | 削除するディレクトリ |
| `SSH_PORT` | `22` | リモートホストのSSHポート |
| `CONFIRM_CLEANUP` | `false` | クリーンアップを実行するにはチェックが必要 |

{{% notice style="warning" %}}
Cleanupパイプラインには、誤削除を防ぐための確認パラメータが含まれています。クリーンアップを実行するには `CONFIRM_CLEANUP` をチェックする必要があります。
{{% /notice %}}

## パイプライン構造の理解

デプロイパイプラインの主要コンポーネントを確認しましょう。

### 1. Agent宣言

```groovy
agent { label 'linux' }
```

これにより、パイプラインが `linux` ラベルを持つJenkins Agentで実行されることが保証されます。

### 2. Parametersブロック

```groovy
parameters {
    string(name: 'SMARTAGENT_ZIP_PATH', ...)
    string(name: 'REMOTE_INSTALL_DIR', ...)
    // ... more parameters
}
```

ビルドをトリガーする際に設定できるパラメータを定義します。

### 3. Stages

デプロイパイプラインには以下のステージがあります。

1. **Preparation** - クレデンシャルからターゲットホストを読み込みます
2. **Extract Smart Agent** - ZIPファイルをステージングディレクトリに展開します
3. **Configure Smart Agent** - config.iniテンプレートを作成します
4. **Deploy to Remote Hosts** - ファイルをコピーし、各ホストでSmart Agentを起動します
5. **Verify Installation** - すべてのホストでSmart Agentのステータスを確認します

### 4. Credentials Binding

```groovy
withCredentials([
    sshUserPrivateKey(credentialsId: 'ssh-private-key', ...),
    string(credentialsId: 'account-access-key', ...)
]) {
    // Pipeline code with access to credentials
}
```

クレデンシャルをログに公開することなく安全に読み込みます。

### 5. Post Actions

```groovy
post {
    success { ... }
    failure { ... }
    always { ... }
}
```

パイプラインの完了後に実行されるアクションを定義します（成功・失敗にかかわらず実行されます）。

## パイプラインの命名規則

明確さと整理のために、一貫した命名規則を使用します。

**推奨される名前:**

```
01-Deploy-Smart-Agent
02-Install-Machine-Agent
03-Install-Database-Agent
04-Cleanup-All-Agents
```

数字のプレフィックスにより、Jenkinsダッシュボードで論理的な順序を維持できます。

## フォルダによるパイプラインの整理

より良い整理のために、Jenkinsフォルダを使用できます。

1. **フォルダの作成**:
   - **New Item** をクリックします
   - 名前を入力します: `AppDynamics Smart Agent`
   - **Folder** を選択します
   - **OK** をクリックします

2. **フォルダ内にパイプラインを作成**:
   - フォルダに入ります
   - 上記の手順でパイプラインを作成します

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

## パイプラインコードの確認

GitHubリポジトリで完全なパイプラインコードを確認できます。

**メインデプロイパイプライン:**
[https://github.com/chambear2809/sm-jenkins/blob/main/pipelines/Jenkinsfile.deploy](https://github.com/chambear2809/sm-jenkins/blob/main/pipelines/Jenkinsfile.deploy)

**その他のパイプライン:**

- [Jenkinsfile.install-machine-agent](https://github.com/chambear2809/sm-jenkins/blob/main/pipelines/Jenkinsfile.install-machine-agent)
- [Jenkinsfile.install-db-agent](https://github.com/chambear2809/sm-jenkins/blob/main/pipelines/Jenkinsfile.install-db-agent)
- [Jenkinsfile.cleanup](https://github.com/chambear2809/sm-jenkins/blob/main/pipelines/Jenkinsfile.cleanup)

## パイプライン設定のテスト

完全なデプロイを実行する前に、パイプラインの設定をテストします。

### 1. 単一ホストでのドライラン

1. IPアドレスを1つだけ含むテスト用クレデンシャル `deployment-hosts-test` を作成します
2. パイプラインを一時的に変更してこのクレデンシャルを使用します
3. パイプラインを実行し、単一ホストで動作することを確認します
4. 確認後、完全なホストリストを使用するように更新します

### 2. 構文チェック

Jenkinsには組み込みの構文バリデータがあります。

1. パイプラインに移動します
2. **Pipeline Syntax** リンクをクリックします
3. **Declarative Directive Generator** を使用して構文を検証します

## 次のステップ

パイプラインが作成できたら、最初のSmart Agentデプロイを実行する準備が整いました。
