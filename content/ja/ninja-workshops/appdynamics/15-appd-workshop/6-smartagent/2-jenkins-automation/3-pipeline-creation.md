---
title: パイプラインの作成
weight: 3
time: 10 minutes
---

## 概要

GitHub リポジトリには、Smart Agent のライフサイクルを管理するための4つの主要パイプラインが含まれています:

1. **Deploy Smart Agent** - Smart Agent サービスをインストールして起動します
2. **Install Machine Agent** - smartagentctl 経由で Machine Agent をインストールします
3. **Install Database Agent** - smartagentctl 経由で Database Agent をインストールします
4. **Cleanup All Agents** - /opt/appdynamics ディレクトリを削除します

すべてのパイプラインコードは [sm-jenkins GitHub リポジトリ](https://github.com/chambear2809/sm-jenkins) で利用できます。

## パイプラインファイル

リポジトリには以下の Jenkinsfile パイプライン定義が含まれています:

```
sm-jenkins/
└── pipelines/
    ├── Jenkinsfile.deploy                  # Deploy Smart Agent
    ├── Jenkinsfile.install-machine-agent  # Install Machine Agent
    ├── Jenkinsfile.install-db-agent       # Install Database Agent
    └── Jenkinsfile.cleanup                # Cleanup All Agents
```

## Jenkins でのパイプライン作成

使用したい各 Jenkinsfile について、以下の手順に従って Jenkins でパイプラインを作成します。

### 方法 1: SCM からのパイプライン（推奨）

この方法では、パイプラインコードをバージョン管理下に保ち、変更を自動的に同期します。

#### ステップ 1: リポジトリのフォークまたはクローン

まず、リポジトリを自分の GitHub アカウントまたは組織にフォークするか、元のリポジトリを直接使用します。

**Repository URL**: `https://github.com/chambear2809/sm-jenkins`

#### ステップ 2: Jenkins でパイプラインを作成

1. **Jenkins Dashboard** に移動します
2. **New Item** をクリックします
3. アイテム名を入力します（例: `Deploy-Smart-Agent`）
4. **Pipeline** を選択します
5. **OK** をクリックします

#### ステップ 3: パイプラインの設定

パイプライン設定ページで以下を設定します:

**General Section:**

- **Description**: `Deploys AppDynamics Smart Agent to multiple hosts`
- **Discard old builds** はチェックを外したままにします（または必要に応じて設定します）

**Build Triggers:**

- 手動実行のみの場合はチェックを外したままにします
- 必要に応じて webhook/polling を設定します

**Pipeline Section:**

- **Definition**: `Pipeline script from SCM` を選択します
- **SCM**: `Git` を選択します
- **Repository URL**: `https://github.com/chambear2809/sm-jenkins`
- **Credentials**: プライベートリポジトリを使用する場合は追加します
- **Branch Specifier**: `*/main`（または `*/master`）
- **Script Path**: `pipelines/Jenkinsfile.deploy`

#### ステップ 4: 保存

**Save** をクリックしてパイプラインを作成します。

#### ステップ 5: 他のパイプラインについて繰り返す

作成したい各パイプラインについて、適切なスクリプトパスを使用してステップ 2〜4 を繰り返します:

| Pipeline Name | Script Path |
|---------------|-------------|
| Deploy-Smart-Agent | `pipelines/Jenkinsfile.deploy` |
| Install-Machine-Agent | `pipelines/Jenkinsfile.install-machine-agent` |
| Install-Database-Agent | `pipelines/Jenkinsfile.install-db-agent` |
| Cleanup-All-Agents | `pipelines/Jenkinsfile.cleanup` |

### 方法 2: 直接パイプラインスクリプト

代わりに、Jenkinsfile の内容を Jenkins に直接コピーすることもできます。

1. **Create New Item**（方法 1 と同じ）
2. **Pipeline** セクションで:
   - **Definition**: `Pipeline script` を選択します
   - **Script**: GitHub から Jenkinsfile の内容全体をコピー＆ペーストします
3. **Save**

{{% notice style="tip" %}}
方法 1（SCM）が推奨されます。パイプラインをバージョン管理下に保ち、更新を容易にするためです。
{{% /notice %}}

## パイプラインパラメータ

各パイプラインは設定可能なパラメータを受け付けます。以下は、メインのデプロイメントパイプラインの主要パラメータです:

### Deploy Smart Agent パイプラインパラメータ

| Parameter | Default | Description |
|-----------|---------|-------------|
| `SMARTAGENT_ZIP_PATH` | `/var/jenkins_home/smartagent/appdsmartagent.zip` | Jenkins サーバー上の Smart Agent ZIP のパス |
| `REMOTE_INSTALL_DIR` | `/opt/appdynamics/appdsmartagent` | ターゲットホスト上のインストールディレクトリ |
| `APPD_USER` | `ubuntu` | Smart Agent プロセスを実行するユーザー |
| `APPD_GROUP` | `ubuntu` | Smart Agent プロセスを実行するグループ |
| `SSH_PORT` | `22` | リモートホストの SSH ポート |
| `AGENT_NAME` | `smartagent` | Smart Agent 名 |
| `LOG_LEVEL` | `DEBUG` | ログレベル（DEBUG, INFO, WARN, ERROR） |

### Cleanup パイプラインパラメータ

| Parameter | Default | Description |
|-----------|---------|-------------|
| `REMOTE_INSTALL_DIR` | `/opt/appdynamics/appdsmartagent` | 削除するディレクトリ |
| `SSH_PORT` | `22` | リモートホストの SSH ポート |
| `CONFIRM_CLEANUP` | `false` | クリーンアップを実行するにはチェックが必要です |

{{% notice style="warning" %}}
クリーンアップパイプラインには、誤削除を防ぐための確認パラメータが含まれています。クリーンアップを実行するには `CONFIRM_CLEANUP` をチェックする必要があります。
{{% /notice %}}

## パイプライン構造の理解

デプロイメントパイプラインの主要コンポーネントを確認しましょう:

### 1. Agent 宣言

```groovy
agent { label 'linux' }
```

これにより、パイプラインは `linux` ラベルを持つ Jenkins エージェントで実行されます。

### 2. Parameters ブロック

```groovy
parameters {
    string(name: 'SMARTAGENT_ZIP_PATH', ...)
    string(name: 'REMOTE_INSTALL_DIR', ...)
    // ... more parameters
}
```

ビルドのトリガー時に設定できる設定可能なパラメータを定義します。

### 3. ステージ

デプロイメントパイプラインには以下のステージがあります:

1. **Preparation** - クレデンシャルからターゲットホストを読み込みます
2. **Extract Smart Agent** - ZIP ファイルをステージングディレクトリに展開します
3. **Configure Smart Agent** - config.ini テンプレートを作成します
4. **Deploy to Remote Hosts** - 各ホストにファイルをコピーし、Smart Agent を起動します
5. **Verify Installation** - すべてのホストで Smart Agent のステータスを確認します

### 4. クレデンシャルバインディング

```groovy
withCredentials([
    sshUserPrivateKey(credentialsId: 'ssh-private-key', ...),
    string(credentialsId: 'account-access-key', ...)
]) {
    // Pipeline code with access to credentials
}
```

クレデンシャルをログに公開せずに安全に読み込みます。

### 5. Post アクション

```groovy
post {
    success { ... }
    failure { ... }
    always { ... }
}
```

パイプラインの完了後に、成功・失敗に関係なく実行するアクションを定義します。

## パイプラインの命名規則

明確さと整理のために、一貫した命名規則を使用します:

**推奨名:**

```
01-Deploy-Smart-Agent
02-Install-Machine-Agent
03-Install-Database-Agent
04-Cleanup-All-Agents
```

数字のプレフィックスは、Jenkins ダッシュボードでの論理的な順序を維持するのに役立ちます。

## フォルダによるパイプラインの整理

より良い整理のために、Jenkins フォルダを使用できます:

1. **フォルダの作成**:
   - **New Item** をクリックします
   - 名前を入力します: `AppDynamics Smart Agent`
   - **Folder** を選択します
   - **OK** をクリックします

2. **フォルダ内でのパイプラインの作成**:
   - フォルダに入ります
   - 上記の手順に従ってパイプラインを作成します

**構造例:**

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

## パイプラインコードの閲覧

GitHub リポジトリで完全なパイプラインコードを確認できます:

**メインのデプロイメントパイプライン:**
[https://github.com/chambear2809/sm-jenkins/blob/main/pipelines/Jenkinsfile.deploy](https://github.com/chambear2809/sm-jenkins/blob/main/pipelines/Jenkinsfile.deploy)

**その他のパイプライン:**

- [Jenkinsfile.install-machine-agent](https://github.com/chambear2809/sm-jenkins/blob/main/pipelines/Jenkinsfile.install-machine-agent)
- [Jenkinsfile.install-db-agent](https://github.com/chambear2809/sm-jenkins/blob/main/pipelines/Jenkinsfile.install-db-agent)
- [Jenkinsfile.cleanup](https://github.com/chambear2809/sm-jenkins/blob/main/pipelines/Jenkinsfile.cleanup)

## パイプライン設定のテスト

フルデプロイメントを実行する前に、パイプライン設定をテストします:

### 1. 単一ホストでのドライラン

1. 1つの IP のみを含むテストクレデンシャル `deployment-hosts-test` を作成します
2. パイプラインを一時的に変更してこのクレデンシャルを使用します
3. パイプラインを実行し、単一ホストで動作することを確認します
4. 確認後、フルホストリストを使用するように更新します

### 2. 構文チェック

Jenkins には組み込みの構文バリデータがあります:

1. パイプラインに移動します
2. **Pipeline Syntax** リンクをクリックします
3. **Declarative Directive Generator** を使用して構文を検証します

## 次のステップ

パイプラインが作成されたので、最初の Smart Agent デプロイメントを実行する準備が整いました！
