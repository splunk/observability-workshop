---
title: セットアップと設定
weight: 2
time: 10 minutes
---

## Step 2: ファイルとディレクトリ構造の準備

Ansible デプロイメント用のプロジェクトディレクトリを作成します。次のファイルを含めてください。

```text
.
├── appdsmartagent_64_linux_24.6.0.2143.deb  # Debian package
├── appdsmartagent_64_linux_24.6.0.2143.rpm  # RedHat package
├── inventory-cloud.yaml                     # Inventory file
├── smartagent.yaml                          # Playbook
└── variables.yaml                           # Variables file
```

ターゲット環境用に適切な Smart Agent パッケージをダウンロード済みであることを確認してください。

## Step 3: ファイルの理解

### 1. Inventory ファイル (`inventory-cloud.yaml`)

inventory ファイルには Smart Agent をデプロイするホストを記載します。ここでホストと認証情報を定義します。

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

**作業内容**: `ansible_host` の IP と認証情報を、実際のラボ環境の値に更新してください。

### 2. 変数ファイル (`variables.yaml`)

このファイルには Smart Agent の設定情報が含まれています。

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

**作業内容**: `smart_agent` セクションを、ご自身のコントローラー URL、アカウント名、アクセスキーで更新してください。

### 3. Playbook (`smartagent.yaml`)

この playbook は Cisco AppDynamics Distribution of OpenTelemetry Collector のデプロイメントを統括します。タスクの概要は次のとおりです。

1. **前提条件**: 必要なパッケージをインストールします (RedHat 系は `yum-utils`、Debian 系は `curl`/`apt-transport-https`)。
2. **ディレクトリの準備**: `/opt/appdynamics/appdsmartagent` ディレクトリが存在することを確認します。
3. **設定**:
    * `config.ini` が存在するか確認します。
    * 存在しない場合は、`variables.yaml` の値を使用してデフォルトの `config.ini` を作成します。
    * `lineinfile` を使用して設定キー (AccountAccessKey、ControllerURL など) を更新し、設定が正しいことを保証します。
4. **パッケージ管理**:
    * OS ファミリ (Debian/RedHat) に応じて正しいパッケージパスを判定します。
    * パッケージがローカルに存在しない場合は失敗します。
    * パッケージをターゲットホストの `/tmp` ディレクトリにコピーします。
    * `dpkg` または `yum` を使用してパッケージをインストールします。
5. **サービス管理**: `smartagent` サービスを再起動します。
6. **クリーンアップ**: 一時的なパッケージファイルを削除します。

この playbook は `when: ansible_os_family == ...` 条件分岐を使用して、同じワークフロー内で RedHat 系と Debian 系の両方のシステムに対応しています。
