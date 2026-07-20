---
title: Machine Agentのデプロイ
time: 5 minutes
weight: 3
description: サーバーエージェントを手動でインストールします。
---

この演習では、以下の操作を行います。

1. Machine agentをインストールするスクリプトを実行する
2. Machine agentを設定する
3. Machine agentを起動する

{{% notice title="注意" style="orange"  %}}
スクリプトを使用してEC2インスタンスにMachine agentをダウンロードします。通常は[https://accounts.appdynamics.com/](https://accounts.appdynamics.com/)にログインしてMachine agentをダウンロードする必要がありますが、アクセス制限の可能性があるため、ポータルから直接ダウンロードするスクリプトを使用します。AppDynamicsポータルにアクセスできる場合にMachine agentをダウンロードしたい場合は、以下の手順に従ってダウンロードし、APMラボのInstall Agentセクションの手順を参照してVMにSCPで転送してください。

1. [AppDynamics Portal](https://accounts.appdynamics.com/)にログインします
2. 左側のメニューで **Downloads** をクリックします
3. **Type** で **Machine Agent** を選択します
4. **Operating System** で **Linux** を選択します
5. **Machine Agent Bundle - 64-bit linux (zip)** を見つけて **Download** ボタンをクリックします
6. Install Agentセクションの手順に従い、ダウンロードしたファイルをEC2インスタンスにSCPで転送します
7. zipファイルを/opt/appdynamics/machineagentディレクトリに展開し、このラボの設定セクションに進みます
{{% /notice %}}

## インストールスクリプトの実行

以下のコマンドを使用して、スクリプトがあるディレクトリに移動します。スクリプトはMachine agentをダウンロードして展開します。

```bash
cd /opt/appdynamics/lab-artifacts/machineagent/
```

以下のコマンドを使用してインストールスクリプトを実行します。

```bash
chmod +x install_machineagent.sh
./install_machineagent.sh
```

以下の画像のような出力が表示されます。

![Install Output](images/install-script-output.png)

## Server Agentの設定

Java Agentの"controller-info.xml"から以下の設定プロパティ値を取得し、次の手順で使用できるようにしておきます。

```bash
cat /opt/appdynamics/javaagent/conf/controller-info.xml
```

- controller-host
- controller-port
- controller-ssl-enabled
- account-name
- account-access-key

Machine Agentの"controller-info.xml"ファイルを編集し、Java Agent設定ファイルから取得した以下のプロパティの値を挿入します。

- controller-host
- controller-port
- controller-ssl-enabled
- account-name
- account-access-key

"sim-enabled"プロパティをtrueに設定してファイルを保存します。以下の画像のようになります。

```bash
cd /opt/appdynamics/machineagent/conf
nano controller-info.xml
```

![Example Config](images/controller-example.png)

## Server Visibility agentの起動

以下のコマンドを使用してServer Visibility agentを起動し、起動したことを確認します。

```bash
cd /opt/appdynamics/machineagent/bin
nohup ./machine-agent &
ps -ef | grep machine
```

以下の画像のような出力が表示されます。

![Example Output](images/run-machine-agent.png)
