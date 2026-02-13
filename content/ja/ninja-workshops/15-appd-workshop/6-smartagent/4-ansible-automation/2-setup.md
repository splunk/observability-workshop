---
title: セットアップと設定
weight: 2
time: 10 minutes
---

## ステップ2: ファイルとディレクトリ構成を準備する

Ansibleデプロイ用のプロジェクトディレクトリを作成します。以下のファイルを含める必要があります：

```text
.
├── appdsmartagent_64_linux_24.6.0.2143.deb  # Debian package
├── appdsmartagent_64_linux_24.6.0.2143.rpm  # RedHat package
├── inventory-cloud.yaml                     # Inventory file
├── smartagent.yaml                          # Playbook
└── variables.yaml                           # Variables file
```

ターゲット環境に適したSmart Agentパッケージをダウンロード済みであることを確認してください。

## ステップ3: ファイルの内容を理解する

### 1. インベントリファイル（`inventory-cloud.yaml`）

インベントリファイルには、Smart Agentをデプロイするホストの一覧を記載します。ホストと認証情報をここで定義します。

```yaml
all:
  hosts:
    smartagent-host-1:
      ansible_host: 54.173.1.106
      ansible_username: ec2-user
      ansible_password: ins3965!
      ansible_become: yes
      ansible_become_method: sudo
      ansible_become_password: ins3965!
      ansible_ssh_common_args: '-o StrictHostKeyChecking=no'

    smartagent-host-2:
      ansible_host: 192.168.86.107
      ansible_username: aleccham
      ansible_password: ins3965!
      ansible_become: yes
      ansible_become_method: sudo
      ansible_become_password: ins3965!

    smartagent-host-3:
      ansible_host: 54.82.95.69
      ansible_username: ubuntu
      ansible_password: ins3965!
      ansible_become: yes
      ansible_become_method: sudo
      ansible_become_password: ins3965!
```

**Action**: `ansible_host` のIPアドレスと認証情報を、実際のラボ環境の情報に更新します。

### 2. 変数ファイル（`variables.yaml`）

このファイルには、Smart Agentの設定情報が含まれています。

```yaml
smart_agent:
  controller_url: 'CONTROLLER URL HERE, JUST THE BASE URL' # o11y.saas.appdynamics.com
  account_name: 'Account Name Here'
  account_access_key: 'YOUR ACCESS KEY HERE'
  fm_service_port: '443' # Use 443 or 8080 depending on your environment.
  ssl: true

smart_agent_package_debian: 'appdsmartagent_64_linux_24.6.0.2143.deb'  # or the appropriate package name
smart_agent_package_redhat: 'appdsmartagent_64_linux_24.6.0.2143.rpm'  # or the appropriate package name
```

**Action**: `smart_agent` セクションを、使用するController URL、アカウント名、アクセスキーに更新します。

### 3. プレイブック（`smartagent.yaml`）

このプレイブックは、Cisco AppDynamics Distribution of OpenTelemetry Collectorのデプロイをオーケストレーションします。タスクの概要は以下のとおりです：

1. **前提パッケージ**: 必要なパッケージをインストールします（RedHatの場合は `yum-utils`、Debianの場合は `curl`/`apt-transport-https`）。
2. **ディレクトリのセットアップ**: `/opt/appdynamics/appdsmartagent` ディレクトリが存在することを確認します。
3. **設定**:
    * `config.ini` が存在するかチェックします。
    * 存在しない場合、`variables.yaml` の値を使用してデフォルトの `config.ini` を作成します。
    * `lineinfile` を使用して設定キー（AccountAccessKey、ControllerURLなど）を更新し、設定が正しいことを確認します。
4. **パッケージ管理**:
    * OSファミリー（Debian/RedHat）に基づいて適切なパッケージパスを決定します。
    * パッケージがローカルに存在しない場合は失敗します。
    * パッケージをターゲットホストの `/tmp` ディレクトリにコピーします。
    * `dpkg` または `yum` を使用してパッケージをインストールします。
5. **サービス管理**: `smartagent` サービスを再起動します。
6. **クリーンアップ**: 一時パッケージファイルを削除します。

このプレイブックは、`when: ansible_os_family == ...` の条件分岐を使用して、同じワークフロー内でRedHatとDebianの両方のシステムに対応しています。
